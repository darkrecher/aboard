# -*- coding: UTF-8 -*-

from positions_iterator import BoardIteratorBase
from point import Point


# TODO : un sur-itérateur renvoyant la distance de propagation.


propag_cond_default = lambda tile_source, tile_dest: tile_dest.data == '.'


class BoardIteratorPropagation(BoardIteratorBase):

	def __init__(self, board, pos_start, propag_condition=propag_cond_default):
		# TODO : avec plusieurs pos_start.
		super().__init__(board)
		self.propag_condition = propag_condition
		# Dict
		#  - clé : le point propagé.
		#  - valeur : la distance depuis le point de départ jusqu'au point propagé.
		self.propagated_points = {}
		# liste de tuple de 2 éléments : la distance et le point propagé.
		self.to_propagate_points = [ (0, Point(pos_start)) ]


	def __iter__(self):
		return self


	def __next__(self):

		if self.to_propagate_points:

			dist, new_point = self.to_propagate_points.pop(0)
			self.propagated_points[new_point] = dist

			to_propagate_only_points = [
				o_point for o_dist, o_point
				in self.to_propagate_points
			]
			for adj_point in self.board.adjacency.adjacent_points(new_point):
				# TODO : mise en forme
				if all((
					adj_point not in self.propagated_points,
					adj_point not in to_propagate_only_points,
					self.propag_condition(self.board.get_tile(new_point), self.board.get_tile(adj_point))
				)):

					self.to_propagate_points.append((dist+1, adj_point))

			self.propag_dist = dist
			self._update_indicators(new_point)
			return self.board.get_tile(new_point)

		else:

			raise StopIteration


class BoardIteratorFindPath(BoardIteratorBase):

	def __init__(
		self, board,
		pos_start, pos_end,
		pass_through_condition=propag_cond_default
	):
	# FUTURE : pathfinding avec tous les shortest paths possibles.
	# pathfinding avec tous les paths possibles

		super().__init__(board)
		self.pass_through_condition = pass_through_condition
		pos_start = Point(pos_start)
		pos_end = Point(pos_end)
		self.pos_start = pos_start
		self.pos_end = pos_end

		iter_propag = BoardIteratorPropagation(
			self.board,
			self.pos_start,
			pass_through_condition)

		try:
			while pos_end not in iter_propag.propagated_points:
				next(iter_propag)
		except StopIteration:
			self.path = None
			return

		propagated_points = iter_propag.propagated_points

		# Et maintenant, on parcourt la propagation à l'envers,
		# pour retrouver le chemin.
		pos_cur = pos_end
		dist_cur = propagated_points[pos_cur]
		self.path = [ pos_cur ]

		while pos_cur != pos_start:

			advanced = False
			for adj_point in self.board.adjacency.adjacent_points(pos_cur):
				if propagated_points.get(adj_point, -2) == dist_cur - 1:
					pos_cur = adj_point
					dist_cur -= 1
					self.path.append(pos_cur)
					advanced = True
					break

			if not advanced:
				raise Exception("No adj point with dist-1. Not supposed to happen")


	def __iter__(self):
		if self.path is None:
			# TODO : raiser une exception spécifique.
			# TODO : ou alors, faut signaler de manière moins violente que y'a pas de chemin.
			raise ValueError("Impossible de trouver un chemin")
		return self


	def __next__(self):
		if self.path:
			pos_path = self.path.pop()
			self._update_indicators(pos_path)
			# TODO : le __getitem__ doit pouvoir accepter des objets Point.
			return self.board[pos_path.x, pos_path.y]
		else:
			raise StopIteration



