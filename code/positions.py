# -*- coding: UTF-8 -*-


class Positions():

	def __init__(
		self,
		posis,
		step=1,
		tell_jumps=False,
		tell_direction_changes=False,
		sliding_window=None,
		continuous_sliding_window=None,
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
		if self.step > 0:
			self.index = 0
		elif self.step < 0:
			self.index = len(posis) - 1

		self.prev_point = None

	#def pouet(
	#	self, sense='┌ ┐ └ ┘', tell_prime_coord_change=False,
	#	skip_lines=None, rect=None, poses=None,
	#	sliding_window=None, continuous_sliding_window=None
	#):
	#	pass

	def __iter__(self):
		return self

	def __next__(self):

		if not self.poses:
			raise StopIteration

		return self.poses.pop(0)

	def skip(self):

		if self.poses:
			self.poses.pop(0)


class Rect(Positions):
	pass

# ----------------- tests des trucs en cours ------------------

def main():

	p = Positions()

	for elem in p:
		print(elem)

	print('-' * 20)

	p2 = Positions()

	for elem in p2:
		if elem in (2, 91):
			p2.skip()
			p2.skip()
		print(elem)


if __name__ == '__main__':
	main()
