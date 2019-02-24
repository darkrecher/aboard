# -*- coding: UTF-8 -*-


from aboard import Board
from board_renderer import BoardRenderer


def strip_multiline(multi_string):
    # J'ai besoin de cette fonction juste pour pouvoir présenter
    # les strings d'une manière plus lisible.
    return "\n".join([line.strip() for line in multi_string.strip().split("\n")])


def test_init_simple():
    board = Board(5, 3)
    setting_data = ("ABCDE", "FGHIJ", "KLMNO")

    board.set_data_from_string(setting_data)

    render_result = """

		ABCDE
		FGHIJ
		KLMNO

	"""
    assert strip_multiline(board.render()) == strip_multiline(render_result)


def test_init_separators():
    board = Board(6, 4)
    # setting_data = ('A;B;C;D;E;F\n', 'GHIJKL', 'MNOPQR', 'STUVWX')
    setting_data = "A;B;C;D;E;F\nG;H;I;J;K;L\nM;N;O;P;Q;R\nS;T;U;V;W;X"

    board.set_data_from_string(setting_data, "\n", ";")

    render_result = """

		ABCDEF
		GHIJKL
		MNOPQR
		STUVWX

	"""
    assert strip_multiline(board.render()) == strip_multiline(render_result)
