from dataclasses import dataclass
from itertools import pairwise
from collections import defaultdict

@dataclass
class Tile:
    name: str
    label: str

    # rgb hex
    color: str 

    n_glue: tuple[str, int]
    e_glue: tuple[str, int]
    s_glue: tuple[str, int]
    w_glue: tuple[str, int]

@dataclass
class TAS:
    tds_file: str
    min_x: int
    min_y: int
    width: int
    height: int
    tilemap: dict[str, tuple[int, int]]

def svg_line(
    x1: float, y1: float, x2: float, y2: float,
    stroke_width: float,
    stroke_color: str,
    stroke_dash_length: float | None = None,
):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-width="{stroke_width}" stroke="{stroke_color}" ' +
       (f'stroke-dasharray="{stroke_dash_length}"' if stroke_dash_length is not None else '')+ 
         '/>'
    )

def svg_text(
    x: float, y: float,
    color: str,
    size: float,
    text: str,
    rotation: float = 0,
):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}em" text-anchor="middle" transform="rotate({rotation}, {x}, {y})">{text}</text>'

def parse_tds(file: str) -> list[Tile]:
    with open(file, 'r') as f:
        tiles = [[field.split() for field in tile.split('\n')[:-1]] for tile in f.read().split('\n\n') if tile]
        tiles = [{field[0] : '' if len(field) < 2 else field[1] for field in tile} for tile in tiles]
        
    NULL_GLUE = ('', 0)
    return [
        Tile(
            t['TILENAME'],
            t['LABEL'],
            t['TILECOLOR'],
            NULL_GLUE if 'NORTHBIND' not in t or 'NORTHLABEL' not in t else (t['NORTHLABEL'], int(t['NORTHBIND'])),
            NULL_GLUE if 'EASTBIND'  not in t or 'EASTLABEL'  not in t else (t['EASTLABEL'],  int(t['EASTBIND'] )),
            NULL_GLUE if 'SOUTHBIND' not in t or 'SOUTHLABEL' not in t else (t['SOUTHLABEL'], int(t['SOUTHBIND'])),
            NULL_GLUE if 'WESTBIND'  not in t or 'WESTLABEL'  not in t else (t['WESTLABEL'],  int(t['WESTBIND'] )),
        )
        for t in tiles
    ]

def tds_to_svg(tiles: list[Tile]) -> dict[str, str]:
    svg_tiles = {}
    for tile in tiles:
        svg_tiles[tile.name] = tile_to_svg(tile)
    return svg_tiles

def tile_to_svg(tile: Tile):
    # pixels
    STROKE_DASH_LENGTH     = 4.0
    STROKE_COLOR           = '#000000'
    STROKE_WIDTH_PRIMARY   = 3.0
    STROKE_WIDTH_SECONDARY = 2.0
    GLUE_SPACING           = 3.0
    GLUE_TEXT_SPACING      = 4.5

    # em
    FONT_SIZE_PRIMARY   = 1.10
    FONT_SIZE_SECONDARY = 0.85

    svg = f'<svg id="{tile.name}" width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'

    # Tile Color
    svg += f'<rect width="100" height="100" fill="{tile.color}"/>'

    # Text Color
    tile_rgb = tuple(map(lambda x: int(x, 16) / 0xff, [tile.color[i:i+2] for i in range(1, len(tile.color[1:]), 2)]))
    lightness = (min(tile_rgb) + max(tile_rgb)) / 2
    text_color = '#000000' if lightness > 0.55 else '#ffffff'
    if tile.name == 'SEED':
        print(lightness, text_color, tile_rgb, tile.color)

    # Tile Glues
    glue_paths = [
        (0,   0  ),
        (100, 0  ),
        (100, 100),
        (0,   100),
        (0,   0  ),
    ]
    glues = [tile.n_glue, tile.e_glue, tile.s_glue, tile.w_glue]
    text_rotation = [180, 270, 0, 90]
    for ((x1, y1), (x2, y2)), (label, strength), rotation in zip(pairwise(glue_paths), glues, text_rotation):
        offset_length = STROKE_WIDTH_PRIMARY / 2

        if strength == 0:
            x_off = offset_length * ((1 if x1 == 0 else -1) if y1 != y2 and x1 == x2 else 0)
            x1_off = x1 + x_off
            x2_off = x2 + x_off

            y_off = offset_length * ((1 if y1 == 0 else -1) if x1 != x2 and y1 == y2 else 0)
            y1_off = y1 + y_off
            y2_off = y2 + y_off

            svg += svg_line(x1_off, y1_off, x2_off, y2_off, STROKE_WIDTH_PRIMARY, STROKE_COLOR, STROKE_DASH_LENGTH)
            continue

        for i in range(strength):
            stroke_width = STROKE_WIDTH_PRIMARY if i == 0 else STROKE_WIDTH_SECONDARY

            x_off = offset_length * ((1 if x1 == 0 else -1) if y1 != y2 and x1 == x2 else 0)
            x1_off = x1 + x_off
            x2_off = x2 + x_off

            y_off = offset_length * ((1 if y1 == 0 else -1) if x1 != x2 and y1 == y2 else 0)
            y1_off = y1 + y_off
            y2_off = y2 + y_off

            offset_length += (stroke_width + STROKE_WIDTH_SECONDARY) / 2 + GLUE_SPACING
            svg += svg_line(x1_off, y1_off, x2_off, y2_off, stroke_width, STROKE_COLOR)

        x_text = (x1 + x2) / 2 + \
            (offset_length + GLUE_TEXT_SPACING) * ((1 if x1 == 0 else -1) if y1 != y2 and x1 == x2 else 0)
        y_text = (y1 + y2) / 2 + \
            (offset_length + GLUE_TEXT_SPACING) * ((1 if y1 == 0 else -1) if x1 != x2 and y1 == y2 else 0)
        svg += svg_text(x_text, y_text, text_color, FONT_SIZE_SECONDARY, label, rotation)

    # Tile Name
    svg += svg_text(50, 60, text_color, FONT_SIZE_SECONDARY, tile.name)

    # Tile Label
    svg += svg_text(50, 40, text_color, FONT_SIZE_PRIMARY, tile.label)

    svg += '</svg>'
    return svg

def parse_tdp(file: str) -> TAS:
    with open(file, 'r') as f:
        lines = f.read().split('\n')

        tds_file = lines[0]
        tiles = [line.split() for line in lines[2:] if line]


    min_x, max_x = None, None
    min_y, max_y = None, None
    tilemap = defaultdict(list)
    for tile, x, y in tiles:
        x, y = int(x), int(y)
        min_x = min(x, min_x) if min_x is not None else x
        min_y = min(y, min_y) if min_y is not None else y
        max_x = max(x, max_x) if max_x is not None else x
        max_y = max(y, max_y) if max_y is not None else y
        tilemap[tile].append((x, y))

    width  = abs(max_x - min_x) + 1
    height = abs(max_y - min_y) + 1
    return TAS(tds_file, min_x, min_y, width, height, dict(tilemap))

def tdp_to_svg(tas: TAS, svg_tiles: dict[str, str]) -> str:
    svg = f'<svg viewBox="0 0 {100*tas.width} {100*tas.height}" xmlns="http://www.w3.org/2000/svg">'

    # <defs>
    svg += '<defs>'
    svg += ''.join(svg_tile for svg_tile in svg_tiles.values())
    svg += '</defs>'

    # <use>
    svg += ''.join(
        f'<use href="#{tile}" x="{100 * (x - tas.min_x)}" y="{100*(tas.height - y - tas.min_y - 1)}"/>'
        for tile, coords in tas.tilemap.items()
        for x, y in coords
    )

    svg += '</svg>'
    return svg
        

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        prog='tas2svg',
        description='Converts tiles from a .tdp file into an .svg file.',
    )

    parser.add_argument('file')
    parser.add_argument(
        '-t',
        '--use-tds',
        help='Convert a .tds file into a set of .svg files.',
        action='store_true'
    )
    parser.add_argument(
        '-of',
        '--output-folder',
        default='.'
    )

    args = parser.parse_args()
    if args.use_tds:
        print('unimplemented')
    else:
        assert args.file.endswith('.tdp')
        print(f"Parsing .tdp file - {args.file}")
        tas = parse_tdp(args.file)

        print(f'Conveting .tds file to svg - {tas.tds_file}')
        tds = parse_tds(tas.tds_file)
        svg_tiles = tds_to_svg(tds)

        print(f'Converting .tds file to svg - {args.file}')
        with open(f'{args.output_folder}/{args.file[:-4]}.svg', 'w+') as f:
            f.write(tdp_to_svg(tas, svg_tiles))
