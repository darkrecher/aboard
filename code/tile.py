# -*- coding: UTF-8 -*-

from position import Pos


class Tile:
    def __init__(self, x=None, y=None, board_owner=None):
        # TODO : il faut accepter le même bazar de param que pour l'objet Pos. Ou pas.
        self.x = x
        self.y = y
        # TODO : est-ce qu'on autorise des tiles sans coord, qui "flotte un peu dans les airs", ou pas ?
        try:
            self.pos = Pos(x, y)
        except:
            self.pos = None
        self.board_owner = board_owner
        self.data = "."
        self.mobile_items = []

    def __str__(self):
        return "<Tile (%s, %s): %s>" % (self.x, self.y, self.data)

    def __repr__(self):
        return str(self)

    def render(self, w=1, h=1):
        return self.data

    def __eq__(self, other):
        return self.data == other.data

        # TODO : pas testé.

    def is_adjacent(self, other):
        if self.board_owner is None:
            raise Exception("board_owner must be defined.")
            # Ça va raiser des exceptions si le board_owner n'est pas comme il faut
            # Osef, c'est ce qu'on veut.
        return self.board_owner.is_adjacent(self, other)
