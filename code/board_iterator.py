# -*- coding: UTF-8 -*-


#from positions_iterator import PositionsIterator

class BoardIterator():

	def __init__(self, board, positions_iterator):
		self.board = board
		self.positions_iterator = positions_iterator


	def __iter__(self):
		return self


	def __next__(self):

		# Ça va éventuellement raiser StopIteration. On laisse faire.
		current_point = next(self.positions_iterator)

		return self.board.get_tile(current_point.x, current_point.y)


# ----------------- tests des trucs en cours ------------------
# (à mettre dans des fichiers test_xxx.py au fur et à mesure que ça marche)

def main():

	from aboard import Board
	from board_renderer import BoardRenderer
	from positions_iterator import PositionsIterator

	positions = [
		(1, 2), (1, 3), (1, 4),
		(2, 4), (3, 4), (5, 4), (6, 4),
		(9, 0) ]


	board = Board(10, 6)
	board_iterator = BoardIterator(
		board,
		PositionsIterator(positions))

	for index, point in enumerate(board_iterator):
		point.data = index

	render_result = """

	.........7
	..........
	.0........
	.1........
	.234.56...
	..........

	"""

	assert board.render() == strip_multiline(render_result)


	my_board_renderer = BoardRenderer(tile_w=2, tile_padding_w=1, tile_padding_h=1, chr_fill_tile='.')
	board = Board(10, 6, default_renderer=my_board_renderer)
	board_iterator = BoardIterator(
		board,
		PositionsIterator(positions))

	for index, point in enumerate(board_iterator):
		DICT_JUMP_DIR = {
			(False, False): '_',
			(True, False): 'J',
			(False, True): 'D',
			(True, True): 'X',
		}
		point.data = str(index) + DICT_JUMP_DIR[ (board_iterator.positions_iterator.jumped, board_iterator.positions_iterator.changed_direction) ]

	print(board.render())


if __name__ == '__main__':
	main()