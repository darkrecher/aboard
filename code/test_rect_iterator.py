# -*- coding: UTF-8 -*-

from point import Point
from aboard import Board
from positions_iterator import BoardIteratorRect, Coord


def test_simple_iteration_main_x():

	board = Board(120, 120)
	slice_x = slice(1, 13, 3)
	slice_y = slice(15, 135, 30)

	positions_check = [
		(1, 15), (4, 15), (7, 15), (10, 15),
		(1, 45), (4, 45), (7, 45), (10, 45),
		(1, 75), (4, 75), (7, 75), (10, 75),
		(1, 105), (4, 105), (7, 105), (10, 105),
	]

	for tile in BoardIteratorRect(board, slice_x, slice_y):
		# TODO : choper direct le point à partir de la tile, quand ce sera possible.
		point = Point(tile.x, tile.y)
		print(point)
		position_check = positions_check.pop(0)
		assert point == position_check

	assert positions_check == []


def test_simple_iteration_main_y():

	board = Board(120, 120)
	slice_x = slice(1, 13, 3)
	slice_y = slice(15, 135, 30)

	positions_check = [
		(1, 15), (1, 45), (1, 75), (1, 105),
		(4, 15), (4, 45), (4, 75), (4, 105),
		(7, 15), (7, 45), (7, 75), (7, 105),
		(10, 15), (10, 45), (10, 75), (10, 105),
	]

	for tile in BoardIteratorRect(board, slice_x, slice_y, Coord.Y):
		# TODO : choper direct le point à partir de la tile, quand ce sera possible.
		point = Point(tile.x, tile.y)
		print(point)
		position_check = positions_check.pop(0)
		assert point == position_check

	assert positions_check == []


def test_jumps_and_dir_changes():

	board = Board(10, 10)
	slice_x = slice(5)
	slice_y = slice(3)
	rect_iter = BoardIteratorRect(board, slice_x, slice_y)

	for tile in rect_iter:
		# TODO : choper direct le point à partir de la tile, quand ce sera possible.
		point = Point(tile.x, tile.y)
		print(point)
		if point == (0, 0):
			assert rect_iter.jumped == True
			assert rect_iter.changed_direction == False
			assert rect_iter.both_coord_changed == True
		elif point == (1, 0):
			assert rect_iter.jumped == False
			assert rect_iter.changed_direction == False
			assert rect_iter.both_coord_changed == False
		elif point.x == 0:
			assert rect_iter.jumped == True
			assert rect_iter.changed_direction == True
			assert rect_iter.both_coord_changed == True
		elif point.x == 1:
			assert rect_iter.jumped == False
			assert rect_iter.changed_direction == True
			assert rect_iter.both_coord_changed == False
		else:
			assert rect_iter.jumped == False
			assert rect_iter.changed_direction == False
			assert rect_iter.both_coord_changed == False


def test_skip_lines():

	# TODO
	assert False

	slice_x = slice(5)
	slice_y = slice(3)
	rect_iter = RectIterator(slice_x, slice_y)
	# TODO : il faut vérifier qu'on puisse faire un skip_line dès le départ. Même si on n'a pas commencé d'itérer.


	for point_elem in rect_iter:
		pass
