# coding: UTF-8
# https://github.com/jinzhijie/py-Minecraft-AFK
import os
import time

import win32api
import win32con
import win32gui
from tqdm import tqdm
from progress.spinner import Spinner

from keyboard import Keyboard
import keyboard
import mouse


class AFK():
    hwnds_list_of_taegets = list()  # 无法获取返回值，只能全局变量
    KEYWORD = 'Minecraft'
    operation_list = [
        {'type': 'mouse.left', 'description': '鼠标左键'},
        {'type': 'mouse.right', 'description': '鼠标右键'},
        {'type': 'mouse.move', 'description': '鼠标移动（不可用）'},
        {'type': 'keyboard.input', 'description': '键盘按键'},
        {'type': 'keyboard.str', 'description': '发送字符'}
    ]

    def __init__(self):
        os.system('title py-Minecraft-AFK')
        self.main()

    def get_hwnd_with_keyword(self, hwnd, unused):
        # 是现有窗口 & 启用了窗口 & 窗口具有WS_VISIBLE样式（非隐藏） & 窗口标题包含关键字
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(
                hwnd) and win32gui.GetWindowText(hwnd).startswith(self.KEYWORD):
            self.hwnds_list_of_taegets.append({
                'title': win32gui.GetWindowText(hwnd),  # 窗口标题
                'hwnd': hwnd  # 句柄 ID
            })

    def get_all_hwnd(self, hwnd, unused):
        # 是现有窗口 & 启用了窗口 & 窗口具有WS_VISIBLE样式（非隐藏）
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            # 加入列表
            self.hwnds_list_of_taegets.append({
                'title': '* 无标题' if title == '' else title,  # 窗口标题
                'hwnd': hwnd  # 句柄 ID
            })

    def layout_hwnd_list(self, hwnds_count):  # 输出窗口标题 & 句柄
        for hwnd_index_id in range(hwnds_count):  # 需要获取 index，因此通过序列索引迭代
            item = self.hwnds_list_of_taegets[hwnd_index_id]
            print('[{index}] {title}, {hwnd}'.format(index=hwnd_index_id, title=item['title'], hwnd=item['hwnd']))

    def do_job(self, call_func, args, loop_times):
        has_key_down_0 = -0b1000000000000000
        has_key_down_1 = -0b111111111111111
        key_down = 0b1

        print('>>> 在此窗口按下 ctrl+c 终止运行 <<<')
        print('>>> 在任何地方按下 右alt键 开始操作 <<<')
        while True:
            time.sleep(0.001)  # 不设延时吃 CPU
            rmenu_status = win32api.GetAsyncKeyState(win32con.VK_RMENU)
            if rmenu_status == has_key_down_0 or rmenu_status == has_key_down_1 or rmenu_status == key_down:
                if not loop_times == 0:
                    for _ in tqdm(range(loop_times), ascii=True):  # ascii=True 可防止多行进度条，loop_time 太大直接就炸
                        call_func(*args)
                    input('>>> 完成，按下回车退出 <<<')
                    break
                else:  # 无限循环
                    spinner = Spinner('正在执行     ')  # 空格防止奇怪的事发生
                    while True:
                        time.sleep(0.001)  # 不设延时吃 CPU
                        rctrl_status = win32api.GetAsyncKeyState(win32con.VK_RCONTROL)
                        spinner.next()
                        call_func(*args)
                        if rctrl_status == has_key_down_0:
                            break

    def classify(self, user_op_type, hwnd):
        op_levels = user_op_type.split('.')
        hardware = op_levels[0]
        operation = op_levels[1]

        loop_times = int(input("重复次数，0为无限重复 >>>"))
        during_time = float(input('操作时间（秒） >>>'))
        delay_time = float(input('延时（秒） >>>'))
        if hardware == 'mouse':
            if operation == 'right':
                self.do_job(mouse.right, (hwnd, during_time, delay_time), loop_times)
            elif operation == 'left':
                self.do_job(mouse.left, (hwnd, during_time, delay_time), loop_times)
            elif operation == 'move':
                distance = int(input('distance >>>'))
                degree = int(input('degree >>>'))
                self.do_job(mouse.move, (distance, degree), loop_times)
        elif hardware == 'keyboard':
            if operation == 'input':
                keys = input('请输入你的按键 >>>')
                is_enter = True if input('是否为回车(Y/N)').lower() == 'y' else False
                if is_enter:
                    call_func = Keyboard(hwnd, keys, delay_time, during_time, True)
                    self.do_job(call_func.operate, loop_times)
                    self.do_job(mouse.move, (distance, degree), loop_times)
                else:
                    call_func = Keyboard(hwnd, keys, delay_time, during_time, False)
                    self.do_job(call_func.operate, loop_times)
            elif operation == 'str':
                keys = input('请输入你的按键 >>>')
                call_func = Keyboard(hwnd, keys, delay_time, during_time, False)
                self.do_job(call_func.sendstr, loop_times)

    def main(self):
        win32gui.EnumWindows(self.get_hwnd_with_keyword, None)  # 枚举屏幕上所有的顶级窗口，第一个参数为 call_func，第二个没啥用。得到关键字窗口
        hwnds_count = len(self.hwnds_list_of_taegets)
        # 根据符合关键字的窗口数量分别引导用户
        if hwnds_count == 1:  # 不让用户进行选择
            user_input_index_id = 0
        elif hwnds_count > 1:  # 有含关键字的窗口
            self.layout_hwnd_list(hwnds_count)
            user_input_index_id = int(input('请输入序号以选择窗口 >>>'))
        else:
            print('未找到含 \"{keyword}\" 的窗口，请选择你需要 AFK 的窗口'.format(keyword=self.KEYWORD))
            win32gui.EnumWindows(self.get_all_hwnd, None)  # 枚举屏幕上所有的顶级窗口，第一个参数为 call_func，第二个没啥用。得到所有窗口
            hwnds_count = len(self.hwnds_list_of_taegets)
            self.layout_hwnd_list(hwnds_count)
            user_input_index_id = int(input('请输入序号以选择窗口 >>>'))

        HWND = self.hwnds_list_of_taegets[user_input_index_id]['hwnd']

        os.system('cls')  # 清空屏幕
        print('{title}, {hwnd}'.format(title=self.hwnds_list_of_taegets[user_input_index_id]['title'],
                                       hwnd=self.hwnds_list_of_taegets[user_input_index_id]['hwnd']))

        op_len = len(self.operation_list)
        for op_index in range(op_len):
            print('[{index}] {description}'.format(index=op_index,
                                                   description=self.operation_list[op_index]['description']))

        user_input_op = self.operation_list[int(input('请选择你要进行的操作 >>>'))]
        user_input_op_type = user_input_op['type']
        self.classify(user_input_op_type, HWND)


if __name__ == '__main__':
    AFK()
