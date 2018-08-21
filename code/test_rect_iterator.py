# -*- coding: UTF-8 -*-

from positions_iterator import RectIterator


def test_simple_iteration():

	slice_x = slice(1, 13, 3)
	slice_y = slice(15, 135, 30)

	positions_check = [
		(1, 15), (4, 15), (7, 15), (10, 15),
		(1, 45), (4, 45), (7, 45), (10, 45),
		(1, 75), (4, 75), (7, 75), (10, 75),
		(1, 105), (4, 105), (7, 105), (10, 105),
	]

	for point_elem in RectIterator(slice_x, slice_y):
		print(point_elem)
		position_check = positions_check.pop(0)
		assert point_elem == position_check

