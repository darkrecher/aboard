# -*- coding: UTF-8 -*-

from point import (
	Point, Direction,
	compute_direction,
	is_adjacent_cross, is_adjacent_diag, set_default_adjacency, is_adjacent,
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


# TODO : tester les directions

