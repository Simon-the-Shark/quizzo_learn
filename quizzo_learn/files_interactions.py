import os.path


def save_test(dir, path):
    with open(path, 'w') as f:
        for frase1 in dir:
            string_to_save = frase1 + "^&^&^&9&^&^&^$#$&^&#@$!" + dir[frase1] + '\n'
            f.write(string_to_save)
        f.close()


def list_of_tests(directory_path):
    return_list = []
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            if name.endswith(".test"):
                return_list.append(name[:-5])
    return return_list


def delete_file(path):
    os.remove(path)
