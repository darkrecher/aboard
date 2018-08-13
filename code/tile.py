# -*- coding: UTF-8 -*-


class Tile():

	def __init__(self, x=None, y=None):
		# TODO : Point !
		self.x = x
		self.y = y
		self.data = '.'


	def render(self, w=1, h=1):
		return str(self.data)[:w]

