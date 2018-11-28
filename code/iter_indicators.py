# -*- coding: UTF-8 -*-

from enum import IntEnum


class IterIndicator(IntEnum):
	PREV_POINT = 0
	PREV_PREV_POINT = 1
	JUMPED = 2
	CHANGED_DIRECTION = 3
	BOTH_COORD_CHANGED = 4

ItInd = IterIndicator

