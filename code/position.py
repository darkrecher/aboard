# -*- coding: UTF-8 -*-


from direction import Dir


class Pos:
    def __init__(self, param_1=None, param_2=None, x=None, y=None):

        if hasattr(param_1, "x") and hasattr(param_1, "y"):
            if self._compute_coords(param_1.x, param_1.y):
                return

        try:
            final_x = param_1["x"]
            final_y = param_1["y"]
        except TypeError:
            pass
        else:
            if self._compute_coords(final_x, final_y):
                return

        try:
            # FUTURE : il faudrait vérifier que param_1 est itérable,
            # et également ordonné.
            # Ce code fonctionne avec un objet "Set", mais de manière
            # non déterministe. On ne sait pas ce qui va dans x ni dans y.
            iter_param_1 = iter(param_1)
            final_x = next(iter_param_1)
            final_y = next(iter_param_1)
        except TypeError:
            pass
        except StopIteration:
            pass
        else:
            if self._compute_coords(final_x, final_y):
                return

        if self._compute_coords(param_1, param_2):
            return

        if self._compute_coords(x, y):
            return

        raise ValueError(
            "Impossible de déduire des coordonnées de ces params : %s %s %s %s"
            % (param_1, param_2, x, y)
        )

    def _compute_coords(self, final_x, final_y):
        try:
            int_final_x = int(final_x)
            int_final_y = int(final_y)
        except TypeError:
            return False
        except ValueError:
            return False
        else:
            self.x = int_final_x
            self.y = int_final_y
            return True

    def __str__(self):
        return "<Pos %s, %s >" % (str(self.x), str(self.y))

    def as_tuple(self):
        return self.x, self.y

    def as_dict(self):
        return {"x": self.x, "y": self.y}

        # TODO : fonction à tester vite fait.

    def move(self, direction, dist=1):
        DICT_VECT_FROM_DIRS = {
            Dir.UP: (0, -1),
            Dir.UP_RIGHT: (+1, -1),
            Dir.RIGHT: (+1, 0),
            Dir.DOWN_RIGHT: (+1, +1),
            Dir.DOWN: (0, +1),
            Dir.DOWN_LEFT: (-1, +1),
            Dir.LEFT: (-1, 0),
            Dir.UP_LEFT: (-1, -1),
        }
        mov_x, mov_y = DICT_VECT_FROM_DIRS[direction]
        self.x += mov_x * dist
        self.y += mov_y * dist

    def __eq__(self, other):
        pos_other = Pos(other)
        return self.x == pos_other.x and self.y == pos_other.y

    def __hash__(self):
        return hash((self.x, self.y))


# Si on veut un nom de classe plus explicite et plus long.
Position = Pos


# --- Direction operations ---


def cmp(a, b):
    # https://stackoverflow.com/questions/15556813/python-why-cmp-is-useful
    return (a > b) - (a < b)


def compute_direction(pos_1, pos_2):
    cmp_x = cmp(pos_2.x, pos_1.x)
    cmp_y = cmp(pos_2.y, pos_1.y)
    cmps = (cmp_x, cmp_y)
    DICT_DIR_FROM_CMPS = {
        (0, 0): None,
        (0, -1): Dir.UP,
        (+1, -1): Dir.UP_RIGHT,
        (+1, 0): Dir.RIGHT,
        (+1, +1): Dir.DOWN_RIGHT,
        (0, +1): Dir.DOWN,
        (-1, +1): Dir.DOWN_LEFT,
        (-1, 0): Dir.LEFT,
        (-1, -1): Dir.UP_LEFT,
    }
    return DICT_DIR_FROM_CMPS[cmps]
