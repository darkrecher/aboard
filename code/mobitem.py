
from point import Point


class MobileItem():

	def __init__(self, board_owner, pos_param_1=None, pos_param_2=None, x=None, y=None):
		self.board_owner = board_owner
		self.data = '#'
		self.pos = Point(pos_param_1, pos_param_2, x, y)




