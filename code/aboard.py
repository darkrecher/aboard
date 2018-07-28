# -*- coding: UTF-8 -*-

from my_log import debug, answer, log


class Tile():

	def __init__(self, x=None, y=None):
		self.x = x
		self.y = y
		self.init()


	def init(self):
		pass


	def render(self, w=1, h=1):
		return '.'


class Board():

	# TODO : on devrait pouvoir spécifier juste une classe héritée de Tile. Sans lambda.
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
		tilepadding_w=0, tilepadding_h=0,
		tile_w=1, tile_h=1,
		border_vertic=False, border_horiz=True,
		chr_fill_padding=' ',
		chr_fill_tile=' ', word_wrap=False
	):
		self.tilepadding_w = tilepadding_w
		self.tilepadding_h = tilepadding_h
		self.tile_w = tile_w
		self.tile_h = tile_h
		self.border_vertic = border_vertic
		self.border_horiz = border_horiz
		self.chr_fill_padding = chr_fill_padding
		self.chr_fill_tile = chr_fill_tile
		self.word_wrap = word_wrap


	def _str_resized(self, value):
		w = self.tile_w
		return str(value).ljust(w, self.chr_fill_tile)[:w]


	def _render_tile(self, tile):
		"""
		Renvoie une liste de tile_h string, chacune ayant une taille tile_w.
		"""
		if self.word_wrap:
			raise NotImplemented("TODO")

		tile_res = tile.render(self.tile_h, self.tile_w)

		if isinstance(tile_res, str):
			process_as_string = True
		else:
			try:
				_ = iter(tile_res)
				process_as_string = False
			except TypeError:
				process_as_string = True

		if process_as_string:
			lines = [ self._str_resized(tile_res) ]
		else:
			lines = []
			for index, line in enumerate(tile_res):
				if index >= self.tile_h:
					break
				lines.append(self._str_resized(line))

		last_lines = [ self.chr_fill_tile*self.tile_w ] * (self.tile_h - 1)
		return lines + last_lines


	def render_iter_lines(self, board):
		# TODO : utiliser un itérateur de Board
		render_result = ''
		interval_tile_w = self.chr_fill_padding * self.tilepadding_w
		interval_line_h = interval_tile_w.join((
			[ self.chr_fill_padding*self.tile_w ] * board.w
		))

		for y in range(board.h):

			rendered_tiles = [
				self._render_tile(board.get_tile(x, y))
				for x in range(board.w)
			]

			for index_line in range(self.tile_h):

				yield interval_tile_w.join((
					rendered_tiles[x][index_line]
					for x in range(board.w)
				))

			if y < board.h-1:
				for index_interval in range(self.tilepadding_h):
					yield interval_line_h


	def render(self, board):
		return '\n'.join(self.render_iter_lines(board))


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


class MyTileTellCoords(Tile):

	def render(self, w=1, h=1):
		return [
			'',
			str(self.x) + ',' + str(self.y),
			self.x * self.y
		]


board = Board(7, 4, lambda x, y: MyTileTellCoords(x, y))
tile = board.get_tile(0, 0)
log(tile.render())

board_renderer = BoardRenderer(
	tile_w=5, tile_h=4,
	tilepadding_w=3, tilepadding_h=2,
	chr_fill_tile='.', chr_fill_padding='#',
)

log(board_renderer._render_tile(tile))
log('')
log(board_renderer.render(board))
log('')

log("End")

