# -*- coding: UTF-8 -*-

from point import (
	Point, Dir,
	is_adjacent_cross, is_adjacent_diag, set_default_adjacency, is_adjacent,
	dir_from_str, compute_direction,
)


def test_adj_cross():

	p1 = Point(5, 5)
	p2 = Point(6, 5)
	p3 = Point(4, 4)

	# same :
	assert is_adjacent_cross(p1, p1) == False
	# cross :
	assert is_adjacent_cross(p1, p2) == True
	# diag :
	assert is_adjacent_cross(p1, p3) == False
	# none :
	assert is_adjacent_cross(p2, p3) == False


def test_adj_diag():

	p1 = Point(5, 5)
	p2 = Point(6, 5)
	p3 = Point(4, 4)

	# same :
	assert is_adjacent_diag(p1, p1) == False
	# cross :
	assert is_adjacent_diag(p1, p2) == True
	# diag :
	assert is_adjacent_diag(p1, p3) == True
	# none :
	assert is_adjacent_diag(p2, p3) == False


def test_adj_default():

	p1 = Point(5, 5)
	p2 = Point(6, 5)
	p3 = Point(4, 4)

	# cross:
	assert is_adjacent(p1, p2) == True
	# diag :
	assert is_adjacent(p1, p3) == False

	set_default_adjacency(is_adjacent_cross)
	# cross:
	assert is_adjacent(p1, p2) == True
	# diag :
	assert is_adjacent(p1, p3) == False

	set_default_adjacency(is_adjacent_diag)
	# cross:
	assert is_adjacent(p1, p2) == True
	# diag :
	assert is_adjacent(p1, p3) == True


def test_directions_equivalence():
	assert Dir.UP == Dir.U == Dir.NORTH == Dir.N == Dir.PAD_8 == dir_from_str('┬') == dir_from_str('↑') == dir_from_str('^')
	assert Dir.UP_RIGHT == Dir.UR == Dir.NORTH_EAST == Dir.NE == Dir.PAD_9 == dir_from_str('┐') == dir_from_str('↗')
	assert Dir.RIGHT == Dir.R == Dir.EAST == Dir.E == Dir.PAD_6 == dir_from_str('┤') == dir_from_str('→') == dir_from_str('>')
	assert Dir.DOWN_RIGHT == Dir.DR == Dir.SOUTH_EAST == Dir.SE == Dir.PAD_3 == dir_from_str('┘') == dir_from_str('↘')
	assert Dir.DOWN == Dir.D == Dir.SOUTH == Dir.S == Dir.PAD_2 == dir_from_str('┴') == dir_from_str('↓') == dir_from_str('V') == dir_from_str('v')
	assert Dir.DOWN_LEFT == Dir.DL == Dir.SOUTH_WEST == Dir.SW == Dir.PAD_1 == dir_from_str('└') == dir_from_str('↙')
	assert Dir.LEFT == Dir.L == Dir.WEST == Dir.W == Dir.PAD_4 == dir_from_str('├') == dir_from_str('←') == dir_from_str('<')
	assert Dir.UP_LEFT == Dir.UL == Dir.NORTH_WEST == Dir.NW == Dir.PAD_7 == dir_from_str('┌') == dir_from_str('↖')


def test_directions_computing():
	center = Point(4, 7)
	assert compute_direction(center, Point(4, 5)) == Dir.UP
	assert compute_direction(center, Point(5, 5)) == Dir.UP_RIGHT
	assert compute_direction(center, Point(6, 5)) == Dir.UP_RIGHT
	assert compute_direction(center, Point(6, 6)) == Dir.UP_RIGHT
	assert compute_direction(center, Point(6, 7)) == Dir.RIGHT
	assert compute_direction(center, Point(6, 8)) == Dir.DOWN_RIGHT
	assert compute_direction(center, Point(6, 9)) == Dir.DOWN_RIGHT
	assert compute_direction(center, Point(5, 9)) == Dir.DOWN_RIGHT
	assert compute_direction(center, Point(4, 9)) == Dir.DOWN
	assert compute_direction(center, Point(3, 9)) == Dir.DOWN_LEFT
	assert compute_direction(center, Point(2, 9)) == Dir.DOWN_LEFT
	assert compute_direction(center, Point(2, 8)) == Dir.DOWN_LEFT
	assert compute_direction(center, Point(2, 7)) == Dir.LEFT
	assert compute_direction(center, Point(2, 6)) == Dir.UP_LEFT
	assert compute_direction(center, Point(2, 5)) == Dir.UP_LEFT
	assert compute_direction(center, Point(3, 5)) == Dir.UP_LEFT

