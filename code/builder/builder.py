import os
import subprocess
import datetime
from file_ordering import ORDERED_CODE_FILENAMES


import_instructions = ["from " + file_name[:-3] for file_name in ORDERED_CODE_FILENAMES]


def is_import_instruction(code_line):
    for import_instruction in import_instructions:
        if import_instruction in code_line:
            return (True, '(' in code_line)
    return (False, False)


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

    with open(".." + os.sep + "version.txt", "r", encoding="utf-8") as file_version:
        str_version = file_version.read()
        token_version, semicol, str_version = str_version.partition(":")
        str_version = str_version.strip()
    str_date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    commit_hash = subprocess.Popen(
        "git rev-parse HEAD", stdout=subprocess.PIPE
    ).stdout.read()
    commit_hash = commit_hash.decode("utf-8").strip()

    text_header = TEMPLATE_HEADER.strip()
    data_tokens = ("version", "date_build", "git_commit_hash")
    data_values = (str_version, str_date_now, commit_hash)
    for data_token, data_value in zip(data_tokens, data_values):
        text_header = text_header.replace("{{" + data_token + "}}", data_value)

    for header_line in text_header.split("\n"):
        yield header_line.strip()

    yield("")


with open("aboard_standalone.py", "w", encoding="utf-8") as file_out:

    for line in generate_header():
        # OK pour le \n : https://docs.python.org/3/library/os.html#os.linesep
        file_out.write(line + "\n")

    for file_name in ORDERED_CODE_FILENAMES:
        with open(".." + os.sep + file_name, "r", encoding="utf-8") as file_code:

            import_multi_line = False

            for code_line in file_code.readlines():
                if import_multi_line:
                    if ')' in code_line:
                        import_multi_line = False
                else:
                    import_line, import_multi_line = is_import_instruction(code_line)
                    if not import_line:
                        file_out.write(code_line)

    file_out.write("\n")


print("Fini !!")
