# 调试用途代码
import win32con
import win32gui

hwnds_list_of_taegets = list()


def get_all_hwnd(hwnd, unused):
	global hwnds_list_of_taegets
	# 是现有窗口 & 启用了窗口 & 窗口具有WS_VISIBLE样式（非隐藏）
	if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
		title = win32gui.GetWindowText(hwnd)
		# 加入列表
		hwnds_list_of_taegets.append({
			'title': '* 无标题' if title == '' else title,  # 窗口标题
			'hwnd': hwnd  # 句柄 ID
		})


win32gui.EnumWindows(get_all_hwnd, None)

hwnds_count = len(hwnds_list_of_taegets)
for hwnd_index_id in range(hwnds_count):  # 通过序列索引迭代
	item = hwnds_list_of_taegets[hwnd_index_id]
	print('[{hwnd}] {title}'.format(title=item['title'], hwnd=item['hwnd']))

input()
