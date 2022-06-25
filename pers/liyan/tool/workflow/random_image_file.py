import os
import random
import sys


def image_file_filter(file_path):
    name_ext = os.path.splitext(os.path.basename(file_path))
    image_ext = name_ext[-1]
    if image_ext.lower() in ['.jpg', '.png', '.bmp']:
        return True
    else:
        return False


if __name__ == '__main__':
    dir_path = sys.argv[1]
    dir_file_list = os.listdir(dir_path)
    image_file_list = list(filter(image_file_filter, dir_file_list))
    print(os.path.join(dir_path, random.choice(image_file_list)), end='')
