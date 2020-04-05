import math
import time
import win32api
import win32con
from universal_function import get_client_center_pos
from universal_function import default_callback
from universal_function import do_postmessage


def moving(distance, degree, time_usage=5, step=4):
    mousepos = list(win32api.GetCursorPos())  # 获得mc的基准光标
    deta_X = int(step * math.sin(math.radians(degree)))
    deta_Y = int(step * math.cos(math.radians(degree)))
    # 根据用户给定的角度和步进计算出每一步再xy轴上要移动的距离分量
    repeat_times = int((distance * 2) / step) + 1 if int((distance *
                                                          2) / step) % 2 else int((distance * 2) / step)
    # 根据用户给定的距离和步进计算出达成目标需要的移动次数，并尝试让这个数可被2整除
    time_each_repetition = time_usage / repeat_times
    # 根据用户给定的时间和移动次数计算出每一次移动的理论用时
    mouse_pos_one = [mousepos[0] + deta_X, mousepos[1] + deta_Y]
    mouse_pos_two = [mousepos[0] - deta_X, mousepos[1] - deta_Y]
    # 根据基准坐标和移动分量算出两个方向的移动坐标
    count, sign = repeat_times, 1  # count为计数器， sign为方向标志
    correct = 0.001  # 时间的矫正，因为移动光标的用时未知请酌情调整
    while count:  # 但计数器非空时调整鼠标位置
        if sign:  # 如果标志位为1，往one方向移动
            start = time.time()
            win32api.SetCursorPos(mouse_pos_one)
            count -= 1  # 每一次移动计数器减一
            if count == int((repeat_times / 4) * 3):  # 当移动次数只剩总次数的四分之三时把标志位清零
                sign = 0
            end = time.time()
            time_use = end - start  # 计算本次使用的时间
            time.sleep(time_each_repetition - time_use - correct)  # 休眠一段时间
        else:  # 如果标志位为0，往two方向移动
            start = time.time()
            win32api.SetCursorPos(mouse_pos_two)
            count -= 1
            if count == int(repeat_times / 4):  # 大同小异
                sign = 1
            end = time.time()
            time_use = end - start
            time.sleep(time_each_repetition - time_use - correct)


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
