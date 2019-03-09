from aboard import Board, Tile, Dir, BoardRenderer, compute_direction


class XmasTile(Tile):

    DICT_ROADFUL_DIRS_FROM_CHAR = {
        "-": (Dir.LEFT, Dir.RIGHT),
        "|": (Dir.UP, Dir.DOWN),
        "L": (Dir.UP, Dir.RIGHT),
        "F": (Dir.DOWN, Dir.RIGHT),
        "7": (Dir.DOWN, Dir.LEFT),
        "J": (Dir.UP, Dir.LEFT),
        "+": (Dir.LEFT, Dir.RIGHT, Dir.UP, Dir.DOWN),
        " ": (),
    }

    def __init__(self, x=None, y=None, board_owner=None):
        super().__init__(x, y, board_owner)
        self.roads = {
            Dir.UP: False,
            Dir.RIGHT: False,
            Dir.DOWN: False,
            Dir.LEFT: False
        }
        self.mid_marker = " "

    def dirs_from_input(self, char_roadful):
        for dir_ in XmasTile.DICT_ROADFUL_DIRS_FROM_CHAR[char_roadful]:
            self.roads[dir_] = True

    def render(self, w=3, h=3):

        path_up = "|" if self.roads[Dir.UP] else " "
        path_left = "-" if self.roads[Dir.LEFT] else " "
        path_right = "-" if self.roads[Dir.RIGHT] else " "
        path_down = "|" if self.roads[Dir.DOWN] else " "
        template = " %s \n%s%s%s\n %s "

        mid_marker = self.mid_marker.replace('\n', ' ')

        data = (
            path_up, path_left,
            mid_marker[:1].rjust(1),
            path_right, path_down
        )

        str_result = template % data
        return str_result.split("\n")


renderer = BoardRenderer(
    tile_w=3, tile_h=3,
    tile_padding_w=1, tile_padding_h=1,
    chr_fill_tile_padding="."
)

board = Board(6, 5, class_tile=XmasTile, default_renderer=renderer)

BOARD_MAP = """
 F---7
F+7  |
||   |
L----J
"""

board_map = BOARD_MAP.replace("\n", "")

for tile, char_roadful in zip(board, board_map):
    tile.dirs_from_input(char_roadful)


def pass_through_xmas(tile_source, tile_dest):
    dir_ = compute_direction(tile_source, tile_dest)
    roads_to_check = {
        Dir.UP: (Dir.UP, Dir.DOWN),
        Dir.DOWN: (Dir.DOWN, Dir.UP),
        Dir.LEFT: (Dir.LEFT, Dir.RIGHT),
        Dir.RIGHT: (Dir.RIGHT, Dir.LEFT),
    }
    road_to_check = roads_to_check.get(dir_)
    if road_to_check is None:
        # Not supposed to happen
        return False
    road_source, road_dest = road_to_check
    return tile_source.roads[road_source] and tile_dest.roads[road_dest]


for index, tile in enumerate(
    board.get_by_pathfinding((0, 3), (2, 0), pass_through_xmas)
):
    tile.mid_marker = str(index)


print(board.render())

expected_result = """

   .   .   .   .   .
   . 4-.-5-.- -.- -.-
   . | .   .   .   . |
.......................
   . | .   .   .   . |
 2-.-3-.-  .   .   .
 | . | . | .   .   . |
.......................
 | . | .   .   .   . |
 1 .   .   .   .   .
 | . | .   .   .   . |
.......................
 | .   .   .   .   . |
 0-.- -.- -.- -.- -.-
   .   .   .   .   .
.......................
   .   .   .   .   .
   .   .   .   .   .
   .   .   .   .   .

"""
