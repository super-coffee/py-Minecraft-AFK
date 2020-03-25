import time
import win32api
import win32con


def _get_lparam(wparam, isKeyUp=True):
    scanCode = win32api.MapVirtualKey(wparam, 0)
    repeatCount = 1 if isKeyUp else 0
    prevKeyState = 1 if isKeyUp else 0
    transitionState = 1 if isKeyUp else 0
    return repeatCount | (scanCode << 16) | (0 << 24) | (prevKeyState << 30) | (transitionState << 31)


class KeyOperate:
    hwnd = None
    keys = None

    def __init__(self, hwnd, keys):
        self.hwnd = hwnd  # 获取句柄和按键
        self.keys = keys

    def key(self, is_enter=False, is_up=False):  # 传入两个参数，是否为回车和是否为按下按键
        wparam = win32con.WM_KEYUP if is_up else win32con.WM_KEYDOWN
        # 根据输入得出wparam
        if is_enter:  # 判断是否为回车
            VkKeyCode = win32con.VK_RETURN  # 赋值回车的虚拟键值
            lparam = _get_lparam(VkKeyCode, is_up)  # 计算lparam
            win32api.PostMessage(self.hwnd, wparam, VkKeyCode, lparam)
            time.sleep(0.001)
        else:
            for key in self.keys:  # 遍历keys，操作所有定义的按键
                VkKeyCode = win32api.VkKeyScan(key)  # 获得按键的虚拟键值
                lparam = _get_lparam(VkKeyCode, is_up)  # 接下来大同小异
                win32api.PostMessage(self.hwnd, wparam, VkKeyCode, lparam)
                time.sleep(0.001)
