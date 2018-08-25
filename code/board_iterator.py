# -*- coding: UTF-8 -*-


# TODO : un board iterator générique. Puis un BoardPosIterator, et un BoardRectIterator.

class BoardPosIterator():

	def __init__(self, board, positions_iterator):
		self.board = board
		self.positions_iterator = positions_iterator
		self.jumped = self.positions_iterator.jumped
		self.changed_direction = self.positions_iterator.changed_direction


	def __iter__(self):
		return self


	def __next__(self):

		# Ça va éventuellement raiser StopIteration. On laisse faire.
		current_point = next(self.positions_iterator)
		self.jumped = self.positions_iterator.jumped
		self.changed_direction = self.positions_iterator.changed_direction

		return self.board.get_tile(current_point.x, current_point.y)



class BoardRectIterator():

	def __init__(self, board, rect_iterator):
		self.board = board
		self.rect_iterator = rect_iterator
		self.jumped = self.rect_iterator.jumped
		self.changed_direction = self.rect_iterator.changed_direction


	def __iter__(self):
		return self


	def __next__(self):

		# Ça va éventuellement raiser StopIteration. On laisse faire.
		current_point = next(self.rect_iterator)
		self.jumped = self.rect_iterator.jumped
		self.changed_direction = self.rect_iterator.changed_direction
		self.changed_sub_coord = self.rect_iterator.changed_sub_coord

		return self.board.get_tile(current_point.x, current_point.y)


# ----------------- tests des trucs en cours ------------------
# (à mettre dans des fichiers test_xxx.py au fur et à mesure que ça marche)

def main():
	pass

	from aboard import Board
	from board_renderer import BoardRenderer
	from positions_iterator import PositionsIterator, RectIterator
	from board_iterator import BoardPosIterator


	board = Board(10, 6)
	board_rect_iterator = BoardRectIterator(
		board,
		RectIterator(slice(3, 6), slice(1, 7, 2)))

	for index, point in enumerate(board_rect_iterator):
		point.data = index

	print(board.render())



if __name__ == '__main__':
	main()
