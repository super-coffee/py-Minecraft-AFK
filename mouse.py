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


def smooth_move(distance, degrees, used_time=5, step=2):
    mouse_pos_tmp = list(win32api.GetCursorPos())
    mouse_pos_tmp1 = [0, 0]
    mouse_pos_tmp2 = [0, 0]
    times = int((distance*2)/step)*4
    time_each_turn = used_time / times
    x_weight = int(step * math.sin(degrees))
    y_weight = int(step * math.cos(degrees))
    mouse_pos_tmp1[0] = mouse_pos_tmp[0] + x_weight
    mouse_pos_tmp1[1] = mouse_pos_tmp[1] + y_weight
    mouse_pos_tmp2[0] = mouse_pos_tmp[0] - x_weight
    mouse_pos_tmp2[1] = mouse_pos_tmp[1] - y_weight
    sign, count = 0, 0
    print(times) ###
    c = 0 ###
    a = time.time() ###
    for _ in range(times):
        if sign == 0:
            start = time.time()
            count += 1
            print(mouse_pos_tmp1)  ###
            win32api.SetCursorPos(mouse_pos_tmp1)
            c += 1 ###
            if count == int(times / 4):
                sign, count = 1, 0
            end = time.time()
            time.sleep(time_each_turn - end + start-0.001)
        else:
            start = time.time()
            count += 1
            print(mouse_pos_tmp2)
            win32api.SetCursorPos(mouse_pos_tmp2)
            c += 1 ###
            if count == int(times / 2):
                sign, count = 0, 0
            end = time.time()
            time.sleep(time_each_turn - end + start-0.001)
    print(c) ###
    b = time.time() ###
    print(b - a) ###


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
