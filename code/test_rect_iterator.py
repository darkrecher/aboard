# -*- coding: UTF-8 -*-

from positions_iterator import RectIterator, Coord


def test_simple_iteration_main_x():

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

	assert positions_check == []


def test_simple_iteration_main_y():

	slice_x = slice(1, 13, 3)
	slice_y = slice(15, 135, 30)

	positions_check = [
		(1, 15), (1, 45), (1, 75), (1, 105),
		(4, 15), (4, 45), (4, 75), (4, 105),
		(7, 15), (7, 45), (7, 75), (7, 105),
		(10, 15), (10, 45), (10, 75), (10, 105),
	]

	for point_elem in RectIterator(slice_x, slice_y, Coord.Y):
		print(point_elem)
		position_check = positions_check.pop(0)
		assert point_elem == position_check

	assert positions_check == []


def test_jumps_and_dir_changes_1():

	slice_x = slice(5)
	slice_y = slice(3)
	rect_iter = RectIterator(slice_x, slice_y)

	for point_elem in rect_iter:
		print(point_elem)
		if point_elem == (0, 0):
			assert rect_iter.jumped == True
			assert rect_iter.changed_direction == False
		elif point_elem == (1, 0):
			assert rect_iter.jumped == False
			assert rect_iter.changed_direction == False
		elif point_elem.x == 0:
			assert rect_iter.jumped == True
			assert rect_iter.changed_direction == True
		elif point_elem.x == 1:
			assert rect_iter.jumped == False
			assert rect_iter.changed_direction == True
		else:
			assert rect_iter.jumped == False
			assert rect_iter.changed_direction == False



