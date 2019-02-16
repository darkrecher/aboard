# -*- coding: UTF-8 -*-

from position import Point


def test_from_obj():

	class Whatever():

		def __init__(self):
			self.x = 23.9
			self.y = 45.8

	p = Point(Whatever())
	assert p.x == 23 and p.y == 45


def test_from_dict():
	p = Point({ 'x': 23.9, 'y': 45.8 })
	assert p.x == 23 and p.y == 45


def test_from_list():
	p = Point([ 23.9, 45.8 ])
	assert p.x == 23 and p.y == 45


def test_from_iterable():
	p = Point(range(10, 40, 7))
	assert p.x == 10 and p.y == 17


def test_from_param():
	p = Point(23.9, 45.8)
	assert p.x == 23 and p.y == 45


def test_from_param_xy():
	p = Point(x=23.9, y=45.8)
	assert p.x == 23 and p.y == 45


def test_from_point():
	p_1 = Point(x=23.9, y=45.8)
	p_2 = Point(p_1)
	p_1.x = 0
	p_1.y = 1
	assert p_2.x == 23 and p_2.y == 45


def test_coord_outing():
	p = Point(23.9, 45.8)
	t = p.as_tuple()
	assert t[0] == 23 and t[1] == 45
	d = p.as_dict()
	assert d['x'] == 23 and d['y'] == 45


def test_str():
	p = Point(23.9, 45.8)
	assert str(p) == '<Point 23, 45 >'


def test_eq():

	p_1 = Point(34, 78)
	p_2 = Point(35, 78)
	p_3 = Point(34, 77)
	p_4 = Point(34, 78)
	p_5 = Point(0, 0)

	assert p_1 == p_1
	assert p_1 != p_2
	assert p_1 != p_3
	assert p_1 == p_4
	assert p_1 != p_5
