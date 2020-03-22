import win32api
import win32con
import win32gui
import os
import time


def _get_mouse_xy(x, y):
    return (y << 16) | x


def left(hwnd, during_time, delay_time):
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, _get_mouse_xy(0, 0))
    time.sleep(during_time)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, _get_mouse_xy(0, 0))
    time.sleep(delay_time)


def right(hwnd, during_time, delay_time):
    win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, 0, _get_mouse_xy(0, 0))
    time.sleep(during_time)
    win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, _get_mouse_xy(0, 0))
    time.sleep(delay_time)


def move(hwnd, direction, speed, delay_time):
    print('没写完')


def press(hwnd, button, during_time, delay_time):
    if button == 'left':
        left(hwnd, during_time, delay_time)
    elif button == 'right':
        right(hwnd, during_time, delay_time)
