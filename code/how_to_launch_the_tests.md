
# Pour lancer les tests

Il faut avoir préalablement installé pytest, avec "pip install pytest"

Ensuite, il faut exécuter dans la console :

`python -m py.test`

Les commandes py.test ou pytest ne marche pas, car elles ne parviennent pas à déterminer correctement le rootdir (je ne sais pas pourquoi).

Et comme les tests sont dans un répertoire "tests", donc pas dans le rootdir, ça ne marche pas.

Pour exécuter un seul fichier de test :

`python -m py.test -k tests/test_le_fichier.py`
