# -*- coding: UTF-8 -*-


from tile import Tile


def test_the_tester_itself():
	assert True


def test_base_tile():
	tile = Tile()
	assert tile.render() == '.'


def test_inherited_tile():

	class MyTile(Tile):

		def init(self, arg_1=0, arg_2=2):
			self.arg_1 = arg_1
			self.arg_2 = arg_2

		def render(self, w=1, h=1):
			return self.arg_1 + self.arg_2

	my_tile = MyTile()
	my_tile.init(3, 4)
	# Donc là, ça nous fait 3 + 4 = 7
	assert my_tile.render() == 7
