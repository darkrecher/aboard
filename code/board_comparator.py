# -*- coding: UTF-8 -*-


from positions_iterator import BoardIteratorBase


class IteratorGetDifferences(BoardIteratorBase):
    def __init__(
        self,
        board_iterator_1,
        board_iterator_2,
        func_comparison=lambda tile_1, tile_2: tile_1 == tile_2,
        check_disposition=True,
        check_quantity=True,
    ):
        self.board_iterator_1 = board_iterator_1
        self.board_iterator_2 = board_iterator_2
        self.func_comparison = func_comparison
        self.check_disposition = check_disposition
        self.check_quantity = check_quantity

    def __iter__(self):
        return self

    def __next__(self):

        while True:

            try:
                tile_1 = next(self.board_iterator_1)
                finished_iter_1 = False
            except StopIteration:
                finished_iter_1 = True

            try:
                tile_2 = next(self.board_iterator_2)
                finished_iter_2 = False
            except StopIteration:
                finished_iter_2 = True

            if finished_iter_1 or finished_iter_2:
                if (finished_iter_1 != finished_iter_2) and self.check_quantity:
                    # TODO : une classe d'exception custom.
                    raise Exception(
                        "Nombre de tile différentes entre les deux itérateurs de tiles."
                    )
                else:
                    raise StopIteration

            if (
                self.board_iterator_1.both_coord_changed
                != self.board_iterator_2.both_coord_changed
            ) and self.check_disposition:
                # TODO : une classe d'exception custom.
                raise Exception("Les tiles ne sont pas disposées de la même manière.")

            if not self.func_comparison(tile_1, tile_2):
                return (tile_1, tile_2)
