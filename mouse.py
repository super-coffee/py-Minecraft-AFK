import win32api
import win32con
import win32gui
import time
import math


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
    print(win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, _get_pos_bin(20, 20)))
    print(win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, _get_pos_bin(50, 20)))


def smooth_move(distance, degree, time_usage=5, step=4):
    mousepos = list(win32api.GetCursorPos())
    deta_X = int(step * math.sin(math.radians(degree)))
    deta_Y = int(step * math.cos(math.radians(degree)))
    repeat_times = int((distance*2) / step) + 1 if int((distance*2) / step) % 2 else int((distance*2) / step)
    time_each_repetition = time_usage / repeat_times
    mouse_pos_one = [mousepos[0] + deta_X, mousepos[1] + deta_Y]
    mouse_pos_two = [mousepos[0] - deta_X, mousepos[1] - deta_Y]
    count, sign = repeat_times, 1
    correct = 0.001
    while count:
        if sign:
            start = time.time()
            win32api.SetCursorPos(mouse_pos_one)
            count -= 1
            if count == int((repeat_times / 4)*3):
                sign = 0
            end = time.time()
            time_use = end - start
            time.sleep(time_each_repetition -time_use - correct)
        else:
            start = time.time()
            win32api.SetCursorPos(mouse_pos_two)
            count -= 1
            if count == int(repeat_times / 4):
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
    # move(197668, 0, 0, 0)
    smooth_move(100, 700)
