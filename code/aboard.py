# -*- coding: UTF-8 -*-

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


# ----------------- tests des trucs en cours ------------------
# (à mettre dans des fichiers test_xxx.py au fur et à mesure que ça marche)

def main():
	from my_log import debug, answer, log
	log('Hellow')


	log('End')


if __name__ == '__main__':
	main()
