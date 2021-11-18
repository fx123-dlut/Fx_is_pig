import os
import re


def print_all_file_path(init_file_path, keyword):
    res = []
    for cur_dir, sub_dir, included_file in os.walk(init_file_path):
        if included_file:
            for file in included_file:
                if re.search(keyword, file):
                    file_path = cur_dir + "\\" + file
                    # print(file_path)
                    res.append(file_path.replace('\\','/'))
    return res


def get_all_file_path(file_path,file_type):
    return print_all_file_path(file_path, '.'+file_type)


if __name__ == '__main__':
    get_all_file_path("E:\projects\git\java\cayenne","java")