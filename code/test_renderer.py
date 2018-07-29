# -*- coding: UTF-8 -*-

from aboard import Tile, Board, BoardRenderer


def test_basic_board():
	board = Board()
	assert board.render() == '.'


def test_sized_board():
	board = Board(8, 2)
	# 2 lignes, constituées de 8 points chacune.
	# Un saut de ligne entre les deux, mais pas à la fin.
	assert board.render() == '........\n........'


class MyTileTellCoords(Tile):

	def render(self, w=1, h=1):
		if (w, h) == (1, 1):
			return hex(self.x * self.y)[2:].upper()
		else:
			return [
				'',
				'_' + str(self.x) + ',' + str(self.y),
				# Attention, ici on ne met pas une string, mais un int.
				# C'est fait exprès. Et ça doit quand même fonctionner.
				self.x * self.y
			]


def strip_multiline(multi_string):
	# J'ai besoin de cette fonction juste pour pouvoir présenter
	# les strings d'une manière plus lisible.
	return '\n'.join([
		line.strip()
		for line in multi_string.strip().split()
	])


def test_multiline_stripper():
	multi_string = """
	abcd
	1234567
	"""
	assert strip_multiline(multi_string) == 'abcd\n1234567'


def test_basic_renderer():
	board = Board(7, 4, lambda x, y: MyTileTellCoords(x, y))
	render_result = """

	0000000
	0123456
	02468AC
	0369CF1

	"""
	assert board.render() == strip_multiline(render_result)


def test_padded_renderer():
	my_board_renderer = BoardRenderer(
		tile_w=5, tile_h=4,
		tile_padding_w=3, tile_padding_h=2,
		chr_fill_tile='.', chr_fill_tile_padding='#',
	)
	board = Board(7, 4, lambda x, y: MyTileTellCoords(x, y))
	render_result = """

	.....###.....###.....###.....###.....###.....###.....
	_0,0.###_1,0.###_2,0.###_3,0.###_4,0.###_5,0.###_6,0.
	0....###0....###0....###0....###0....###0....###0....
	.....###.....###.....###.....###.....###.....###.....
	#####################################################
	#####################################################
	.....###.....###.....###.....###.....###.....###.....
	_0,1.###_1,1.###_2,1.###_3,1.###_4,1.###_5,1.###_6,1.
	0....###1....###2....###3....###4....###5....###6....
	.....###.....###.....###.....###.....###.....###.....
	#####################################################
	#####################################################
	.....###.....###.....###.....###.....###.....###.....
	_0,2.###_1,2.###_2,2.###_3,2.###_4,2.###_5,2.###_6,2.
	0....###2....###4....###6....###8....###10...###12...
	.....###.....###.....###.....###.....###.....###.....
	#####################################################
	#####################################################
	.....###.....###.....###.....###.....###.....###.....
	_0,3.###_1,3.###_2,3.###_3,3.###_4,3.###_5,3.###_6,3.
	0....###3....###6....###9....###12...###15...###18...
	.....###.....###.....###.....###.....###.....###.....

	"""
	assert board.render(my_board_renderer) == strip_multiline(render_result)

