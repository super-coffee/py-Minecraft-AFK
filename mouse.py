import math
import time

import win32api
import win32con
import win32gui


def _get_client_center_pos(hwnd):
    x1, x2, y1, y2 = win32gui.GetClientRect(hwnd)
    average_x = round((x1 + y1) / 2)
    average_y = round((x2 + y2) / 2)
    return _get_pos_bin(average_x, average_y)


def _get_pos_bin(x, y):
    return (y << 16) | x


def left(hwnd, during_time, delay_time, pos):
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, pos)
    time.sleep(during_time)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, pos)
    time.sleep(delay_time)


def right(hwnd, during_time, delay_time, pos):
    win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 0, pos)
    time.sleep(during_time)
    win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, pos)
    time.sleep(delay_time)


def move(hwnd, direction, speed, delay_time):  # TODO
    # win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, _get_pos_bin(1366, 768))
    print(bin(_get_pos_bin(20, 20)))
    print(win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE,
                               win32con.MK_LBUTTON, _get_pos_bin(20, 20)))
    print(win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE,
                               win32con.MK_LBUTTON, _get_pos_bin(50, 20)))


def moving(distance, degree, time_usage=5, step=4):
    mousepos = list(win32api.GetCursorPos())  # 获得mc的基准光标
    deta_X = int(step * math.sin(math.radians(degree)))
    deta_Y = int(step * math.cos(math.radians(degree)))
    # 根据用户给定的角度和步进计算出每一步再xy轴上要移动的距离分量
    repeat_times = int((distance * 2) / step) + 1 if int((distance * 2) / step) % 2 else int((distance * 2) / step)
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


def press(hwnd, button, during_time, delay_time):
    pos = _get_client_center_pos(hwnd)
    if button == 'left':
        left(hwnd, during_time, delay_time, pos)
    elif button == 'right':
        right(hwnd, during_time, delay_time, pos)


if __name__ == '__main__':  # DEBUG
    time.sleep(5)
    moving(500, 90, 5, 4)
