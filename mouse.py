import math
import time

import win32api
import win32con
import win32gui


def _get_pos_bin(x, y):
    return (y << 16) | x


def move(self, distance, degree, time_usage=5, step=4):
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
    during_time = None
    delay_time = None
    click_sign = False
    is_right = True

    def __init__(self, hwnd, delay_time, during_time, is_right):
        self.hwnd = hwnd
        self.delay_time = delay_time
        self.during_time = during_time  # 对照键盘操作
        self.click_sign = True if during_time > 0 else False
        self.is_right = is_right

    def _get_client_center_pos(self):
        x1, x2, y1, y2 = win32gui.GetClientRect(self.hwnd)
        average_x = round((x1 + y1) / 2)
        average_y = round((x2 + y2) / 2)
        return _get_pos_bin(average_x, average_y)

    def left(self, pos):  # 右键点击
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, pos)
        time.sleep(self.during_time)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, pos)
        time.sleep(self.delay_time)

    def right(self, pos):  # 左键点击
        win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONDOWN, 0, pos)
        time.sleep(self.during_time)
        win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONUP, 0, pos)
        time.sleep(self.delay_time)

    def operate(self, is_up=False):
        pos = self._get_client_center_pos()  # 获取客户端中心坐标
        if self.click_sign and self.is_right:
            self.right(pos)
        elif self.click_sign and not self.is_right:
            self.left(pos)
        elif not self.click_sign and self.is_right:
            if is_up:
                win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONUP, 0, pos)
            else:
                win32api.PostMessage(
                    self.hwnd, win32con.WM_RBUTTONDOWN, 0, pos)
        else:
            if is_up:
                win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONUP, 0, pos)
            else:
                win32api.PostMessage(
                    self.hwnd, win32con.WM_RBUTTONDOWN, 0, pos)



if __name__ == '__main__':  # DEBUG
    # time.sleep(5)
    # move(500, 90, 5, 4)
    pass
