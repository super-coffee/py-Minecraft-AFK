import os
import time

import win32con
from universal_function import get_client_center_pos
from universal_function import default_callback
from universal_function import do_postmessage


class Mouse:
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
	def press(self, callback=default_callback, args=None):
		pos = get_client_center_pos(self.hwnd)
		if self.keys == 0:
			mouse_key = [win32con.WM_LBUTTONDOWN, win32con.WM_LBUTTONUP]
		elif self.keys == 1:
			mouse_key = [win32con.WM_RBUTTONDOWN, win32con.WM_RBUTTONUP]
		else:
			mouse_key = [win32con.WM_MBUTTONDOWN, win32con.WM_MBUTTONUP]
		do_postmessage(self.hwnd, self.during_time, self.delay_time, mouse_key, pos, callback, args)

	# ---------------------------------移动操作-------------------------------------- #
	def move(self, callback=default_callback, args=None):
		args.append(0), args.append(0), args.append(True)
		os.popen(f"MOUSEMOVE.exe {self.during_time} {self.delay_time} {self.keys} 5")
		start = time.time()
		while True:
			callback(args)
			time.sleep(0.01)
			end = time.time()
			if end - start >= 5:
				break


if __name__ == '__main__':  # DEBUG
	pass
