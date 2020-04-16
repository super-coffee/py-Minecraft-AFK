import time
import win32api, win32con
from universal_function import get_lparam
from universal_function import _do_postmessage
from universal_function import default_callback


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
		args.append((self.hwnd, win32con.WM_KEYUP, VkKeyCode, get_lparam(VkKeyCode, True)))
		_do_postmessage(self.hwnd, VkKeyCode, self.during_time, self.delay_time, callback, args)

	# ---------------------------------发送字符--------------------------------------- #
	# 已废弃，待修改
	def sendstr(self, is_up=False, callback=default_callback, args=None):
		for key in self.keys:
			VkKeyCode = win32api.VkKeyScan(key)
			win32api.PostMessage(self.hwnd, 0, VkKeyCode, 0)
			time.sleep(self.delay_time)


if __name__ == "__main__":
	pass
