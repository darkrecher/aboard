# -*- coding: UTF-8 -*-

from point import Point, Dir, dir_from_str, compute_direction

from adjacency import (
	AdjacencyEvaluatorCross, AdjacencyEvaluatorCrossDiag,
	set_default_adjacency)

from aboard import Board


def test_adj_cross():

	simple_board = Board(10, 10, class_adjacency=AdjacencyEvaluatorCross)

	p1 = Point(5, 5)
	p2 = Point(6, 5)
	p3 = Point(4, 4)

	# same :
	assert simple_board.is_adjacent(p1, p1) == False
	# cross :
	assert simple_board.is_adjacent(p1, p2) == True
	# diag :
	assert simple_board.is_adjacent(p1, p3) == False
	# none :
	assert simple_board.is_adjacent(p2, p3) == False


def test_adj_diag():

	simple_board = Board(10, 10, class_adjacency=AdjacencyEvaluatorCrossDiag)

	p1 = Point(5, 5)
	p2 = Point(6, 5)
	p3 = Point(4, 4)

	# same :
	assert simple_board.is_adjacent(p1, p1) == False
	# cross :
	assert simple_board.is_adjacent(p1, p2) == True
	# diag :
	assert simple_board.is_adjacent(p1, p3) == True
	# none :
	assert simple_board.is_adjacent(p2, p3) == False


def test_adj_default():

	board_adj_default_cross = Board(10, 10)

	p1 = Point(5, 5)
	p2 = Point(6, 5)
	p3 = Point(4, 4)

	# cross:
	assert board_adj_default_cross.is_adjacent(p1, p2) == True
	# diag :
	assert board_adj_default_cross.is_adjacent(p1, p3) == False

	set_default_adjacency(AdjacencyEvaluatorCross)
	board_adj_default_cross_2 = Board(10, 10)
	# cross:
	assert board_adj_default_cross_2.is_adjacent(p1, p2) == True
	# diag :
	assert board_adj_default_cross_2.is_adjacent(p1, p3) == False

	set_default_adjacency(AdjacencyEvaluatorCrossDiag)
	board_adj_default_cross_diag = Board(10, 10)
	# cross:
	assert board_adj_default_cross_diag.is_adjacent(p1, p2) == True
	# diag :
	assert board_adj_default_cross_diag.is_adjacent(p1, p3) == True


def test_directions_equivalence():
	assert Dir.UP == Dir.U == Dir.NORTH == Dir.N == Dir.PAD_8 == dir_from_str('┬') == dir_from_str('↑') == dir_from_str('^')
	assert Dir.UP_RIGHT == Dir.UR == Dir.NORTH_EAST == Dir.NE == Dir.PAD_9 == dir_from_str('┐') == dir_from_str('↗')
	assert Dir.RIGHT == Dir.R == Dir.EAST == Dir.E == Dir.PAD_6 == dir_from_str('┤') == dir_from_str('→') == dir_from_str('>')
	assert Dir.DOWN_RIGHT == Dir.DR == Dir.SOUTH_EAST == Dir.SE == Dir.PAD_3 == dir_from_str('┘') == dir_from_str('↘')
	assert Dir.DOWN == Dir.D == Dir.SOUTH == Dir.S == Dir.PAD_2 == dir_from_str('┴') == dir_from_str('↓') == dir_from_str('V') == dir_from_str('v')
	assert Dir.DOWN_LEFT == Dir.DL == Dir.SOUTH_WEST == Dir.SW == Dir.PAD_1 == dir_from_str('└') == dir_from_str('↙')
	assert Dir.LEFT == Dir.L == Dir.WEST == Dir.W == Dir.PAD_4 == dir_from_str('├') == dir_from_str('←') == dir_from_str('<')
	assert Dir.UP_LEFT == Dir.UL == Dir.NORTH_WEST == Dir.NW == Dir.PAD_7 == dir_from_str('┌') == dir_from_str('↖')


def test_directions_ordering():
	dirs = [ Dir.LEFT, Dir.UP_LEFT, Dir.DOWN_RIGHT, Dir.RIGHT, Dir.UP, Dir.DOWN_LEFT, Dir.UP_RIGHT, Dir.DOWN ]
	dirs.sort()
	assert dirs == [ Dir.UP, Dir.UP_RIGHT, Dir.RIGHT, Dir.DOWN_RIGHT, Dir.DOWN, Dir.DOWN_LEFT, Dir.LEFT, Dir.UP_LEFT ]


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

