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


class BoardRenderer():

	AUTHORIZED_ATTRIBUTES = {
		'tile_w': 1, 'tile_h': 1, 'chr_fill_tile': ' ',
		'word_wrap': False,
		'tile_padding_w': 0, 'tile_padding_h': 0,
		'chr_fill_tile_padding': ' ',
		'tile_border_vertic': False, 'tile_border_horiz': False,
		'chr_tile_border_vertic': '|', 'chr_tile_border_horiz': '-',
		'chr_tile_border_cross': '+',
		'deduce_board_style_from_tile_style': False,
		'board_padding_w': 0, 'board_padding_h': 0,
		'chr_fill_board_padding': ' ',
		'board_border_vertic': False, 'board_border_horiz': False,
		'chr_board_border_vertic': '|', 'chr_board_border_horiz': '-',
		'chr_board_border_cross': '+',
	}

	NOT_IMPLEMENTED = [
		'word_wrap',
		'tile_border_vertic', 'tile_border_horiz',
		'chr_tile_border_vertic', 'chr_tile_border_horiz',
		'chr_tile_border_cross',
		'deduce_board_style_from_tile_style',
		'board_padding_w', 'board_padding_h',
		'chr_fill_board_padding',
		'board_border_vertic', 'board_border_horiz',
		'chr_board_border_vertic', 'chr_board_border_horiz',
		'chr_board_border_cross',
	]

	def __init__(self, **kwargs):

		for key_attr in kwargs:
			if key_attr not in BoardRenderer.AUTHORIZED_ATTRIBUTES:
				raise ValueError("Paramètre inconnu : " + key_attr)
			if key_attr in BoardRenderer.NOT_IMPLEMENTED:
				raise ValueError("TODO : " + key_attr)

		dict_attrs = dict(BoardRenderer.AUTHORIZED_ATTRIBUTES)
		dict_attrs.update(kwargs)
		for key_attr, val_attr in dict_attrs.items():
			setattr(self, key_attr, val_attr)


	def _str_resized(self, value):
		w = self.tile_w
		return str(value).ljust(w, self.chr_fill_tile)[:w]


	def _render_tile(self, tile):
		"""
		Renvoie une liste de tile_h string, chacune ayant une taille tile_w.
		"""
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
		interval_tile_w = self.chr_fill_tile_padding * self.tile_padding_w
		interval_line_h = interval_tile_w.join((
			[ self.chr_fill_tile_padding*self.tile_w ] * board.w
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
				for index_interval in range(self.tile_padding_h):
					yield interval_line_h


	def render(self, board):
		return '\n'.join(self.render_iter_lines(board))


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

# tests

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

