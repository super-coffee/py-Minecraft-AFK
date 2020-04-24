import os
import json
import uuid


# -------------------------------寻找指定后缀文件------------------------------------ #
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


# --------------------------------读取配置文件------------------------------------- #
def read(file_name):
	with open(file_name, 'r') as config_file:
		contents = config_file.read()
	config = json.loads(contents)
	return config


# --------------------------------包装配置文件------------------------------------- #
def pack(operate, during_time, delay_time, loop_times, keys, op_list):
	op_list.append({
		"op_type": operate,
		"loop_times": loop_times,
		"down_time": during_time,
		"up_time": delay_time,
		'keys': keys
	})
	return op_list


# --------------------------------生成配置文件------------------------------------- #
def generate_config():
	li, final_config = list(), list()
	while True:
		hardware = 'keyboard.' if input('是否为键盘操作，否则为鼠标操作(Y/N)>>>').lower() == 'y' else 'mouse.'
		if hardware == 'keyboard.':
			operate = 'input' if input('是否为按键操作，否则为发送字符(Y/N)').lower() == 'y' else 'str'
			final_operate = hardware + operate
			if operate == 'input':
				delay_time = float(input('请输入按键抬起持续时间>>>'))
				during_time = float(input('请输入按键按下时间>>>'))
				keys = input('请输入按键，若输入多个按键则只按第一个按键>>>')
				loop_times = int(input('请输入重复次数，若为-1，则无限重复>>>')) if delay_time else -1
				pack(final_operate, during_time, delay_time, loop_times, keys, li)
			else:
				delay_time = float(input('输入间隔时间>>>'))
				keys = input('请输入内容>>>')
				loop_times = int(input('请输入重复次数，若为-1，则无限重复>>>'))
				pack(final_operate, 0, delay_time, loop_times, keys, li)
		else:
			operate = 'press' if input('是否为按键操作，否则为鼠标移动(Y/N)>>>').lower() == 'y' else 'move'
			final_operate = hardware + operate
			if operate == 'press':
				delay_time = float(input('请输入按键抬起持续时间>>>'))
				during_time = float(input('请输入按键按下时间>>>'))
				keys = int(input('请输入按键 ，0为左键，1为右键，2为中键>>>'))
				loop_times = int(input('请输入重复次数，若为-1，则无限重复>>>')) if delay_time else 0
				pack(final_operate, during_time, delay_time, loop_times, keys, li)
			else:
				distance = int(input('请输入光标移动距离>>>'))
				degree = float(input('请输入角度>>>'))
				delay_time = int(input('请输入持续时间，若为零，程序自动设置>>>'))
				loop_times = int(input('请输入重复次数，若为-1，则无限重复>>>'))
				pack(final_operate, distance, degree, loop_times, delay_time, li)
		if input('是否继续输入(Y/N)>>>').lower() == 'n':
			if len(li) <= 1:
				method = 'class'
			else:
				method = 'multi' if input('是否并发动作(Y/N)>>>').lower() == 'y' else 'class'
			repeat_times = int(input('请输入总循环次数>>>'))
			final_config = [{
				method: li,
				'loop_times': repeat_times
			}]
			file_name = uuid.uuid1()
			create_Json(final_config, '../configs/', '{filename}.json'.format(filename=file_name))
			break
	return final_config


# --------------------------------保存配置文件------------------------------------- #
def create_Json(Json, path, name):
	filepath = path+name
	with open(filepath, 'w') as config:
		config.write(json.dumps(Json, indent=4))
		print('已保存至 {filename}'.format(filename=filepath))


if __name__ == '__main__':
	print(generate_config())
