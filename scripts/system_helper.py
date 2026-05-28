from dataclasses import dataclass
from typing import Iterable

@dataclass
class Tile:
    name: str
    label: str

    # rgb hex
    color: str 

    n_glue: tuple[str, int] | None
    e_glue: tuple[str, int] | None
    s_glue: tuple[str, int] | None
    w_glue: tuple[str, int] | None

def serialize_tiles(file: str, tiles: Iterable[Tile]):
    with open(file, 'w+') as f:
        f.write(
            '\n\n'.join(
                '\n'.join(
                    [f'TILENAME {tile.name}',
                     f'LABEL {tile.label}',
                     (f'NORTHBIND {tile.n_glue[1]}\nNORTHLABEL {tile.n_glue[0]}' if tile.n_glue else ''),
                     (f'EASTBIND {tile.e_glue[1]}\nEASTLABEL {tile.e_glue[0]}'   if tile.e_glue else ''),
                     (f'SOUTHBIND {tile.s_glue[1]}\nSOUTHLABEL {tile.s_glue[0]}' if tile.s_glue else ''),
                     (f'WESTBIND {tile.w_glue[1]}\nWESTLABEL {tile.w_glue[0]}'   if tile.w_glue else ''),
                     f'TILECOLOR {tile.color}',
                     'CREATE',
                    ]
                )
                for tile in tiles
            )
        )

if __name__ == "__main__":
    pass



