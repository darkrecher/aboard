# -*- coding: UTF-8 -*-

from positions_iterator import BoardIteratorBase
from position import Pos


propag_cond_default = lambda tile_source, tile_dest: tile_dest.data == "."


class BoardIteratorPropagation(BoardIteratorBase):
    def __init__(self, board, pos_start, propag_condition=propag_cond_default):
        # TODO : avec plusieurs pos_start.
        super().__init__(board)
        self.propag_condition = propag_condition
        # Dict
        #  - clé : la pos propagée.
        #  - valeur : la distance depuis la pos de départ jusqu'à la pos propagée.
        self.propagated_poss = {}
        # liste de tuple de 2 éléments : la distance et la pos propagée.
        self.to_propagate_poss = [(0, Pos(pos_start))]

    def __iter__(self):
        return self

    def __next__(self):

        if self.to_propagate_poss:

            dist, new_pos = self.to_propagate_poss.pop(0)
            self.propagated_poss[new_pos] = dist

            to_propagate_only_poss = [o_pos for o_dist, o_pos in self.to_propagate_poss]
            for adj_pos in self.board.adjacency.adjacent_positions(new_pos):
                if all(
                    (
                        adj_pos not in self.propagated_poss,
                        adj_pos not in to_propagate_only_poss,
                        self.propag_condition(self.board[new_pos], self.board[adj_pos]),
                    )
                ):

                    self.to_propagate_poss.append((dist + 1, adj_pos))

            self.propag_dist = dist
            self._update_indicators(new_pos)
            return self.board.get_tile(new_pos)

        else:

            raise StopIteration


class BoardIteratorFindPath(BoardIteratorBase):
    def __init__(
        self, board, pos_start, pos_end, pass_through_condition=propag_cond_default
    ):
        # FUTURE : pathfinding avec tous les shortest paths possibles.
        # pathfinding avec tous les paths possibles

        super().__init__(board)
        self.pass_through_condition = pass_through_condition
        pos_start = Pos(pos_start)
        pos_end = Pos(pos_end)
        self.pos_start = pos_start
        self.pos_end = pos_end

        iter_propag = BoardIteratorPropagation(
            self.board, self.pos_start, pass_through_condition
        )

        try:
            while pos_end not in iter_propag.propagated_poss:
                next(iter_propag)
        except StopIteration:
            self.path = None
            return

        propagated_poss = iter_propag.propagated_poss

        # Et maintenant, on parcourt la propagation à l'envers,
        # pour retrouver le chemin.
        pos_cur = pos_end
        dist_cur = propagated_poss[pos_cur]
        self.path = [pos_cur]

        while pos_cur != pos_start:

            advanced = False
            for adj_pos in self.board.adjacency.adjacent_positions(pos_cur):
                if (
                    propagated_poss.get(adj_pos, -2) == dist_cur - 1
                ) and pass_through_condition(self.board[adj_pos], self.board[pos_cur]):
                    pos_cur = adj_pos
                    dist_cur -= 1
                    self.path.append(pos_cur)
                    advanced = True
                    break

            if not advanced:
                raise Exception("No adj pos with dist-1. Not supposed to happen")

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
            return self.board[pos_path]
        else:
            raise StopIteration
