# -*- coding: UTF-8 -*-

from position import Pos


class Tile:
    """
    Une case / tuile d'un board.
    On peut lui ajouter les attributs que l'on veut, la faire hériter, etc.
    Un board contient un tableau de deux dimensions. Chaque élément
    de ce tableau est une instance de Tile.

    attributs :

    board_owner : Le Board dans lequel se trouve la Tile.
    x, y : deux entiers. Coordonnées de cette Tile, dans son board_owner.
    pos : Position. La position (x, y) de cette Tile dans son board_owner.
    data : Objet quelconque, string-isable avec la fonction str().
           C'est cette attribut qui sera utilisé lorsqu'on fera
           un rendu du board_owner (fonction render()).
    mobile_items : inutilisé pour l'instant.
    """

    def __init__(self, x=None, y=None, board_owner=None):
        """
        Les paramètres x, y et board_owner sont fournis par l'objet Board,
        qui crée ses propres Tiles lors de son init.
        En théorie, rien n'empêche d'avoir des Tiles non associées à un Board,
        mais ça n'a pas été testé, et il est possible que certaines fonctions
        ne marchent pas (par exemple, toutes les règles d'adjacence).
        """
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
