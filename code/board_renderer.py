# -*- coding: UTF-8 -*-

from my_log import debug, answer, log
from tile import Tile


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
		tile_res = tile.render(self.tile_w, self.tile_h)

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
