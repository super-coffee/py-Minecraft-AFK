import time
import win32api
import win32con
from universal_function import *


def _do_postmessage(hwnd, VkKeyCode, during_time, delay_time, callback, args):
    lparamUp = get_lparam(VkKeyCode, True)
    lparamDown = get_lparam(VkKeyCode, False)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, VkKeyCode, lparamDown)
    nonblocking_delay(during_time, callback, args)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, VkKeyCode, lparamUp)
    nonblocking_delay(delay_time, callback, args)


class Keyboard:
    hwnd = None
    keys = None
    delay_time = None
    during_time = None
    click_sign = False
    is_enter = False

    def __init__(self, hwnd, keys, delay_time, during_time, is_enter):
        self.hwnd = hwnd  # 获取句柄和按键
        self.keys = keys
        self.delay_time = delay_time
        self.during_time = during_time
        self.is_enter = is_enter
        self.click_sign = True if during_time > 0 else False

    def operate(self, is_up=False, callback=default_callback, args=None):  # 传入两个参数，是否为回车和是否为按下按键
        msg = win32con.WM_KEYUP if is_up else win32con.WM_KEYDOWN
        # 根据输入得出wparam
        if not self.click_sign and self.is_enter:
            VkKeyCode = win32con.VK_RETURN  # 赋值回车的虚拟键值
            lparam = get_lparam(VkKeyCode, is_up)  # 计算lparam
            win32api.PostMessage(self.hwnd, msg, VkKeyCode, lparam)
            args.append((self.hwnd, win32con.WM_KEYUP, VkKeyCode, get_lparam(VkKeyCode, True)))
            stop(args)
        elif not self.click_sign and not self.is_enter:
            for key in self.keys:  # 遍历keys，操作所有定义的按键
                VkKeyCode = win32api.VkKeyScan(key)  # 获得按键的虚拟键值
                lparam = get_lparam(VkKeyCode, is_up)  # 接下来大同小异
                win32api.PostMessage(self.hwnd, msg, VkKeyCode, lparam)
                args.append((self.hwnd, win32con.WM_KEYUP, VkKeyCode, get_lparam(VkKeyCode, True)))
                stop(args)
        elif self.click_sign and self.is_enter:
            VkKeyCode = win32con.VK_RETURN  # 赋值回车的虚拟键值
            args.append((self.hwnd, win32con.WM_KEYUP, VkKeyCode, get_lparam(VkKeyCode, True)))
            _do_postmessage(self.hwnd, VkKeyCode, self.during_time, self.delay_time, callback, args)
        else:
            for key in self.keys:  # 遍历keys，操作所有定义的按键
                VkKeyCode = win32api.VkKeyScan(key)  # 获得按键的虚拟键值
                args.append((self.hwnd, win32con.WM_KEYUP, VkKeyCode, get_lparam(VkKeyCode, True)))
                _do_postmessage(self.hwnd, VkKeyCode, self.during_time, self.delay_time, callback, args)

    def sendstr(self):
        for key in self.keys:
            VkKeyCode = win32api.VkKeyScan(key)
            win32api.PostMessage(self.hwnd, 0, VkKeyCode, 0)
            time.sleep(self.delay_time)


if __name__ == "__main__":
    # KeyOperate().key()
    pass
