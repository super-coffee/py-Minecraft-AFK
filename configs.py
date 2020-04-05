import os
import json
import uuid


def find(path, suffix):
    config_list = list()
    for filename in os.listdir(path):
        if filename.endswith(suffix):
            _path = path + filename
            name = filename.rstrip(suffix)
            config_list.append({
                'name': name,
                'path': _path
            })
    return config_list


def read(file_name):
    with open(file_name, 'r') as config_file:
        contents = config_file.read()
    config = json.loads(contents)
    return config


def pack(operate, during_time, delay_time, loop_times, keys, op_list):
    op_list.append({
        "op_type": operate,
        "loop_times": loop_times,
        "down_time": during_time,
        "up_time": delay_time,
        'keys': keys
    })
    return op_list


def generate_simple_config():
    li = list()
    while True:
        hardware = 'keyboard.' if input('是否为键盘操作，否则为鼠标操作(Y/N)>>>').lower() == 'y' else 'mouse.'
        if hardware == 'keyboard.':
            operate = 'input' if input('是否为按键操作，否则为发送字符(Y/N)').lower() == 'y' else 'str'
            final_operate = hardware + operate
            if operate == 'input':
                delay_time = int(input('请输入按键抬起持续时间，若为0，则长按>>>'))
                during_time = int(input('请输入按键按下时间>>>')) if delay_time else 0
                keys = input('请输入按键，若输入多个按键则一起按下>>>')
                loop_times = int(input('请输入重复次数，若为-1，则无限重复>>>')) if delay_time else 0
                pack(final_operate, during_time, delay_time, loop_times, keys, li)
            else:
                delay_time = int(input('输入间隔时间>>>'))
                keys = input('请输入内容>>>')
                loop_times = int(input('请输入重复次数，若为-1，则无限重复>>>'))
                pack(final_operate, 0, delay_time, loop_times, keys, li)
        else:
            operate = 'press' if input('是否为按键操作，否则为鼠标移动(Y/N)>>>').lower() == 'y' else 'move'
            final_operate = hardware + operate
            if operate == 'press':
                delay_time = int(input('请输入按键抬起持续时间，若为0，则长按>>>'))
                during_time = int(input('请输入按键按下时间>>>')) if delay_time else 0
                keys = int(input('请输入按键 ，0为左键，1为右键，2为中键>>>'))
                loop_times = int(input('请输入重复次数，若为-1，则无限重复>>>')) if delay_time else 0
                pack(final_operate, during_time, delay_time, loop_times, keys, li)
            else:
                during_time = int(input('请输入持续时间，若为零，程序自动设置>>>'))
                degree = int(input('请输入角度>>>'))
                loop_times = int(input('请输入重复次数，若为-1，则无限重复>>>'))
                pack(final_operate, during_time, 0, loop_times, degree, li)
        if input('是否继续输入(Y/N)>>>').lower() == 'n':
            file_name = uuid.uuid1()
            create_Json(li, './configs/', '{filename}.json'.format(filename=file_name))
            break
    return li


def create_Json(Json, path, name):
    filepath = path+name
    with open(filepath, 'w') as config:
        config.write(json.dumps(Json))
        print('已保存至 {filename}'.format(filename=filepath))


if __name__ == '__main__':
    print(generate_simple_config())
