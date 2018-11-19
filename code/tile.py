# -*- coding: UTF-8 -*-


class Tile():

	def __init__(self, x=None, y=None, board_father=None):
		# TODO : Point !
		self.x = x
		self.y = y
		self.board_father = board_father
		self.data = '.'


	def __str__(self):
		return '<Tile (%s, %s): %s>' % (self.x, self.y, self.data)


	def render(self, w=1, h=1):
		return str(self.data)[:w]


	# TODO WIP pas testé.
	def is_adjacent(self, other):
		if self.board_father is None:
			raise Exception("board_father must be defined.")
		# Ça va raiser des exceptions si le board_father n'est pas comme il faut
		# Osef, c'est ce qu'on veut.
		return self.board_father.is_adjacent(self, other)
