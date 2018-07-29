# -*- coding: UTF-8 -*-

from my_log import debug, answer, log
from tile import Tile
from board_renderer import BoardRenderer


class Board():

	# TODO : on devrait pouvoir spécifier juste une classe héritée de Tile. Sans lambda.
	def __init__(
		self,
		w=1, h=1,
		tile_generator=lambda x, y: Tile(x, y),
		default_renderer=BoardRenderer(),
	):

		self.w = w
		self.h = h
		self._default_renderer = default_renderer

		self._tiles = [
			[ tile_generator(x, y) for x in range(w) ]
			for y in range(h)
		]
		self._default_renderer = BoardRenderer()


	# TODO : faut pos, tuple et x, y
	def get_tile(self, x, y):
		return self._tiles[y][x]


	def _render_tile(self, tile):
		pass


	def render(self, renderer=None):
		if renderer is None:
			renderer = self._default_renderer
		return renderer.render(self)


# ----------------- tests ------------------
# TODO : mettre ça dans des fichiers pytest

board = Board(8, 2)
log(board.render())

class MyTile(Tile):

	def init(self, arg_1=0, arg_2=2):
		self.arg_1 = arg_1
		self.arg_2 = arg_2

	def render(self, w=1, h=1):
		return self.arg_1+self.arg_2


my_tile = MyTile()
my_tile.init(3, 4)
log(my_tile.render())


class MyTileTellCoords(Tile):

	def render(self, w=1, h=1):
		if (w, h) == (1, 1):
			return hex(self.x * self.y)[2:].upper()
		else:
			return [
				'',
				' ' + str(self.x) + ',' + str(self.y),
				self.x * self.y
			]


board = Board(7, 4, lambda x, y: MyTileTellCoords(x, y))
tile = board.get_tile(0, 0)
log(tile.render())

my_board_renderer = BoardRenderer(
	tile_w=5, tile_h=4,
	tile_padding_w=3, tile_padding_h=2,
	chr_fill_tile='.', chr_fill_tile_padding='#',
)

log(my_board_renderer._render_tile(tile))
log('')
log(board.render())
log('')
log(board.render(my_board_renderer))
log('')

log("End")

