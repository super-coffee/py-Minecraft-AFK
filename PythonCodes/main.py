# coding: UTF-8
import os
import time
import threading
# 导入win32api
from win32 import win32api, win32gui
from win32.lib import win32con
# 导入进度条相关
from tqdm import tqdm
from progress.spinner import Spinner
# 导入操作相关模块
import configs
from hardware import Mouse, Keyboard
from universal_function import stop, KD0, KD1, KD2


# 主类
class AFK():
	hwnds_list_of_taegets = list()  # 无法获取返回值，只能全局变量
	KEYWORD = 'Minecraft'  # 窗口关键字
	run_status = True  # 这个是CharlieYu定义的可能会删掉

	def __init__(self):  # 开始运行
		os.system('title py-Minecraft-AFK')
		self.main()

	# --------------------------------寻找带关键字的窗口-------------------------------- #
	def get_hwnd_with_keyword(self, hwnd, unused):
		# 是现有窗口 & 启用了窗口 & 窗口具有WS_VISIBLE样式（非隐藏） & 窗口标题包含关键字
		if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(
				hwnd) and win32gui.GetWindowText(hwnd).startswith(self.KEYWORD):
			self.hwnds_list_of_taegets.append({
				'title': win32gui.GetWindowText(hwnd),  # 窗口标题
				'hwnd': hwnd  # 句柄 ID
			})

	# --------------------------------寻找所有窗口------------------------------------- #
	def get_all_hwnd(self, hwnd, unused):  # 寻找所有窗口
		# 是现有窗口 & 启用了窗口 & 窗口具有WS_VISIBLE样式（非隐藏）
		if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
			title = win32gui.GetWindowText(hwnd)
			# 加入列表
			self.hwnds_list_of_taegets.append({
				'title': '* 无标题' if title == '' else title,  # 窗口标题
				'hwnd': hwnd  # 句柄 ID
			})

	# ---------------------------------枚举窗口--------------------------------------- #
	def layout_hwnd_list(self, hwnds_count):  # 输出窗口标题 & 句柄
		for hwnd_index_id in range(hwnds_count):  # 需要获取 index，因此通过序列索引迭代
			item = self.hwnds_list_of_taegets[hwnd_index_id]
			print('[{index}] {title}, {hwnd}'.format(index=hwnd_index_id, title=item['title'], hwnd=item['hwnd']))

	def do_job(self, callback, loop_times):
		# ----------------------------------检测alt---------------------------------- #
		if self.run_status:
			print('>>>  在此窗口按下 ctrl+c 终止运行  <<<')
			print('>>> 在任何地方按下 右alt键 开始操作 <<<')
			print('>>>在任何窗口按右ctrl暂停，右alt恢复<<<')
			while True:
				time.sleep(0.001)
				rmenu_status = win32api.GetAsyncKeyState(win32con.VK_RMENU)
				if rmenu_status == KD0 or rmenu_status == KD1 or rmenu_status == KD2:
					self.run_status = False
					os.system('cls')
					print('开始运行')
					break
		# --------------------------------运行检测循环次数------------------------------ #
		if loop_times == -1:  # =-1则无限循环
			spinner = Spinner('Running   ')
			count = 0
			while True:
				count = count + 1
				callback(callback=stop, args=[win32con.VK_RCONTROL, win32con.VK_RMENU])
				if count == 20:
					spinner.next()
					count = 0
		else:  # 否则运行loop_times次
			for _ in tqdm(range(loop_times), ascii=True):
				callback(callback=stop, args=[win32con.VK_RCONTROL, win32con.VK_RMENU])

	# --------------------------------分流所有指令------------------------------------- #
	def classify(self, hwnd, step):
		for cfg in step:
			op_levels = cfg['op_type'].split('.')
			hardware = op_levels[0]
			operation = op_levels[1]
			if hardware == 'mouse':
				call_func = Mouse(hwnd, cfg['keys'], cfg['up_time'], cfg['down_time'])
				if operation == 'press':
					self.do_job(call_func.press, cfg['loop_times'])
				elif operation == 'move':
					self.do_job(call_func.move, cfg['loop_times'])
			elif hardware == 'keyboard':
				call_func = Keyboard(hwnd, cfg['keys'], cfg['up_time'], cfg['down_time'])
				if operation == 'input':
					self.do_job(call_func.operate, cfg['loop_times'])
				elif operation == 'str':
					self.do_job(call_func.sendstr, cfg['loop_times'])

	def main(self):
		# ----------------------------------窗口句柄部分---------------------------------- #
		win32gui.EnumWindows(self.get_hwnd_with_keyword, None)  # 枚举屏幕上所有的顶级窗口，第一个参数为 call_func，第二个没啥用。得到关键字窗口
		hwnds_count = len(self.hwnds_list_of_taegets)
		# 根据符合关键字的窗口数量分别引导用户
		if hwnds_count == 1:  # 不让用户进行选择
			user_input_index_id = 0
		elif hwnds_count > 1:  # 有含关键字的窗口
			self.layout_hwnd_list(hwnds_count)
			user_input_index_id = int(input('请输入序号以选择窗口 >>>'))
		else:
			print('未找到含 \"{keyword}\" 的窗口，请选择你需要 AFK 的窗口'.format(keyword=self.KEYWORD))
			win32gui.EnumWindows(self.get_all_hwnd, None)  # 枚举屏幕上所有的顶级窗口，第一个参数为 call_func，第二个没啥用。得到所有窗口
			hwnds_count = len(self.hwnds_list_of_taegets)
			self.layout_hwnd_list(hwnds_count)
			user_input_index_id = int(input('请输入序号以选择窗口 >>>'))

		HWND = self.hwnds_list_of_taegets[user_input_index_id]['hwnd']

		os.system('cls')  # 清空屏幕

		# ----------------------------------配置文件部分---------------------------------- #
		config_list = configs.find('../configs/', '.json')
		if len(config_list):
			for index in range(len(config_list)):
				print('[%s] %s' % (index, config_list[index]['name']))
			index = int(input('请输入要读取的配置序号，若为-1则创建新的配置>>>'))
			if index == -1:
				cfgs = configs.generate_config()
			else:
				cfgs = configs.read(config_list[index]['path'])
		else:
			print('未发现配置文件，请按提示创建配置文件')
			cfgs = configs.generate_config()

		# ----------------------------------分流部分------------------------------------- #
		for config_per_step in cfgs:
			# 动作并发
			if 'multi' in config_per_step.keys():
				pass
			# 动作依次执行
			elif 'class' in config_per_step.keys():
				step = config_per_step['class']
				loop_times = config_per_step['loop_times']
				for _ in range(loop_times):
					self.classify(HWND, step)
		input('运行完成，按回车退出')


if __name__ == '__main__':
	AFK()
