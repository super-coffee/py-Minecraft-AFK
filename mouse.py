import win32api
import win32con
from universal_function import get_client_center_pos
from universal_function import default_callback
from universal_function import do_postmessage


class Mouse:
    hwnd = None
    keys = None
    delay_time = None
    during_time = None
    click_sign = False

    def __init__(self, hwnd, keys, delay_time, during_time):
        self.hwnd = hwnd  # 获取句柄和按键
        self.keys = keys
        self.delay_time = delay_time
        self.during_time = during_time
        self.click_sign = True if during_time > 0 else False

    def press(self, is_up=False, callback=default_callback, args=None):
        pos = get_client_center_pos(self.hwnd)
        index = 1 if is_up else 0
        if self.keys == 0:
            mouse_key = [win32con.WM_LBUTTONDOWN, win32con.WM_LBUTTONUP]
        elif self.keys == 1:
            mouse_key = [win32con.WM_RBUTTONDOWN, win32con.WM_RBUTTONUP]
        else:
            mouse_key = [win32con.WM_MBUTTONDOWN, win32con.WM_MBUTTONUP]
        if self.click_sign:
            args.append((self.hwnd, mouse_key[1], 0, pos))
            do_postmessage(self.hwnd, self.during_time, self.delay_time, mouse_key, pos, callback, args)
        else:
            win32api.PostMessage(self.hwnd, mouse_key[index], 0, pos)

    def move(self, is_up=False, callback=default_callback, args=None):
        pass


if __name__ == '__main__':  # DEBUG
    pass
