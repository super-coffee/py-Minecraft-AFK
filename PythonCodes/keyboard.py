import time
import os
import win32api, win32con
from universal_function import get_lparam
from universal_function import _do_postmessage
from universal_function import default_callback
from universal_function import nonblocking_delay


class Keyboard:
	# --------------------------------定义一些变量------------------------------------- #
	hwnd = None
	keys = None
	delay_time = None
	during_time = None

	# --------------------------------初始化传入参数----------------------------------- #
	def __init__(self, hwnd, keys, delay_time, during_time):
		self.hwnd = hwnd  # 获取句柄和按键
		self.keys = keys
		self.delay_time = delay_time
		self.during_time = during_time

	# ---------------------------------按键操作--------------------------------------- #
	def operate(self, callback=default_callback, args=None):  # 传入两个参数，是否为回车和是否为按下按键
		VkKeyCode = win32api.VkKeyScan(self.keys[0])  # 获得按键的虚拟键值
		_do_postmessage(self.hwnd, VkKeyCode, self.during_time, self.delay_time, callback, args)

	# ---------------------------------发送字符--------------------------------------- #
	def sendstr(self, callback=default_callback, args=None):
		args.append(0), args.append(0), args.append(True)
		os.popen(f"..\\plugins\\CLIPBOARD.exe {self.keys}")
		while True:
			callback(args)
			time.sleep(0.01)
			end = time.time()
			if end - start >= self.delay_time:
				break


if __name__ == "__main__":
	pass
