# -*- coding: UTF-8 -*-


from point import Dir, compute_direction
from tile import Tile
from adjacency import AdjacencyEvaluatorCross, set_default_adjacency
from board_renderer import BoardRenderer
from propagation_iterator import BoardIteratorFindPath
from aboard import Board


def strip_multiline(multi_string):
	# J'ai besoin de cette fonction juste pour pouvoir présenter
	# les strings d'une manière plus lisible.
	return '\n'.join([
		line.strip()
		for line in multi_string.strip().split('\n')
	])


class XmasTile(Tile):

	def __init__(self, x=None, y=None, board_father=None):
		super().__init__(x, y, board_father)
		self.roads = {
			Dir.UP: False,
			Dir.RIGHT: False,
			Dir.DOWN: False,
			Dir.LEFT: False,
		}
		self.mid_marker = ' '


	def dirs_from_input(self, str_input):
		"""
		en haut, à droite, en bas, à gauche.
		"""
		if len(str_input) < 4:
			raise Exception("str_input fail : " + str_input)
		if str_input[0] == '1':
			self.roads[Dir.UP] = True
		if str_input[1] == '1':
			self.roads[Dir.RIGHT] = True
		if str_input[2] == '1':
			self.roads[Dir.DOWN] = True
		if str_input[3] == '1':
			self.roads[Dir.LEFT] = True


	def render(self, w=3, h=3):

		str_result = []

		item_marker = ' '

		if self.roads[Dir.UP]:
			dir_marker = '|'
		else:
			dir_marker = ' '

		str_result.append(item_marker + dir_marker + ' ')

		left_char = '-' if self.roads[Dir.LEFT] else ' '

		right_char = '-' if self.roads[Dir.RIGHT] else ' '
		str_result.append(left_char + self.mid_marker + right_char)
		if self.roads[Dir.DOWN]:
			line_3 = ' | '
		else:
			line_3 = '   '
		str_result.append(line_3)

		return str_result


def pass_through_xmas(tile_source, tile_dest):
	dir_ = compute_direction(tile_source, tile_dest)
	roads_to_check = {
		Dir.UP:(Dir.UP, Dir.DOWN),
		Dir.DOWN:(Dir.DOWN, Dir.UP),
		Dir.LEFT:(Dir.LEFT, Dir.RIGHT),
		Dir.RIGHT:(Dir.RIGHT, Dir.LEFT),
	}
	road_to_check = roads_to_check.get(dir_)
	if road_to_check is None:
		# Not supposed to happen
		return False
	road_source, road_dest = road_to_check
	return tile_source.roads[road_source] and tile_dest.roads[road_dest]


def test_find_path_roads():
	# Test ajouté suite à un bug trouvé lors du challenge CodinGame "XMas Rush".

	set_default_adjacency(AdjacencyEvaluatorCross)

	renderer = BoardRenderer(tile_w=3, tile_h=3, tile_padding_w=1, tile_padding_h=1, chr_fill_tile_padding='.')
	board = Board(
		7, 7, class_tile=XmasTile,
		default_renderer=renderer,
	)

	definition_roads = (
		(0, 3, '1010'),
		(0, 2, '1010'),
		(0, 1, '0111'),
		(1, 1, '1111'),
		(2, 1, '0011'),
		(1, 0, '0110'),
		(2, 0, '0101'),
	)

	for x, y, input_def_roads in definition_roads:
		board[x, y].dirs_from_input(input_def_roads)

	for index, tile in enumerate(BoardIteratorFindPath(board, (0, 3), (2, 0), pass_through_xmas)):
		tile.mid_marker = str(index)

	print(board.render())

	render_result = """

		   .   .   .   .   .   .
		   . 4-.-5-.   .   .   .
		   . | .   .   .   .   .
		...........................
		   . | .   .   .   .   .
		-2-.-3-.-  .   .   .   .
		 | . | . | .   .   .   .
		...........................
		 | .   .   .   .   .   .
		 1 .   .   .   .   .   .
		 | .   .   .   .   .   .
		...........................
		 | .   .   .   .   .   .
		 0 .   .   .   .   .   .
		 | .   .   .   .   .   .
		...........................
		   .   .   .   .   .   .
		   .   .   .   .   .   .
		   .   .   .   .   .   .
		...........................
		   .   .   .   .   .   .
		   .   .   .   .   .   .
		   .   .   .   .   .   .
		...........................
		   .   .   .   .   .   .
		   .   .   .   .   .   .
		   .   .   .   .   .   .

	"""
	assert strip_multiline(board.render()) == strip_multiline(render_result)

