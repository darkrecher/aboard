import sys

def log(*args):
	"""
	Simple log.
	"""
	print(*args, file=sys.stderr)


