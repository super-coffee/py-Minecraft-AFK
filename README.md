# py-Minecraft-AFK
![ICON](https://img.xiao-jin.xyz/2020/03/25/07f1e7d0de1f6.png)  
![Python3](https://img.shields.io/badge/Python-3.7+-blue?color=3776AB&&logo=python) ![GPLv3](https://img.shields.io/github/license/jinzhijie/py-Minecraft-AFK) ![GitHub last commit (dev branch)](https://img.shields.io/github/last-commit/jinzhijie/py-Minecraft-AFK/dev) ![Pyinstaller](https://github.com/jinzhijie/py-Minecraft-AFK/workflows/Pyinstaller/badge.svg) ![Dev Code Check](https://github.com/jinzhijie/py-Minecraft-AFK/workflows/Dev%20Code%20Check/badge.svg?branch=dev)

一个基于 win32api 的 Minecraft 的挂机程序，即使失去焦点或最小化依然可以完成鼠标/键盘的动作。  
A win32api-based Minecraft AFK program that can complete mouse / keyboard actions even if it loses focus or is minimized.

---
## 用途
- 挂机钓鱼（最基础简单的挂机方法）
- 挂机刷怪（如小黑塔，刷怪塔）
- 挂机跑图 ~~（虽然你可能会由于某些意外情况惨死在路上）~~
- 挂机完成某些MC工程（如铺铁轨等）

## 如何使用
1. 从 [Releases](https://github.com/jinzhijie/py-Minecraft-AFK/releases) 页面下载合适的版本
2. 双击运行，按提示操作

## 常见问题
### 如何实现后台挂机？
- 用 <kbd>F3</kbd>+<kbd>P</kbd> 停用失去焦点后暂停，接着按 <kbd>alt</kbd>+<kbd>tab</kbd> 切出

### 如何挂机完成多项操作
- 此功能将会在以后实现

## 关于反馈
如果你发现了程序的bug，你可以在 [Issues](https://github.com/jinzhijie/py-Minecraft-AFK/issues/new) 中反馈

## 已知问题
- 从 Minecraft 1.13 开始，Mojang 对准心跟随光标机制做出了破坏性的修改，导致鼠标移动完全无法使用，预计修正时间不明。  
在 Minecraft 1.12.2 及以下，你依然可以使用鼠标移动，但必须保证焦点在 Minecraft 窗口

## 其他版本
| 编写语言 | 项目地址 |
| ---- | ---- |
| C++ | [Cheny233/Minecraft-AFK](https://github.com/Cheny233/Minecraft-AFK) |

## Language localization
We welcome your post-contribution to language localization. You can open a new [Pull Requests](https://github.com/jinzhijie/py-Minecraft-AFK/pulls) to us.
