# -*- coding: UTF-8 -*-

from position import Pos


class AdjacencyEvaluator:
    def __init__(self, board):
        self.board = board

    def is_adjacent(self, pos_1, pos_2):
        raise NotImplemented

    def adjacent_tiles(self, pos):
        raise NotImplemented


class AdjacencyEvaluatorCross(AdjacencyEvaluator):
    def is_adjacent(self, pos_1, pos_2):
        if pos_1.x == pos_2.x:
            return pos_1.y - pos_2.y in (-1, 1)
        if pos_1.y == pos_2.y:
            return pos_1.x - pos_2.x in (-1, 1)
        return False

    def adjacent_positions(self, pos):
        # Il est conseillé de mettre dans le même ordre que l'ordre des Direction.
        # C'est à dire dans le sens des aiguilles d'une montre.
        # (Mais ce n'est pas tout le temps possible avec des fonctions d'adjacences tordues)
        offsets = [(0, -1), (+1, 0), (0, +1), (-1, 0)]
        for offset in offsets:
            x = pos.x + offset[0]
            y = pos.y + offset[1]
            # TODO : le check de inbounds devrait être dans la classe board, tellement c'est un truc basique.
            if (0 <= x < self.board.w) and (0 <= y < self.board.h):
                yield Pos(x, y)


class AdjacencyEvaluatorCrossDiag(AdjacencyEvaluator):
    def is_adjacent(self, pos_1, pos_2):
        abs_diff_x = abs(pos_1.x - pos_2.x)
        abs_diff_y = abs(pos_1.y - pos_2.y)
        return (
            (abs_diff_x, abs_diff_y) != (0, 0) and abs_diff_x <= 1 and abs_diff_y <= 1
        )

    def adjacent_positions(self, pos):
        # Il est conseillé de mettre dans le même ordre que l'ordre des Direction.
        # C'est à dire dans le sens des aiguilles d'une montre.
        # (Mais ce n'est pas tout le temps possible avec des fonctions d'adjacences tordues)
        offsets = [
            (0, -1),
            (+1, -1),
            (+1, 0),
            (+1, +1),
            (0, +1),
            (-1, +1),
            (-1, 0),
            (-1, -1),
        ]
        for offset in offsets:
            x = pos.x + offset[0]
            y = pos.y + offset[1]
            # TODO : le check de inbounds devrait être dans la classe board, tellement c'est un truc basique.
            if (0 <= x < self.board.w) and (0 <= y < self.board.h):
                yield Pos(x, y)


# TODO : les adjacences toriques. Avec les tests qui vont bien.
# TODO : tester les fonctions adjacent_positions.
# FUTURE : un itérateur qui renvoie des None sur les positions adjacentes pas valides. (je sais pas si on en aura besoin)


class_default_adjacency = AdjacencyEvaluatorCross


def set_default_adjacency(new_class_default_adjacency):
    global class_default_adjacency
    class_default_adjacency = new_class_default_adjacency


def get_default_adjacency():
    global class_default_adjacency
    return class_default_adjacency
