import math
import os
import time
import win32api
import win32con
import win32gui

# 这个文件里面包含了很多咖啡可以添加的调料（大雾

# 伪宏定义
KD0 = -0b1000000000000000
KD1 = -0b111111111111111
KD2 = 0b1


def default_callback():
    pass


def release_key(hwnd, VkKeyCode, is_mouse):
    if not is_mouse:
        lparam_up = get_lparam(VkKeyCode)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, VkKeyCode, lparam_up)
    if is_mouse:
        win32api.PostMessage(hwnd, VkKeyCode, 0, 0)


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


# 鼠标专用，有空合并
def do_postmessage(hwnd, during_time, delay_time, key, pos, callback, args):
    sign = True if delay_time else False
    delay = 1 if int(delay_time) == 0 else during_time
    args.append(hwnd), args.append(key[1]), args.append(True)
    win32api.PostMessage(hwnd, key[0], 0, pos)
    nonblocking_delay(delay, callback, args)
    if sign:
        win32api.PostMessage(hwnd, key[1], 0, pos)
        nonblocking_delay(delay_time, callback, args)


# 键盘专用
def _do_postmessage(hwnd, VkKeyCode, during_time, delay_time, callback, args):
    sign = True if delay_time else False
    delay = 1 if int(delay_time) == 0 else during_time
    lparamUp = get_lparam(VkKeyCode, True)
    lparamDown = get_lparam(VkKeyCode, False)
    args.append(hwnd), args.append(VkKeyCode), args.append(False)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, VkKeyCode, lparamDown)
    nonblocking_delay(delay, callback, args)
    if sign:
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, VkKeyCode, lparamUp)
        nonblocking_delay(delay_time, callback, args)


def get_lparam(wparam, isKeyUp=True):
    scanCode = win32api.MapVirtualKey(wparam, 0)
    repeatCount = 1 if isKeyUp else 0
    prevKeyState = 1 if isKeyUp else 0
    transitionState = 1 if isKeyUp else 0
    return repeatCount | (scanCode << 16) | (0 << 24) | (prevKeyState << 30) | (transitionState << 31)


# 暂停用的方法
def stop(arg):
    key_status = win32api.GetAsyncKeyState(arg[0])
    if key_status == KD1:
        win32api.PostMessage(*arg[2])
        release_key(arg[3], arg[4], arg[5])
        print(">>>       已暂停，按alt恢复       <<<")
        while True:
            key_status = win32api.GetAsyncKeyState(arg[1])
            if key_status == KD1:
                os.system('cls')
                print(">>>           恢复运行           <<<")
                break


# 已经废弃准备大改的鼠标移动方法
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
