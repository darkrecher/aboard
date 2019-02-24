# -*- coding: UTF-8 -*-


from aboard import Board
from board_renderer import BoardRenderer
from board_comparator import IteratorGetDifferences


def test_comp_simple():

    board_1 = Board(5, 3)
    setting_data_1 = ("ABCDE", "FGHIJ", "KLMNO")
    board_1.set_data_from_string(setting_data_1)

    board_2 = Board(5, 3)
    setting_data_2 = ("ABCDX", "FGHIJ", "KZMNO")
    board_2.set_data_from_string(setting_data_2)

    index_diff = 0

    for tile_1, tile_2 in IteratorGetDifferences(board_1[:], board_2[:]):

        print(tile_1, tile_2)

        if index_diff == 0:
            first = False
            assert tile_1.x == tile_2.x == 4
            assert tile_1.y == tile_2.y == 0
            assert tile_1.data == "E"
            assert tile_2.data == "X"
        elif index_diff == 1:
            assert tile_1.x == tile_2.x == 1
            assert tile_1.y == tile_2.y == 2
            assert tile_1.data == "L"
            assert tile_2.data == "Z"
        else:
            assert False

        index_diff += 1


def test_comp_no_diff():

    setting_data = ("ABCDE", "FGHIJ", "KLMNO")

    board_1 = Board(5, 3)
    board_1.set_data_from_string(setting_data)

    board_2 = Board(5, 3)
    board_2.set_data_from_string(setting_data)

    assert list(IteratorGetDifferences(board_1[:], board_2[:])) == []


# TODO :
#  - test de func_comparison spécifique.
#  - test avec check_disposition = True et = False.
#  - test avec check_quantity = True et = False.
#  - test de comparaison sur le même board, mais avec deux itérateurs différents. (un test sans diff, un avec).
