# coding: UTF-8
# https://github.com/jinzhijie/py-Minecraft-AFK
import os
import time

import win32api
import win32con
import win32gui
from tqdm import tqdm
from progress.spinner import Spinner
import configs
from keyboard import Keyboard
from mouse import Mouse
from universal_function import stop, KD0, KD1, KD2


class AFK():
    hwnds_list_of_taegets = list()  # 无法获取返回值，只能全局变量
    KEYWORD = 'Minecraft'
    run_status = True

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

    def do_job(self, callback, loop_times):
        if self.run_status:
            print('>>> 在此窗口按下 ctrl+c 终止运行 <<<')
            print('>>> 在任何地方按下 右alt键 开始操作 <<<')
            while True:
                time.sleep(0.001)
                rmenu_status = win32api.GetAsyncKeyState(win32con.VK_RMENU)
                if rmenu_status == KD0 or rmenu_status == KD1 or rmenu_status == KD2:
                    self.run_status = False
                    break
        for _ in range(loop_times):
            callback(callback=stop, args=[win32con.VK_RCONTROL])

    def classify(self, hwnd, cfg):
        op_levels = cfg['op_type'].split('.')
        hardware = op_levels[0]
        operation = op_levels[1]
        if hardware == 'mouse':
            if operation == 'press':
                call_func = Mouse(hwnd, cfg['keys'], cfg['up_time'], cfg['down_time'])
                self.do_job(call_func.press, cfg['loop_times'])
            elif operation =='move':
                call_func = Mouse(hwnd, cfg['keys'], cfg['up_time'], cfg['down_time'])
                self.do_job(call_func.move, cfg['loop_times'])
        elif hardware == 'keyboard':
            if operation == 'input':
                call_func = Keyboard(hwnd, cfg['keys'], cfg['up_time'], cfg['down_time'], False)
                self.do_job(call_func.operate, cfg['loop_times'])
            elif operation == 'str':
                call_func = Keyboard(hwnd, cfg['keys'], cfg['up_time'], cfg['down_time'], False)
                self.do_job(call_func.sendstr, cfg['loop_times'])

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

        config_list = configs.find('./configs/', '.json')
        if len(config_list):
            for index in range(len(config_list)):
                print('[{index}] {name}'.format(index=index, name=config_list[index]['name']))
            cfgs = configs.read(config_list[int(input('请输入要读取的配置序号>>>'))]['path'])
        else:
            cfgs = configs.generate_simple_config()
        config = cfgs[0]['multi'] if 'class' in cfgs else cfgs[0]['class']
        loop_times = cfgs[0]['loop_times']
        for _ in tqdm(range(loop_times), ascii=True):
            for cfg in config:
                self.classify(HWND, cfg)


if __name__ == '__main__':
    AFK()
