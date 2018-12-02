# coding=utf-8
"""
quizzo_learn files_interactions
interacts with files
"""

import os.path


def save_test(dir, path):
    """ saves file '*.test' """
    with open(path, 'w', encoding="utf-8") as f:
        for frase1 in dir:
            string_to_save = frase1 + "<#^#^#>" + dir[frase1] + '\n'
            f.write(string_to_save)
        f.close()


def list_of_tests(directory_path):
    """ returns list of files '*.test' """
    return_list = []
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            if name.endswith(".test"):
                return_list.append(name[:-5])
    return return_list


def delete_file(path):
    """ deletes file """
    os.remove(path)


def read_test(path):
    """ returns list od questions and answers """
    dir_of_questions = {}
    reversed_dir_of_questions = {}

    with open(path, "r", encoding="utf-8") as f:
        f_readed = f.read()
        rows = f_readed.split("\n")
        rows = rows[:-1]
        for row in rows:
            frases = row.split("<#^#^#>")
            dir_of_questions[frases[0]] = str(frases[1])
            reversed_dir_of_questions[frases[1]] = str(frases[0])
        f.close()
    return [dir_of_questions, reversed_dir_of_questions]
