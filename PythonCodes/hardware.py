import time
import os
import win32api, win32con
from universal_function import get_lparam
from universal_function import _do_postmessage
from universal_function import do_postmessage
from universal_function import default_callback
from universal_function import nonblocking_delay
from universal_function import get_client_center_pos



class hardware:
	"""
	这个是鼠标和键盘的基类
	"""

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


class Keyboard(hardware):
	"""
	这个是键盘用的类

	Init方法的参数:\n
	1.传窗口句柄\n
	2.按键或者要发送的字符串\n
	3.延迟时间或者按键抬起时间\n
	4.按键按下时间
	"""

	# ---------------------------------按键操作--------------------------------------- #
	def operate(self, callback=default_callback, args=None):  # 传入两个参数，是否为回车和是否为按下按键
		VkKeyCode = win32api.VkKeyScan(self.keys[0])  # 获得按键的虚拟键值
		_do_postmessage(self.hwnd, VkKeyCode, self.during_time, self.delay_time, callback, args)

	# ---------------------------------发送字符--------------------------------------- #
	def sendstr(self, callback=default_callback, args=None):
		start = time.time()
		os.system(f"..\\plugins\\CLIPBOARD.exe {self.keys}")
		args.append(0), args.append(0), args.append(True)
		win32api.keybd_event(0x11, 0, 0, 0)
		win32api.keybd_event(0x56, 0, 0, 0)
		time.sleep(0.001)
		win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
		win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
		time.sleep(0.001)
		win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
		win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
		while True:
			callback(args)
			time.sleep(0.01)
			end = time.time()
			if end - start >= self.delay_time:
				break


class Mouse(hardware):
	"""
	这个是键盘用的类

	Init方法的参数:\n
	1.传窗口句柄\n
	2.按键或者完成鼠标一点的用时\n
	3.按键抬起时间或者鼠标移动角度\n
	4.按键按下时间或者鼠标移动距离
	"""

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
		os.popen(f"..\\plugins\\MOUSEMOVE.exe {self.during_time} {self.delay_time} {self.keys} 5")
		start = time.time()
		while True:
			callback(args)
			time.sleep(0.01)
			end = time.time()
			if end - start >= 5:
				break




if __name__ == "__main__":
	pass
