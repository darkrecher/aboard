# -*- coding: UTF-8 -*-

from point import (
	Point,
	is_adjacent, set_default_adjacency, is_adjacent_diag,
	Direction)


class Positions():

	def __init__(
		self,
		posis,
		step=1,
		tell_jumps=False,
		tell_direction_changes=False,
		sliding_window=None,
		continuous_sliding_window=None,
		adjacency=None,
	):

		# jump : la coord précédente n'est pas adjacente
		# dir_change, la direction entre :
		#   (la coord précédente-précédente et la coord précédente)
		#   (la coord précédente et l'actuelle)
		# sont différentes.
		# Du coup, pour le jump, il faut se poser la question du type d'adjacence.
		# Diagonale ou pas diagonale ?

		# posis peut contenir des ellipsis.
		self.posis = posis
		self.step = step
		if self.step > 0:
			self.next_index = 0
		elif self.step < 0:
			self.next_index = len(self.posis) - 1
		else:
			raise ValueError("Le step doit être différent de 0.")

		self.is_adjacent = adjacency or is_adjacent
		self.current_point = None
		self.prev_point = None
		self.prev_prev_point = None
		self.jumped = True
		self.changed_direction = False

	#def pouet(
	#	self, sense='┌ ┐ └ ┘', tell_prime_coord_change=False,
	#	skip_lines=None, rect=None, poses=None,
	#	sliding_window=None, continuous_sliding_window=None
	#):
	#	pass

	def __iter__(self):
		return self


	def __next__(self):

		if self.next_index <= -1 or self.next_index >= len(self.posis):
			raise StopIteration

		self.prev_prev_point = self.prev_point
		self.prev_point = self.current_point
		self.current_point = Point(self.posis[self.next_index])

		self.jumped = (
			self.prev_point is None
			or self.is_adjacent(self.prev_point, self.current_point))



		self.next_index += self.step
		return self.current_point


	def skip(self):
		pass


class Rect(Positions):
	pass


# ----------------- tests des trucs en cours ------------------

def main():

	p = Positions(((1, 2), (3, 4), (5, 6), (7, 8)))

	for elem in p:
		print(elem)

	p1 = Point(5, 5)
	p2 = Point(6, 5)
	p3 = Point(4, 4)

	set_default_adjacency(is_adjacent_diag)

	print('same : ', is_adjacent(p1, p1))
	print('cross: ', is_adjacent(p1, p2))
	print('diag : ', is_adjacent(p1, p3))
	print('none : ', is_adjacent(p2, p3))


if __name__ == '__main__':
	main()
