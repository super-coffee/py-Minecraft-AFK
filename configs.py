import os
import json


def find(path, suffix):
    file_list = list()
    key_len = len(suffix)
    for _, _, files in os.walk(path):
        for name in files:
            if name[0-key_len:] == suffix:  # 判断后缀名是否匹配
                file_path = os.path.join(path, name)
                file_list.append(file_path)
    return file_list


def read(file_name):
    with open(file_name, 'r') as config_file:
        contents = config_file.read()
    config = json.loads(contents)
    return config

def parser():
    pass

if __name__ == '__main__':
    suffix = '.json'
    a = find('./configs/', suffix)
    print(a)
