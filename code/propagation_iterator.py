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
				o_point
				for o_dist, o_point
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

