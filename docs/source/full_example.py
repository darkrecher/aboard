from aboard import Board, Tile, Dir, BoardRenderer, compute_direction


class XmasTile(Tile):
    """
    Tile spécifique, pour l'exemple inspiré de Xmas Rush.

    Variables membres :
        mid_marker : string de un seul caractère, qui sera affiché lors
            du rendu de la tile.
            C'est l'équivalent de tile.data dans la classe de base.
        roads : dictionnaire avec 4 éléments. Les clés du dictionnaire
            sont les 4 directions Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT.
            Chaque valeur est un booléen, indiquant si le chemin de
            cette tile dans la direction indiqué par la clé est ouvert.

    Les roads de la tile peuvent être initialisées à l'aide d'un
    caractère (voir fonction Tile.dirs_from_input).
    """

    # Liste des caractères "roadful" permettant d'initialiser les roads.
    # Il n'y a pas toutes les combinaisons possibles,
    # car on n'en a pas besoin.
    # clé : un caractère. (Sa représentation visuelle correspond
    # à peu près aux roads ouvertes).
    # valeur : une liste de directions, indiquant les roads ouvertes
    # correspondantes. Celles qui ne sont pas dans la liste doivent
    # rester fermées.
    # Par exemple : la lettre L équivaut à une road ouverte vers le haut,
    # et une vers la droite.
    DICT_ROADFUL_DIRS_FROM_CHAR = {
        "-": (Dir.LEFT, Dir.RIGHT),
        "|": (Dir.UP, Dir.DOWN),
        "L": (Dir.UP, Dir.RIGHT),
        "/": (Dir.DOWN, Dir.RIGHT),
        "7": (Dir.DOWN, Dir.LEFT),
        "J": (Dir.UP, Dir.LEFT),
        "+": (Dir.LEFT, Dir.RIGHT, Dir.UP, Dir.DOWN),
        " ": (),
    }

    def __init__(self, x=None, y=None, board_owner=None):
        super().__init__(x, y, board_owner)
        self.roads = {
            Dir.UP: False,
            Dir.RIGHT: False,
            Dir.DOWN: False,
            Dir.LEFT: False
        }
        self.mid_marker = " "

    def dirs_from_input(self, char_roadful):
        """
        Initialise les routes ouvertes de la tile (dict self.roads),
        à partir du caractère "roadful" passé en paramètre.
        """
        for dir_ in XmasTile.DICT_ROADFUL_DIRS_FROM_CHAR[char_roadful]:
            self.roads[dir_] = True

    def render(self, w=3, h=3):
        """
        Renvoie la représentation graphique de la tile. Le rendu par
        défaut est sur un carré de 3x3 caractères. Les roads ouvertes
        sont affichées par des tirets et des traits verticaux.
        La variable mid_marker est affichée au milieu du rendu.

        Exemple :

        Avec un self.roads dans lequel les directions Dir.UP et Dir.RIGHT
        sont à True, et les deux autres sont à False.
        Avec un self.mid_marker = "A".

        Le rendu renverra la liste de string suivantes :
        [
            ' | ',
            ' A-',
            '   ',
        ]
        """
        path_up = "|" if self.roads[Dir.UP] else " "
        path_left = "-" if self.roads[Dir.LEFT] else " "
        path_right = "-" if self.roads[Dir.RIGHT] else " "
        path_down = "|" if self.roads[Dir.DOWN] else " "
        template = " %s \n%s%s%s\n %s "

        data = (
            path_up, path_left,
            self.mid_marker[:1].rjust(1),
            path_right, path_down
        )

        str_result = template % data
        return str_result.split("\n")


def pass_through_xmas(tile_source, tile_dest):
    """
    Fonction utilisée comme condition de déplacement pour le path-finding.
    On considère qu'il est possible de passer d'une tile à l'autre si la
    route adéquate est ouverte à la fois dans la tile source et dans la
    tile dest. La route adéquate dépend de la position relative de
    tile_source et tile_dest.

    Exemple :

    Avec tile_1.roads[Dir.RIGHT] = True
    Avec tile_2.roads[Dir.LEFT] = True

    C'est à dire, que les rendu seraient les suivants :
    tile_1 = [
        '   ',
        ' .-',
        '   ',
    ]
    tile_2 = [
        '   ',
        '-. ',
        '   ',
    ]

    Le déplacement est possible si tile_1 est à gauche de tile_2.
    Dans les autres cas de positions relatives, le déplacement n'est
    pas possible.
    """
    dir_ = compute_direction(tile_source, tile_dest)
    roads_to_check = {
        Dir.UP: (Dir.UP, Dir.DOWN),
        Dir.DOWN: (Dir.DOWN, Dir.UP),
        Dir.LEFT: (Dir.LEFT, Dir.RIGHT),
        Dir.RIGHT: (Dir.RIGHT, Dir.LEFT),
    }
    road_to_check = roads_to_check.get(dir_)
    if road_to_check is None:
        # Not supposed to happen
        return False
    road_source, road_dest = road_to_check
    return tile_source.roads[road_source] and tile_dest.roads[road_dest]


renderer = BoardRenderer(
    tile_w=3, tile_h=3,
    tile_padding_w=1, tile_padding_h=1,
    chr_fill_tile_padding="."
)

board = Board(6, 4, class_tile=XmasTile, default_renderer=renderer)

# Plan du board. (Une multi-line string de 6 colonnes et 4 lignes, comme
# les dimensions du board). Chaque caractère est un "roadful" char,
# définissant les directions ouvertes de la tile correspondante.
# Certains chemins sont des culs-de-sac, et il y a deux chemins
# possibles pour aller d'une tile du bas vers une tile du haut.
# C'est fait exprès pour le test.
BOARD_MAP = """
 /---7
/+7  |
||   |
L----J
"""

board_map = BOARD_MAP.replace("\n", "")

# Initialisation des routes du board, à partir de BOARD_MAP.
for tile, char_roadful in zip(board, board_map):
    tile.dirs_from_input(char_roadful)

# Recherche du chemin le plus court. Marquage de ce chemin en définissant
# les mid_marker des tiles par lesquelles ont passe.
# Départ = 0. Tile suivante = 1. Ainsi de suite.
for index, tile in enumerate(
    board.get_by_pathfinding((0, 3), (2, 0), pass_through_xmas)
):
    tile.mid_marker = str(index)

# Affichage du rendu, permettant de vérifier le plan du board,
# ainsi que le chemin trouvé.
print(board.render())

expected_result = """

   .   .   .   .   .
   . 4-.-5-.- -.- -.-
   . | .   .   .   . |
.......................
   . | .   .   .   . |
 2-.-3-.-  .   .   .
 | . | . | .   .   . |
.......................
 | . | .   .   .   . |
 1 .   .   .   .   .
 | . | .   .   .   . |
.......................
 | .   .   .   .   . |
 0-.- -.- -.- -.- -.-
   .   .   .   .   .

"""
