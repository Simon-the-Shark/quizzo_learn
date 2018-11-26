import os.path


def save_test(name, dir):
    with open(os.path.join(os.pardir, "res", "my_tests", name + ".test"), 'w') as f:
        for frase1 in dir:
            string_to_save = frase1 + "^&^&^&9&^&^&^$#$&^&#@$!" + dir[frase1] + '\n'
            f.write(string_to_save)
        f.close()
