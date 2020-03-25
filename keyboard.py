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
        self.hwnd = hwnd
        self.keys = keys

    def keydown(self):
        for key in self.keys:
            # 得到 wparam
            VkKeyCode = win32api.VkKeyScan(key)
            # 得到 lparam
            lparamDown = _get_lparam(VkKeyCode, False)
            # PostMessage
            win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, VkKeyCode, lparamDown)
            time.sleep(0.0001)

    def keyup(self):
        for key in self.keys:
        # 得到 wparam
            VkKeyCode = win32api.VkKeyScan(key)
            # 得到 lparam
            lparamUp = _get_lparam(VkKeyCode, True)
            # PostMessage
            win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, VkKeyCode, lparamUp)
            time.sleep(0.0001)




def enter(hwnd):
    # 得到 wparam
    wparam = win32con.VK_RETURN
    # 得到 lparam
    lparam = _get_lparam(wparam, False)
    # PostMessage
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, wparam, lparam)
