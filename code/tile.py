# -*- coding: UTF-8 -*-

from my_log import debug, answer, log


class Tile():

	def __init__(self, x=None, y=None):
		self.x = x
		self.y = y
		self.init()


	def init(self):
		pass


	def render(self, w=1, h=1):
		return '.'

