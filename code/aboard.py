# -*- coding: UTF-8 -*-


from coord import Coord
from direction import Dir
from position import Pos, compute_direction
from adjacency import (
    get_default_adjacency,
    set_default_adjacency,
    AdjacencyEvaluator,
    AdjacencyEvaluatorCross,
    AdjacencyEvaluatorCrossDiag,
)
from tile import Tile
from board_renderer import BoardRenderer
from positions_iterator import BoardIteratorPositions, BoardIteratorRect
from iter_indicators import IterIndicator
from propagation_iterator import (
    propag_cond_default,
    BoardIteratorPropagation,
    BoardIteratorFindPath,
)

ItInd = IterIndicator


class BoardIndexError(IndexError):
    pass


class Board:

    # TODO : une fonction qui trouve un chemin passant par toutes les positions d'un
    # ensemble donné. (Si c'est possible).
    # Pour résoudre des problèmes "genre 4 elements".

    def __init__(
        self,
        w=1,
        h=1,
        class_tile=Tile,
        default_renderer=BoardRenderer(),
        class_adjacency=None,
    ):
        self.w = w
        self.h = h
        self._default_renderer = default_renderer

        self.class_adjacency = (
            class_adjacency if class_adjacency is not None else get_default_adjacency()
        )

        self.adjacency = self.class_adjacency(self)
        self.is_adjacent = self.adjacency.is_adjacent

        self._tiles = [[class_tile(x, y, self) for x in range(w)] for y in range(h)]

    def _get_tile(self, x, y):
        try:
            return self._tiles[y][x]
        except IndexError:
            msg = "Coord not in board. coord : %s, %s. board size : %s, %s."
            data = (x, y, self.w, self.h)
            raise BoardIndexError(msg % data)

    def get_tile(self, *args, **kwargs):
        pos = Pos(*args, **kwargs)
        return self._get_tile(pos.x, pos.y)

    def __getitem__(self, args):
        # FUTURE : on a le droit de faire du *args, **kwargs avec getitem ?
        # Et ça donne quoi si on le fait ? À tester.

        if not args:
            return BoardIteratorRect(self)

        try:
            pos = Pos(args)
        except ValueError:
            pos = None

        if pos is not None:
            # Mode un seul élément
            return self._get_tile(pos.x, pos.y)

        slice_x = None
        slice_y = None
        id_coord_main = Coord.X

        try:
            iter_on_args = iter(args)
            slice_x = next(iter_on_args)
            slice_y = next(iter_on_args)
            id_coord_main = next(iter_on_args)
        except TypeError:
            slice_x = args
        except StopIteration:
            pass

        if (
            slice_x is None
            or slice_y is None
            or isinstance(slice_x, slice)
            or isinstance(slice_y, slice)
        ):

            # Mode itération
            if slice_x is None:
                slice_x = slice(None, None, None)
            if isinstance(slice_x, int):
                slice_x = slice(slice_x, slice_x + 1, None)

            if slice_y is None:
                slice_y = slice(None, None, None)
            if isinstance(slice_y, int):
                slice_y = slice(slice_y, slice_y + 1, None)

            dict_coord_from_str = {"X": Coord.X, "Y": Coord.Y}
            if isinstance(id_coord_main, str):
                id_coord_main = id_coord_main.upper()
                if id_coord_main in dict_coord_from_str:
                    id_coord_main = dict_coord_from_str[id_coord_main]

            return BoardIteratorRect(self, slice_x, slice_y, id_coord_main)

            # Mode fail
        raise Exception("TODO fail get item" + "".join(args))

    def __iter__(self):
        return BoardIteratorRect(self)

    def render(self, renderer=None):
        if renderer is None:
            renderer = self._default_renderer
        return renderer.render(self)

    def iter_positions(self, positions):
        return BoardIteratorPositions(self, positions)

    def get_by_propagation(self, pos_start, propag_condition=propag_cond_default):
        return BoardIteratorPropagation(self, pos_start, propag_condition)

    def get_by_pathfinding(
        self, pos_start, pos_end, pass_through_condition=propag_cond_default
    ):
        return BoardIteratorFindPath(self, pos_start, pos_end, pass_through_condition)

    def set_data_from_string(self, data_lines, sep_line=None, sep_tiles=None):

        if sep_line is not None:
            data_lines = data_lines.split(sep_line)
        board_iter = BoardIteratorRect(self).group_by_subcoord()

        for data_line, board_line in zip(data_lines, board_iter):
            if sep_tiles is not None:
                data_line = data_line.split(sep_tiles)
            for data_tile, tile in zip(data_line, board_line):
                tile.data = data_tile

                # TODO : Il faut des itérateur de positions avec des ellipsis.
                # Genre : (1, 2), ... ,(5, 2), (1, 3), ..., (6, 3),

    def replace_tile(self, new_tile, pos):
        new_tile.pos = Pos(pos)
        new_tile.x = pos.x
        new_tile.y = pos.y
        self._tiles[pos.y][pos.x] = new_tile

    def circular_permute_tiles(self, positions):
        """
		positions est un itérable.
		"""

        made_first_iteration = False

        for pos in positions:
            if made_first_iteration:
                cur_pos = pos
                cur_tile = self._tiles[cur_pos.y][cur_pos.x]
                cur_tile.pos = Pos(prev_pos)
                cur_tile.x = prev_pos.x
                cur_tile.y = prev_pos.y
                self._tiles[prev_pos.y][prev_pos.x] = cur_tile
                prev_pos = cur_pos
            else:
                first_pos = pos
                first_tile = self._tiles[first_pos.y][first_pos.x]
                prev_pos = first_pos
                made_first_iteration = True

        first_tile.pos = Pos(pos)
        first_tile.x = pos.x
        first_tile.y = pos.y
        self._tiles[pos.y][pos.x] = first_tile
