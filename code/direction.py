# -*- coding: UTF-8 -*-


from enum import IntEnum

class Direction(IntEnum):
	# C'est dans l'ordre du sens des aiguilles d'une montre, en commençant par le haut.
	# Classic
	UP = 0
	UP_RIGHT = 1
	RIGHT = 2
	DOWN_RIGHT = 3
	DOWN = 4
	DOWN_LEFT = 5
	LEFT = 6
	UP_LEFT = 7
	# Classic abbr.
	U = 0
	UR = 1
	R = 2
	DR = 3
	D = 4
	DL = 5
	L = 6
	UL = 7
	# Cardinal
	NORTH = 0
	NORTH_EAST = 1
	EAST = 2
	SOUTH_EAST = 3
	SOUTH = 4
	SOUTH_WEST = 5
	WEST = 6
	NORTH_WEST = 7
	# Cardinal abbr.
	N = 0
	NE = 1
	E = 2
	SE = 3
	S = 4
	SW = 5
	W = 6
	NW = 7
	# Numeric pad.
	PAD_8 = 0
	PAD_9 = 1
	PAD_6 = 2
	PAD_3 = 3
	PAD_2 = 4
	PAD_1 = 5
	PAD_4 = 6
	PAD_7 = 7

# Alias
Dir = Direction

DICT_DIR_FROM_STR = {
	# Box-drawing chars (https://en.wikipedia.org/wiki/Box-drawing_character)
	'┬': Dir.UP,
	'┐': Dir.UP_RIGHT,
	'┤': Dir.RIGHT,
	'┘': Dir.DOWN_RIGHT,
	'┴': Dir.DOWN,
	'└': Dir.DOWN_LEFT,
	'├': Dir.LEFT,
	'┌': Dir.UP_LEFT,
	# Arrows (ne marche pas complètement bien dans Sublime Text, mais c'est pas grave)
	'↑': Dir.UP,
	'↗': Dir.UP_RIGHT,
	'→': Dir.RIGHT,
	'↘': Dir.DOWN_RIGHT,
	'↓': Dir.DOWN,
	'↙': Dir.DOWN_LEFT,
	'←': Dir.LEFT,
	'↖': Dir.UP_LEFT,
	# Ascii arrows
	'^': Dir.UP,
	'>': Dir.RIGHT,
	'v': Dir.DOWN,
	'V': Dir.DOWN,
	'<': Dir.LEFT,
}

def dir_from_str(char):
	# FUTURE : raiser une exception spécifique si y'a pas le char dans dict.
	return DICT_DIR_FROM_STR[char]
