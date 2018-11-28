from iter_indicators import IterIndicator

ItInd = IterIndicator


def _fetch_indicators(obj_source, obj_dest):
	obj_dest.prev_point = obj_source.prev_point
	obj_dest.prev_prev_point = obj_source.prev_prev_point
	obj_dest.jumped = obj_source.jumped
	obj_dest.changed_direction = obj_source.changed_direction
	obj_dest.both_coord_changed = obj_source.both_coord_changed
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


# autre sur_itérateur : emmagasiner toutes les tiles, jusqu'à répondre à une certaine condition.
# Quand ça arrive, ressortir les tiles emmagasinées, et ainsi de suite.
# (On les ressort sous forme d'un itérateur, ou d'une liste ? On va dire une liste)
# TODO : sortir les groupes de tile sous forme d'itérateur. Sans pré-itérer au départ.
# La "certaine condition", ce serait both_coord_changed. Mais on peut mettre autre chose, une lambda, etc.
