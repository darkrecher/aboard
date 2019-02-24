# -*- coding: UTF-8 -*-

from position import Pos


def test_from_obj():
    class Whatever:
        def __init__(self):
            self.x = 23.9
            self.y = 45.8

    p = Pos(Whatever())
    assert p.x == 23 and p.y == 45


def test_from_dict():
    p = Pos({"x": 23.9, "y": 45.8})
    assert p.x == 23 and p.y == 45


def test_from_list():
    p = Pos([23.9, 45.8])
    assert p.x == 23 and p.y == 45


def test_from_iterable():
    p = Pos(range(10, 40, 7))
    assert p.x == 10 and p.y == 17


def test_from_param():
    p = Pos(23.9, 45.8)
    assert p.x == 23 and p.y == 45


def test_from_param_xy():
    p = Pos(x=23.9, y=45.8)
    assert p.x == 23 and p.y == 45


def test_from_pos():
    p_1 = Pos(x=23.9, y=45.8)
    p_2 = Pos(p_1)
    p_1.x = 0
    p_1.y = 1
    assert p_2.x == 23 and p_2.y == 45


def test_coord_outing():
    p = Pos(23.9, 45.8)
    t = p.as_tuple()
    assert t[0] == 23 and t[1] == 45
    d = p.as_dict()
    assert d["x"] == 23 and d["y"] == 45


def test_str():
    p = Pos(23.9, 45.8)
    assert str(p) == "<Pos 23, 45 >"


def test_eq():

    p_1 = Pos(34, 78)
    p_2 = Pos(35, 78)
    p_3 = Pos(34, 77)
    p_4 = Pos(34, 78)
    p_5 = Pos(0, 0)

    assert p_1 == p_1
    assert p_1 != p_2
    assert p_1 != p_3
    assert p_1 == p_4
    assert p_1 != p_5
