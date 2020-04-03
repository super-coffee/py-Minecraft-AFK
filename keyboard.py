import time
import win32api
import win32con
from universal_function import *


def _get_lparam(wparam, isKeyUp=True):
    scanCode = win32api.MapVirtualKey(wparam, 0)
    repeatCount = 1 if isKeyUp else 0
    prevKeyState = 1 if isKeyUp else 0
    transitionState = 1 if isKeyUp else 0
    return repeatCount | (scanCode << 16) | (0 << 24) | (prevKeyState << 30) | (transitionState << 31)


def do_postmessage(hwnd, VkKeyCode, during_time, delay_time, callback, args):
    lparamUp = _get_lparam(VkKeyCode, True)
    lparamDown = _get_lparam(VkKeyCode, False)
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
            lparam = _get_lparam(VkKeyCode, is_up)  # 计算lparam
            win32api.PostMessage(self.hwnd, msg, VkKeyCode, lparam)
        elif not self.click_sign and not self.is_enter:
            for key in self.keys:  # 遍历keys，操作所有定义的按键
                VkKeyCode = win32api.VkKeyScan(key)  # 获得按键的虚拟键值
                lparam = _get_lparam(VkKeyCode, is_up)  # 接下来大同小异
                win32api.PostMessage(self.hwnd, msg, VkKeyCode, lparam)
        elif self.click_sign and self.is_enter:
            VkKeyCode = win32con.VK_RETURN  # 赋值回车的虚拟键值
            do_postmessage(self.hwnd, VkKeyCode, self.during_time, self.delay_time, callback, args)
        else:
            for key in self.keys:  # 遍历keys，操作所有定义的按键
                VkKeyCode = win32api.VkKeyScan(key)  # 获得按键的虚拟键值
                do_postmessage(self.hwnd, VkKeyCode, self.during_time, self.delay_time, callback, args)

    def sendstr(self):
        for key in self.keys:
            VkKeyCode = win32api.VkKeyScan(key)
            win32api.PostMessage(self.hwnd, 0, VkKeyCode, 0)
            time.sleep(self.delay_time)


if __name__ == "__main__":
    # KeyOperate().key()
    pass
