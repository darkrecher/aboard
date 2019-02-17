import os
import subprocess
import datetime
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


def generate_header():
	TEMPLATE_HEADER = """
	# -*- coding: UTF-8 -*-

	# Version stand-alone de la librairie python aboard.
	# https://github.com/darkrecher/aboard
	# https://aboard.readthedocs.io/fr/latest/
	#
	# Version : {{version}}
	# Date du build : {{date_build}}
	# commit git : {{git_commit_hash}}
	"""

	with open('..' + os.sep + 'version.txt', 'r', encoding='utf-8') as file_version:
		str_version = file_version.read()
		token_version, semicol, str_version = str_version.partition(':')
		str_version = str_version.strip()
	str_date_now = datetime.datetime.now().strftime('%Y-%m-%d')
	commit_hash = subprocess.Popen("git rev-parse HEAD", stdout=subprocess.PIPE).stdout.read()
	commit_hash = commit_hash.decode('utf-8').strip()

	text_header = TEMPLATE_HEADER.strip()
	data_tokens = ('version', 'date_build', 'git_commit_hash')
	data_values = (str_version, str_date_now, commit_hash)
	for data_token, data_value in zip(data_tokens, data_values):
		text_header = text_header.replace('{{' + data_token + '}}', data_value)

	for header_line in text_header.split('\n'):
		yield header_line.strip()


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



