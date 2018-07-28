# -*- coding: UTF-8 -*-

from my_log import debug, answer, log


class Tile():

	def __init__(self, x=None, y=None):
		self.init()


	def init(self):
		pass


	def render(self, w=1, h=1):
		return '.'


class Board():

	def __init__(self, w=1, h=1, tile_generator=lambda x, y: Tile(x, y)):

		self.w = w
		self.h = h
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

	def render(self):
		# TODO : permettre un autre renderer que le default.
		return self._default_renderer.render(self)


class BoardRenderer():

	def __init__(
		self,
		tilepadding_vertic=0, tilepadding_horiz=0,
		tile_w=1, tile_h=1,
		border_vertic=False, border_horiz=True
	):
		self.tilepadding_vertic = tilepadding_vertic
		self.tilepadding_horiz = tilepadding_horiz
		self.tile_w = tile_w
		self.tile_h = tile_h
		self.border_vertic = border_vertic
		self.border_horiz = border_horiz


	def render(self, board):
		# TODO : utiliser un itérateur de Board
		render_result = ''
		for y in range(board.h):
			line = ''
			for x in range(board.w):
				line += board.get_tile(x, y).render()
			render_result += line + '\n'

		return render_result


# tests


class MyTile(Tile):

	def init(self, arg_1=0, arg_2=2):
		self.arg_1 = arg_1
		self.arg_2 = arg_2

	def render(self, w=1, h=1):
		return self.arg_1+self.arg_2


my_tile = MyTile()
my_tile.init(3, 4)
log(my_tile.render())


board = Board(7, 4)
tile = board.get_tile(0, 0)
log(tile.render())
log('')

log(board.render())

log('')
log("End")

