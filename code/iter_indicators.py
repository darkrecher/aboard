# -*- coding: UTF-8 -*-

from enum import IntEnum


class IterIndicator(IntEnum):
	PREV_POS = 0
	PREV_PREV_POS = 1
	JUMPED = 2
	CHANGED_DIRECTION = 3
	BOTH_COORD_CHANGED = 4
	PROPAG_DIST = 5

ItInd = IterIndicator

