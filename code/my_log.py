# -*- coding: UTF-8 -*-


"""
On va faire simple.
C'est étonnant comme un truc aussi simple que le log peut devenir compliqué.
Dans tout un tas de cas.
Je veux juste écrire des conneries. C'est possible ou bien ?
"""

import sys

def log(*args):
	print(*args, file=sys.stderr)


