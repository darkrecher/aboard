import os
from file_ordering import ORDERED_CODE_FILENAMES

import_instructions = [
	'from ' + file_name[:-3]
	for file_name in ORDERED_CODE_FILENAMES
]

def is_import_instruction(code_line):
	for import_instruction in import_instructions:
		if import_instruction in code_line:
			return True
	return False

# TODO : ajouter des commentaires indiquant le nom du fichier à chaque fois.
# TODO : et au début, le numéro de commit, la version, le repo git, ...
with open('aboard_standalone.py', 'w', encoding='utf-8') as file_out:

	for file_name in ORDERED_CODE_FILENAMES:
		with open('..' + os.sep + file_name, 'r', encoding='utf-8') as file_code:

			for code_line in file_code.readlines():
				if not is_import_instruction(code_line):
					#print(code_line)
					file_out.write(code_line)
	# TODO : y'avait pas un writeline quelque part ? (Connerie de \r\n / \n / ...)
	file_out.write('\n')

print("Fini !!")



