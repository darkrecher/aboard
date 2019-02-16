# -*- coding: UTF-8 -*-

from position import Point


class Tile():

	def __init__(self, x=None, y=None, board_father=None):
		# TODO : il faut accepter le même bazar de param que pour l'objet Point. Ou pas.
		# TODO : renommer board_father en board_owner.
		self.x = x
		self.y = y
		# TODO : est-ce qu'on autorise des tiles sans coord, qui "flotte un peu dans les airs", ou pas ?
		try:
			self.point = Point(x, y)
		except:
			self.point = None
		self.board_father = board_father
		self.data = '.'
		self.mobile_items = []


	def __str__(self):
		return '<Tile (%s, %s): %s>' % (self.x, self.y, self.data)


	def render(self, w=1, h=1):
		return str(self.data)[:w]


	def __eq__(self, other):
		return self.data == other.data


	# TODO WIP pas testé.
	def is_adjacent(self, other):
		if self.board_father is None:
			raise Exception("board_father must be defined.")
		# Ça va raiser des exceptions si le board_father n'est pas comme il faut
		# Osef, c'est ce qu'on veut.
		return self.board_father.is_adjacent(self, other)
