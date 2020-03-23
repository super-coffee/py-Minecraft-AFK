import win32api
import win32con


def _get_lparam(wparam, isKeyUp=True):
    scanCode = win32api.MapVirtualKey(wparam, 0)
    repeatCount = 1 if isKeyUp else 0
    prevKeyState = 1 if isKeyUp else 0
    transitionState = 1 if isKeyUp else 0
    return repeatCount | (scanCode << 16) | (0 << 24) | (prevKeyState << 30) | (transitionState << 31)


def input(hwnd, keys):
    for key in keys:
        # 得到 wparam
        wparam = win32api.VkKeyScan(key)
        # 得到 lparam
        lparam = _get_lparam(wparam, False)
        # PostMessage
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, wparam, lparam)


def enter(hwnd):
    # 得到 wparam
    wparam = win32con.VK_RETURN
    # 得到 lparam
    lparam = _get_lparam(wparam, False)
    # PostMessage
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, wparam, lparam)
