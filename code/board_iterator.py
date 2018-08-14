# -*- coding: UTF-8 -*-


class BoardIterator():

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


# ----------------- tests des trucs en cours ------------------
# (à mettre dans des fichiers test_xxx.py au fur et à mesure que ça marche)

def main():
	pass


if __name__ == '__main__':
	main()