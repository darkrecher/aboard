from iter_indicators import IterIndicator

ItInd = IterIndicator


def _fetch_indicators(obj_source, obj_dest):
	obj_dest.prev_point = obj_source.prev_point
	obj_dest.prev_prev_point = obj_source.prev_prev_point
	obj_dest.jumped = obj_source.jumped
	obj_dest.changed_direction = obj_source.changed_direction
	obj_dest.both_coord_changed = obj_source.both_coord_changed
	obj_dest.propag_dist = obj_source.propag_dist
	obj_dest.iter_indicators = obj_source.iter_indicators


class SurIteratorTellIndicators():

	def __init__(
		self,
		board_iterator,
		id_indic_to_tell=(ItInd.BOTH_COORD_CHANGED, )):

		self.board_iterator = board_iterator
		self.id_indic_to_tell = id_indic_to_tell


	def __iter__(self):
		return self


	def __next__(self):

		next_tile = next(self.board_iterator)
		_fetch_indicators(self.board_iterator, self)

		returned_infos = [
			self.iter_indicators[id_ind]
			for id_ind in self.id_indic_to_tell ]

		returned_infos.append(next_tile)
		return tuple(returned_infos)


group_by_subcoord=lambda board_iterator:board_iterator.both_coord_changed

class SurIteratorGroupTiles():

	def __init__(
		self,
		board_iterator,
		grouping_separator=group_by_subcoord
	):
		self.board_iterator = board_iterator
		self.grouping_separator = grouping_separator
		self.current_group_tiles = []
		self.next_tile = None


	def __iter__(self):
		# FUTURE : il faut faire une première pré-itération.
		# Et à chaque renvoi d'un nouveau groupe, on a également une itération d'avance.
		# C'est un peu étrange et je me demande s'il n'y aurait pas moyen de faire plus simple.
		self.next_tile = next(self.board_iterator)
		return self


	def __next__(self):

		if self.next_tile is None:
			raise StopIteration

		self.current_group_tiles.append(self.next_tile)
		finished_iterator = False

		try:
			self.next_tile = next(self.board_iterator)
		except StopIteration:
			finished_iterator = True

		while not self.grouping_separator(self.board_iterator) and not finished_iterator:
			self.current_group_tiles.append(self.next_tile)
			try:
				self.next_tile = next(self.board_iterator)
			except StopIteration:
				finished_iterator = True

		# TODO : à factoriser, mais après avoir testé le cas qui reste, à faire dans test_board_sur_iterator.
		if finished_iterator:
			self.next_tile = None
			returned_group_tiles = self.current_group_tiles
			self.current_group_tiles = []
			return returned_group_tiles
		else:
			returned_group_tiles = self.current_group_tiles
			self.current_group_tiles = []
			return returned_group_tiles


# autre sur_itérateur : emmagasiner toutes les tiles, jusqu'à répondre à une certaine condition.
# Quand ça arrive, ressortir les tiles emmagasinées, et ainsi de suite.
# (On les ressort sous forme d'un itérateur, ou d'une liste ? On va dire une liste)
# TODO : sortir les groupes de tile sous forme d'itérateur. Sans pré-itérer au départ.
# La "certaine condition", ce serait both_coord_changed. Mais on peut mettre autre chose, une lambda, etc.
