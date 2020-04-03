import time

import win32api
import win32gui


KD0 = -0b1000000000000000
KD1 = -0b111111111111111
KD2 = 0b1


def default_callback():
    pass


# oh，你要延迟，要不我们喝杯咖啡吧（大雾
# tips：请勿往里面传要阻塞的函数，否则你会误了正事儿的（大雾
def nonblocking_delay(delay_time, callback, args):
    start = time.time()
    while True:
        callback(args)
        now = time.time()
        if now - start >= delay_time:
            break


def get_client_center_pos(hwnd):
    x1, x2, y1, y2 = win32gui.GetClientRect(hwnd)
    average_x = round((x1 + y1) / 2)
    average_y = round((x2 + y2) / 2)
    return get_pos_bin(average_x, average_y)


def get_pos_bin(x, y):
    return (y << 16) | x


def do_postmessage(hwnd, during_time, delay_time, key, pos, callback, args):
    win32api.PostMessage(hwnd, key[0], 0, pos)
    nonblocking_delay(during_time, callback, args)
    win32api.PostMessage(hwnd, key[1], 0, pos)
    nonblocking_delay(delay_time, callback, args)


def get_lparam(wparam, isKeyUp=True):
    scanCode = win32api.MapVirtualKey(wparam, 0)
    repeatCount = 1 if isKeyUp else 0
    prevKeyState = 1 if isKeyUp else 0
    transitionState = 1 if isKeyUp else 0
    return repeatCount | (scanCode << 16) | (0 << 24) | (prevKeyState << 30) | (transitionState << 31)


def stop(arg):
    key_status = win32api.GetAsyncKeyState(arg[0])
    if key_status == KD1:
        win32api.PostMessage(*arg[1])
        while True:
            key_status = win32api.GetAsyncKeyState(arg[0])
            if key_status == KD1:
                break



