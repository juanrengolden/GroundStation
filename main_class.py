import tkinter as tk
import subprocess
import threading
import socket
import time
import pickle
import matplotlib
import os

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Thread_Class import MyThread
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from geoMap_Class import TDT_vec, TDT_img, TDT_ter
from data_class import data_class


## 整个main函数，用于生成各空间以及传递相关参数
class main_Class:
    def __init__(self, root):
        # 初始化，因此只运行一次
        self.root = root
        self.root.title("人机地面站0.9 —— By JuanRen")  # 设置窗口标题
        self.root.geometry("1400x630")  # 设置窗口大小
        self.font_style = '宋体'  # 通用字体

        '''
        1. 构建一个容器用于放置状态栏
        '''
        # 创建一个容器
        self.Frame_State = tk.Frame(root, bd=4, relief="groove")
        self.Frame_State.place(x=0, y=70)
        # 创建一个说明
        self.Label_State = tk.Label(self.Frame_State, text="状态显示栏", fg='black', font=(self.font_style, 10))
        self.Label_State.pack(fill=tk.BOTH)
        # 创建状态显示窗口
        self.Text_State = tk.Text(self.Frame_State, wrap='none', width=40)
        self.Text_State.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # 创建一个字符串用于输出名牌
        self.State_Output = "\t" + "人机地面站——By JuanRen." + "\n"
        self.Text_State.insert(tk.END, self.State_Output)
        # 创建滚动条
        self.Scrollbar_State = tk.Scrollbar(self.Frame_State, orient='vertical', command=self.Text_State.yview)
        self.Scrollbar_State.pack(side=tk.RIGHT, fill=tk.Y)
        self.Text_State.configure(yscrollcommand=self.Scrollbar_State.set)

        '''
        2. IP容器，包括label，按键以及输入框
        '''
        # 创建一个容器
        self.Frame_IP = tk.Frame(root, bd=4, relief="groove")
        self.Frame_IP.place(x=0, y=0)
        self.Label_IP = tk.Label(self.Frame_IP, text="IP设置栏", fg='black', font=(self.font_style, 10))
        self.Label_IP.grid(row=0, column=7)
        # ip地址设置
        self.label_IP1 = tk.Label(self.Frame_IP, text="IP1:", fg='black', font=(self.font_style, 10))
        self.label_IP2 = tk.Label(self.Frame_IP, text="IP2:", fg='black', font=(self.font_style, 10))
        self.label_IP3 = tk.Label(self.Frame_IP, text="IP3:", fg='black', font=(self.font_style, 10))
        self.label_IP4 = tk.Label(self.Frame_IP, text="IP4:", fg='black', font=(self.font_style, 10))
        self.label_IP5 = tk.Label(self.Frame_IP, text="IP5:", fg='black', font=(self.font_style, 10))
        self.label_IP6 = tk.Label(self.Frame_IP, text="IP6:", fg='black', font=(self.font_style, 10))
        self.label_IP7 = tk.Label(self.Frame_IP, text="IP7:", fg='black', font=(self.font_style, 10))
        self.label_IP8 = tk.Label(self.Frame_IP, text="IP8:", fg='black', font=(self.font_style, 10))
        self.label_IP9 = tk.Label(self.Frame_IP, text="IP9:", fg='black', font=(self.font_style, 10))
        self.label_IP10 = tk.Label(self.Frame_IP, text="IP10:", fg='black', font=(self.font_style, 10))
        self.label_IP1.grid(row=1)
        self.label_IP2.grid(row=1, column=3)
        self.label_IP3.grid(row=1, column=6)
        self.label_IP4.grid(row=1, column=9)
        self.label_IP5.grid(row=1, column=12)
        self.label_IP6.grid(row=2)
        self.label_IP7.grid(row=2, column=3)
        self.label_IP8.grid(row=2, column=6)
        self.label_IP9.grid(row=2, column=9)
        self.label_IP10.grid(row=2, column=12)

        # ip输入框设置
        self.Entry_IP1 = tk.Entry(self.Frame_IP, fg='black', font=(self.font_style, 10))
        self.Entry_IP2 = tk.Entry(self.Frame_IP, fg='black', font=(self.font_style, 10))
        self.Entry_IP3 = tk.Entry(self.Frame_IP, fg='black', font=(self.font_style, 10))
        self.Entry_IP4 = tk.Entry(self.Frame_IP, fg='black', font=(self.font_style, 10))
        self.Entry_IP5 = tk.Entry(self.Frame_IP, fg='black', font=(self.font_style, 10))
        self.Entry_IP6 = tk.Entry(self.Frame_IP, fg='black', font=(self.font_style, 10))
        self.Entry_IP7 = tk.Entry(self.Frame_IP, fg='black', font=(self.font_style, 10))
        self.Entry_IP8 = tk.Entry(self.Frame_IP, fg='black', font=(self.font_style, 10))
        self.Entry_IP9 = tk.Entry(self.Frame_IP, fg='black', font=(self.font_style, 10))
        self.Entry_IP10 = tk.Entry(self.Frame_IP, fg='black', font=(self.font_style, 10))
        # 设置默认输入
        # 红方: 161-165,有人机A3: 163
        # 蓝方: 177-181,有人机B3: 179
        self.IP_array = ['192.168.1.161', '192.168.1.162', '192.168.1.163', '192.168.1.164', '192.168.1.165',
                         '192.168.1.177', '192.168.1.178', '192.168.1.179', '192.168.1.180', '192.168.1.181']  # ip枚举
        self.Port_array = [8081, 8082, 8083, 8084, 8085, 8091, 8092, 8093, 8094, 8095]

        self.Entry_IP1.insert(0, self.IP_array[0])
        self.Entry_IP2.insert(0, self.IP_array[1])
        self.Entry_IP3.insert(0, self.IP_array[2])
        self.Entry_IP4.insert(0, self.IP_array[3])
        self.Entry_IP5.insert(0, self.IP_array[4])
        self.Entry_IP6.insert(0, self.IP_array[5])
        self.Entry_IP7.insert(0, self.IP_array[6])
        self.Entry_IP8.insert(0, self.IP_array[7])
        self.Entry_IP9.insert(0, self.IP_array[8])
        self.Entry_IP10.insert(0, self.IP_array[9])
        # 设置位置
        self.Entry_IP1.grid(row=1, column=1)
        self.Entry_IP2.grid(row=1, column=4)
        self.Entry_IP3.grid(row=1, column=7)
        self.Entry_IP4.grid(row=1, column=10)
        self.Entry_IP5.grid(row=1, column=13)
        self.Entry_IP6.grid(row=2, column=1)
        self.Entry_IP7.grid(row=2, column=4)
        self.Entry_IP8.grid(row=2, column=7)
        self.Entry_IP9.grid(row=2, column=10)
        self.Entry_IP10.grid(row=2, column=13)

        # 确认按键
        self.Button_IP1_Confirm = tk.Button(self.Frame_IP, text="确认", fg='black', font=(self.font_style, 10),
                                            command=self.Confirm_IP1)
        self.Button_IP2_Confirm = tk.Button(self.Frame_IP, text="确认", fg='black', font=(self.font_style, 10),
                                            command=self.Confirm_IP2)
        self.Button_IP3_Confirm = tk.Button(self.Frame_IP, text="确认", fg='black', font=(self.font_style, 10),
                                            command=self.Confirm_IP3)
        self.Button_IP4_Confirm = tk.Button(self.Frame_IP, text="确认", fg='black', font=(self.font_style, 10),
                                            command=self.Confirm_IP4)
        self.Button_IP5_Confirm = tk.Button(self.Frame_IP, text="确认", fg='black', font=(self.font_style, 10),
                                            command=self.Confirm_IP5)
        self.Button_IP6_Confirm = tk.Button(self.Frame_IP, text="确认", fg='black', font=(self.font_style, 10),
                                            command=self.Confirm_IP6)
        self.Button_IP7_Confirm = tk.Button(self.Frame_IP, text="确认", fg='black', font=(self.font_style, 10),
                                            command=self.Confirm_IP7)
        self.Button_IP8_Confirm = tk.Button(self.Frame_IP, text="确认", fg='black', font=(self.font_style, 10),
                                            command=self.Confirm_IP8)
        self.Button_IP9_Confirm = tk.Button(self.Frame_IP, text="确认", fg='black', font=(self.font_style, 10),
                                            command=self.Confirm_IP9)
        self.Button_IP10_Confirm = tk.Button(self.Frame_IP, text="确认", fg='black', font=(self.font_style, 10),
                                             command=self.Confirm_IP10)

        # 设置位置
        self.Button_IP1_Confirm.grid(row=1, column=2)
        self.Button_IP2_Confirm.grid(row=1, column=5)
        self.Button_IP3_Confirm.grid(row=1, column=8)
        self.Button_IP4_Confirm.grid(row=1, column=11)
        self.Button_IP5_Confirm.grid(row=1, column=14)
        self.Button_IP6_Confirm.grid(row=2, column=2)
        self.Button_IP7_Confirm.grid(row=2, column=5)
        self.Button_IP8_Confirm.grid(row=2, column=8)
        self.Button_IP9_Confirm.grid(row=2, column=11)
        self.Button_IP10_Confirm.grid(row=2, column=14)
        '''
        3.控制栏容器
        '''
        # 创建一个容器
        self.Frame_Show = tk.Frame(root, bd=4, relief="groove")
        self.Frame_Show.place(x=330, y=410)
        self.Label_Show0 = tk.Label(self.Frame_Show, text="实时显示栏", fg='black', font=(self.font_style, 10),bd=1,
                                    relief="groove")
        self.Label_Show0.grid(row=0, column=4)

        # 显示模块设置
        self.label_Show1 = tk.Label(self.Frame_Show, text="IP", fg='black', font=(self.font_style, 10), bd=1,
                                    relief="groove")
        self.label_Show2 = tk.Label(self.Frame_Show, text="Side", fg='black', font=(self.font_style, 10), bd=1,
                                    relief="groove")
        self.label_Show3 = tk.Label(self.Frame_Show, text="Sysid", fg='black', font=(self.font_style, 10), bd=1,
                                    relief="groove")
        self.label_Show4 = tk.Label(self.Frame_Show, text="飞行模式", fg='black', font=(self.font_style, 10), bd=1,
                                    relief="groove")
        self.label_Show5 = tk.Label(self.Frame_Show, text="任务模式", fg='black', font=(self.font_style, 10), bd=1,
                                    relief="groove")
        self.label_Show6 = tk.Label(self.Frame_Show, text="纬度", fg='black', font=(self.font_style, 10), bd=1,
                                    relief="groove")
        self.label_Show7 = tk.Label(self.Frame_Show, text="经度", fg='black', font=(self.font_style, 10), bd=1,
                                    relief="groove")
        self.label_Show8 = tk.Label(self.Frame_Show, text="高度", fg='black', font=(self.font_style, 10), bd=1,
                                    relief="groove")
        self.label_Show9 = tk.Label(self.Frame_Show, text="航向角", fg='black', font=(self.font_style, 10), bd=1,
                                    relief="groove")
        self.label_Show10 = tk.Label(self.Frame_Show, text="目标", fg='black', font=(self.font_style, 10), bd=1,
                                    relief="groove")
        self.label_Show1.grid(row=1)
        self.label_Show2.grid(row=1, column=1)
        self.label_Show3.grid(row=1, column=2)
        self.label_Show4.grid(row=1, column=3)
        self.label_Show5.grid(row=1, column=4)
        self.label_Show6.grid(row=1, column=5)
        self.label_Show7.grid(row=1, column=6)
        self.label_Show8.grid(row=1, column=7)
        self.label_Show9.grid(row=1, column=8)
        self.label_Show10.grid(row=1, column=9)



        # 输出模块(1号机)
        width_size = 10
        self.Text_show1_IP1 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show2_IP1 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show3_IP1 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show4_IP1 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show5_IP1 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show6_IP1 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show7_IP1 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show8_IP1 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show9_IP1 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show10_IP1 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)

        self.Text_show1_IP1.insert(tk.END, "   1")

        self.Text_show1_IP1.grid(row=2)
        self.Text_show2_IP1.grid(row=2, column=1)
        self.Text_show3_IP1.grid(row=2, column=2)
        self.Text_show4_IP1.grid(row=2, column=3)
        self.Text_show5_IP1.grid(row=2, column=4)
        self.Text_show6_IP1.grid(row=2, column=5)
        self.Text_show7_IP1.grid(row=2, column=6)
        self.Text_show8_IP1.grid(row=2, column=7)
        self.Text_show9_IP1.grid(row=2, column=8)
        self.Text_show10_IP1.grid(row=2, column=9)


        # 输出模块(2号机)
        self.Text_show1_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show2_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show3_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show4_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show5_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show6_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show7_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show8_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show9_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show10_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show11_IP2 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)

        self.Text_show1_IP2.insert(tk.END, "   2")

        self.Text_show1_IP2.grid(row=3)
        self.Text_show2_IP2.grid(row=3, column=1)
        self.Text_show3_IP2.grid(row=3, column=2)
        self.Text_show4_IP2.grid(row=3, column=3)
        self.Text_show5_IP2.grid(row=3, column=4)
        self.Text_show6_IP2.grid(row=3, column=5)
        self.Text_show7_IP2.grid(row=3, column=6)
        self.Text_show8_IP2.grid(row=3, column=7)
        self.Text_show9_IP2.grid(row=3, column=8)
        self.Text_show10_IP2.grid(row=3, column=9)


        # 输出模块(3号机)
        self.Text_show1_IP3 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show2_IP3 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show3_IP3 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show4_IP3 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show5_IP3 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show6_IP3 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show7_IP3 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show8_IP3 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show9_IP3 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show10_IP3 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)

        self.Text_show1_IP3.insert(tk.END, "   3")

        self.Text_show1_IP3.grid(row=4)
        self.Text_show2_IP3.grid(row=4, column=1)
        self.Text_show3_IP3.grid(row=4, column=2)
        self.Text_show4_IP3.grid(row=4, column=3)
        self.Text_show5_IP3.grid(row=4, column=4)
        self.Text_show6_IP3.grid(row=4, column=5)
        self.Text_show7_IP3.grid(row=4, column=6)
        self.Text_show8_IP3.grid(row=4, column=7)
        self.Text_show9_IP3.grid(row=4, column=8)
        self.Text_show10_IP3.grid(row=4, column=9)


        # 输出模块(4号机)
        self.Text_show1_IP4 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show2_IP4 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show3_IP4 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show4_IP4 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show5_IP4 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show6_IP4 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show7_IP4 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show8_IP4 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show9_IP4 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show10_IP4 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)

        self.Text_show1_IP4.insert(tk.END, "   4")

        self.Text_show1_IP4.grid(row=5)
        self.Text_show2_IP4.grid(row=5, column=1)
        self.Text_show3_IP4.grid(row=5, column=2)
        self.Text_show4_IP4.grid(row=5, column=3)
        self.Text_show5_IP4.grid(row=5, column=4)
        self.Text_show6_IP4.grid(row=5, column=5)
        self.Text_show7_IP4.grid(row=5, column=6)
        self.Text_show8_IP4.grid(row=5, column=7)
        self.Text_show9_IP4.grid(row=5, column=8)
        self.Text_show10_IP4.grid(row=5, column=9)


        # 输出模块(5号机)
        self.Text_show1_IP5 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show2_IP5 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show3_IP5 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show4_IP5 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show5_IP5 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show6_IP5 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show7_IP5 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show8_IP5 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show9_IP5 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show10_IP5 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)

        self.Text_show1_IP5.insert(tk.END, "   5")

        self.Text_show1_IP5.grid(row=6)
        self.Text_show2_IP5.grid(row=6, column=1)
        self.Text_show3_IP5.grid(row=6, column=2)
        self.Text_show4_IP5.grid(row=6, column=3)
        self.Text_show5_IP5.grid(row=6, column=4)
        self.Text_show6_IP5.grid(row=6, column=5)
        self.Text_show7_IP5.grid(row=6, column=6)
        self.Text_show8_IP5.grid(row=6, column=7)
        self.Text_show9_IP5.grid(row=6, column=8)
        self.Text_show10_IP5.grid(row=6, column=9)


        # 输出模块(6号机)
        self.Text_show1_IP6 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show2_IP6 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show3_IP6 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show4_IP6 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show5_IP6 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show6_IP6 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show7_IP6 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show8_IP6 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show9_IP6 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show10_IP6 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)

        self.Text_show1_IP6.insert(tk.END, "   6")

        self.Text_show1_IP6.grid(row=7)
        self.Text_show2_IP6.grid(row=7, column=1)
        self.Text_show3_IP6.grid(row=7, column=2)
        self.Text_show4_IP6.grid(row=7, column=3)
        self.Text_show5_IP6.grid(row=7, column=4)
        self.Text_show6_IP6.grid(row=7, column=5)
        self.Text_show7_IP6.grid(row=7, column=6)
        self.Text_show8_IP6.grid(row=7, column=7)
        self.Text_show9_IP6.grid(row=7, column=8)
        self.Text_show10_IP6.grid(row=7, column=9)


        # 输出模块(7号机)
        self.Text_show1_IP7 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show2_IP7 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show3_IP7 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show4_IP7 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show5_IP7 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show6_IP7 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show7_IP7 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show8_IP7 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show9_IP7 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show10_IP7 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)

        self.Text_show1_IP7.insert(tk.END, "   7")

        self.Text_show1_IP7.grid(row=8)
        self.Text_show2_IP7.grid(row=8, column=1)
        self.Text_show3_IP7.grid(row=8, column=2)
        self.Text_show4_IP7.grid(row=8, column=3)
        self.Text_show5_IP7.grid(row=8, column=4)
        self.Text_show6_IP7.grid(row=8, column=5)
        self.Text_show7_IP7.grid(row=8, column=6)
        self.Text_show8_IP7.grid(row=8, column=7)
        self.Text_show9_IP7.grid(row=8, column=8)
        self.Text_show10_IP7.grid(row=8, column=9)


        # 输出模块(8号机)
        self.Text_show1_IP8 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show2_IP8 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show3_IP8 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show4_IP8 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show5_IP8 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show6_IP8 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show7_IP8 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show8_IP8 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show9_IP8 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show10_IP8 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)

        self.Text_show1_IP8.insert(tk.END, "   8")

        self.Text_show1_IP8.grid(row=9)
        self.Text_show2_IP8.grid(row=9, column=1)
        self.Text_show3_IP8.grid(row=9, column=2)
        self.Text_show4_IP8.grid(row=9, column=3)
        self.Text_show5_IP8.grid(row=9, column=4)
        self.Text_show6_IP8.grid(row=9, column=5)
        self.Text_show7_IP8.grid(row=9, column=6)
        self.Text_show8_IP8.grid(row=9, column=7)
        self.Text_show9_IP8.grid(row=9, column=8)
        self.Text_show10_IP8.grid(row=9, column=9)


        # 输出模块(9号机)
        self.Text_show1_IP9 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show2_IP9 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show3_IP9 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show4_IP9 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show5_IP9 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show6_IP9 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show7_IP9 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show8_IP9 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show9_IP9 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show10_IP9 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)

        self.Text_show1_IP9.insert(tk.END, "   9")

        self.Text_show1_IP9.grid(row=10)
        self.Text_show2_IP9.grid(row=10, column=1)
        self.Text_show3_IP9.grid(row=10, column=2)
        self.Text_show4_IP9.grid(row=10, column=3)
        self.Text_show5_IP9.grid(row=10, column=4)
        self.Text_show6_IP9.grid(row=10, column=5)
        self.Text_show7_IP9.grid(row=10, column=6)
        self.Text_show8_IP9.grid(row=10, column=7)
        self.Text_show9_IP9.grid(row=10, column=8)
        self.Text_show10_IP9.grid(row=10, column=9)


        # 输出模块(10号机)
        self.Text_show1_IP10 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show2_IP10 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show3_IP10 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show4_IP10 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show5_IP10 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show6_IP10 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show7_IP10 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show8_IP10 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show9_IP10 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)
        self.Text_show10_IP10 = tk.Text(self.Frame_Show, wrap='none', width=width_size, height=1)

        self.Text_show1_IP10.insert(tk.END, "   10")

        self.Text_show1_IP10.grid(row=11)
        self.Text_show2_IP10.grid(row=11, column=1)
        self.Text_show3_IP10.grid(row=11, column=2)
        self.Text_show4_IP10.grid(row=11, column=3)
        self.Text_show5_IP10.grid(row=11, column=4)
        self.Text_show6_IP10.grid(row=11, column=5)
        self.Text_show7_IP10.grid(row=11, column=6)
        self.Text_show8_IP10.grid(row=11, column=7)
        self.Text_show9_IP10.grid(row=11, column=8)
        self.Text_show10_IP10.grid(row=11, column=9)

        '''
        整体控制容器
        '''
        # 创建一个容器
        self.Frame_Control = tk.Frame(root, bd=4, relief="groove")
        self.Frame_Control.place(x=0, y=410)
        self.Label_Control = tk.Label(self.Frame_Control, text="控制栏", fg='black', font=(self.font_style, 10))
        self.Label_Control.grid(row=0, column=2)
        # 创建全部监听/停止监听按键
        self.Button_Start_Stop = tk.Button(self.Frame_Control, text="全部开始", fg='black', font=(self.font_style, 10),
                                           command=self.Confirm_Start_Stop)
        self.Button_Start_Stop.grid(row=1,column=0)
        self.Button_Start_Flight = tk.Button(self.Frame_Control, text="全部起飞", fg='black', font=(self.font_style, 10),
                                           command=self.Confirm_Start_Flight)
        self.Button_Start_Flight.grid(row=1, column=1)

        self.Button_Start_Combat = tk.Button(self.Frame_Control, text="开始对抗", fg='black', font=(self.font_style, 10),
                                           command=self.Confirm_Start_Combat)
        self.Button_Start_Combat.grid(row=1, column=2)
        self.Button_Start_Land = tk.Button(self.Frame_Control, text="开始降落", fg='black', font=(self.font_style, 10),
                                           command=self.Confirm_Start_Land)
        self.Button_Start_Land.grid(row=1, column=3)

        self.Button_Clear_Vision = tk.Button(self.Frame_Control, text="清空视觉", fg='black', font=(self.font_style, 10),
                                           command=self.Confirm_Clear_Vision)
        self.Button_Clear_Vision.grid(row=1, column=4)
        self.Button_Clear_State = tk.Button(self.Frame_Control, text="清空状态", fg='black', font=(self.font_style, 10),
                                           command=self.Confirm_Clear_State)
        self.Button_Clear_State.grid(row=2, column=0)


        '''
        有人机视觉识别容器
        '''
        #红方
        # 创建一个容器
        self.Frame_Detect_Red = tk.Frame(root,bd = 4, relief="groove")
        self.Frame_Detect_Red.place(x=1090, y=0)
        # 创建一个说明
        self.Label_Detect_Red = tk.Label(self.Frame_Detect_Red, text="红方视觉检测结果", fg='black', font=(self.font_style, 10))
        self.Label_Detect_Red.pack(fill=tk.BOTH)
        # 创建状态显示窗口
        self.Text_Detect_Red = tk.Text(self.Frame_Detect_Red, wrap='none', width=40,height=22)
        self.Text_Detect_Red.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # 创建一个字符串用于输出名牌
        self.Red_Detect_Output = "\t\t" + "红方检测结果" + "\n"
        self.Text_Detect_Red.insert(tk.END, self.Red_Detect_Output)
        # 创建滚动条
        self.Scrollbar_Red_Detect = tk.Scrollbar(self.Frame_Detect_Red, orient='vertical', command=self.Text_Detect_Red.yview)
        self.Scrollbar_Red_Detect.pack(side=tk.RIGHT, fill=tk.Y)
        self.Text_Detect_Red.configure(yscrollcommand=self.Scrollbar_Red_Detect.set)

        #蓝方
        self.Frame_Detect_Blue= tk.Frame(root,bd = 4, relief="groove")
        self.Frame_Detect_Blue.place(x=1090, y=310)
        # 创建一个说明
        self.Label_Detect_Blue = tk.Label(self.Frame_Detect_Blue, text="蓝方视觉检测结果", fg='black', font=(self.font_style, 10))
        self.Label_Detect_Blue.pack(fill=tk.BOTH)
        # 创建状态显示窗口
        self.Text_Detect_Blue = tk.Text(self.Frame_Detect_Blue, wrap='none', width=40,height=22)
        self.Text_Detect_Blue.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # 创建一个字符串用于输出名牌
        self.Blue_Detect_Output = "\t\t" + "蓝方检测结果" + "\n"
        self.Text_Detect_Blue.insert(tk.END, self.Blue_Detect_Output)
        # 创建滚动条
        self.Scrollbar_Blue_Detect = tk.Scrollbar(self.Frame_Detect_Blue, orient='vertical', command=self.Text_Detect_Blue.yview)
        self.Scrollbar_Blue_Detect.pack(side=tk.RIGHT, fill=tk.Y)
        self.Text_Detect_Blue.configure(yscrollcommand=self.Scrollbar_Blue_Detect.set)

        '''
        卫星地图容器
        '''
        # 创建一个容器
        self.Frame_Map = tk.Frame(root, bd=4, relief="groove")
        self.Frame_Map.place(x=310, y=70)
        # self.Label_Map = tk.Label(self.Frame_Map, text="卫星地图", fg='black', font=(self.font_style, 10))
        # self.Label_Map.grid(row=0,column=1)

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 创建卫星地图
        self.Map_fig = plt.figure(figsize=(7.7, 3.3))
        self.ax = self.Map_fig.add_subplot(projection=ccrs.PlateCarree())
        plt.tight_layout(pad=1.0, h_pad=None, w_pad=None, rect=None)
        # 河北超图区域
        self.ax.set_extent([115.908, 115.922, 39.367, 39.372], crs=ccrs.PlateCarree())
        request = TDT_img()
        self.ax.add_image(request, 16)

        # 在Tkinter中嵌入图形
        self.canvas = FigureCanvasTkAgg(self.Map_fig, master=self.Frame_Map)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.Frame_Map.grid_rowconfigure(0, weight=1)
        self.Frame_Map.grid_columnconfigure(0, weight=1)
        # self.gl = self.ax.gridlines(draw_labels=True, linewidth=1, color='k', alpha=0.5, linestyle='--')
        # self.gl.xlabels_top = self.gl.ylabels_right = False
        # self.gl.xformatter = LONGITUDE_FORMATTER
        # self.gl.yformatter = LATITUDE_FORMATTER

        # 绑定关闭事件，在关闭 Tkinter 窗口时关闭 Matplotlib 图形
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        '''
        更新数据的定期调用
        '''
        self.pkl_files = [
            "UAV1_STATE.pkl",
            "UAV2_STATE.pkl",
            "UAV3_STATE.pkl",
            "UAV4_STATE.pkl",
            "UAV5_STATE.pkl",
            "UAV6_STATE.pkl",
            "UAV7_STATE.pkl",
            "UAV8_STATE.pkl",
            "UAV9_STATE.pkl",
            "UAV10_STATE.pkl"
        ]
        self.count = 10

        '''
        创建线程套接字数组
        '''
        self.threads_arr=[None]*self.count


        '''
        实例化数据
        '''
        self.data_read_and_judge = data_class(self.pkl_files, self.count)

        # 启动定期更新
        self.schedule_update()

    '''按键绑定事件，对连接上的目标发送对抗命令'''
    def Confirm_Start_Flight(self):
        if self.Button_Start_Flight['text']=="全部起飞":
            count_for_all_send = 0
            for i in range(1,self.count+1):
                if self.threads_arr[i-1] and not self.threads_arr[i-1].start_command_flag:   #若对应ip套接字非空且发送标志位为false
                    command={'id':88,
                             'command':1}
                    self.threads_arr[i-1].start_command_flight(command)  #开始发送指令
                    self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"向{i}号无人机发送起飞指令!\n")
                    self.Text_State.see(tk.END)
                    count_for_all_send += 1
                elif not self.threads_arr[i-1]:
                    self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"{i}号无人机未连接，无法发送!\n")
                    self.Text_State.see(tk.END)
                else:
                    self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"{i}号无人机已发送过消息!\n")
                    self.Text_State.see(tk.END)

            if count_for_all_send >= 10:
                self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"所有无人机均正常发送命令\n")
                self.Text_State.see(tk.END)

    '''按键绑定事件，对连接上的目标发送对抗命令'''
    def Confirm_Start_Combat(self):
        if self.Button_Start_Combat['text']=="开始对抗":
            count_for_all_send = 0
            for i in range(1,self.count+1):
                if self.threads_arr[i-1] and not self.threads_arr[i-1].command_flag:   #若对应ip套接字非空且发送标志位为false
                    command={'id':88,
                             'command':2}
                    self.threads_arr[i-1].start_command(command)  #开始发送指令
                    self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"向{i}号无人机发送对抗指令!\n")
                    self.Text_State.see(tk.END)
                    count_for_all_send += 1
                elif not self.threads_arr[i-1]:
                    self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"{i}号无人机未连接，无法发送!\n")
                    self.Text_State.see(tk.END)
                else:
                    self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"{i}号无人机已发送过消息!\n")
                    self.Text_State.see(tk.END)

            if count_for_all_send >= 10:
                self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"所有无人机均正常发送命令\n")
                self.Text_State.see(tk.END)

    '''按键绑定事件，对连接上的目标发送对抗命令'''
    def Confirm_Start_Land(self):
        if self.Button_Start_Land['text']=="开始降落":
            count_for_all_send = 0
            for i in range(1,self.count+1):
                if self.threads_arr[i-1] and not self.threads_arr[i-1].stop_command_flag:   #若对应ip套接字非空且发送标志位为false
                    command={'id':88,
                             'command':3}
                    self.threads_arr[i-1].start_command_stop(command)  #开始发送指令
                    self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"向{i}号无人机发送降落指令!\n")
                    self.Text_State.see(tk.END)
                    count_for_all_send += 1
                elif not self.threads_arr[i-1]:
                    self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"{i}号无人机未连接，无法发送!\n")
                    self.Text_State.see(tk.END)
                else:
                    self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"{i}号无人机已发送过消息!\n")
                    self.Text_State.see(tk.END)

            if count_for_all_send >= 10:
                self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"所有无人机均正常发送命令\n")
                self.Text_State.see(tk.END)

    '''清除视觉检测结果栏'''
    def Confirm_Clear_Vision(self):
        getattr(self, f'Text_Detect_Red').delete("1.0", tk.END)
        getattr(self, f'Text_Detect_Blue').delete("1.0", tk.END)

        self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"已清除双方视觉检测结果！\n")
        self.Text_State.see(tk.END)

    '''清除状态显示栏'''
    def Confirm_Clear_State(self):
        getattr(self, f'Text_State').delete("1.0", tk.END)
        self.State_Output = "\t" + "人机地面站——By JuanRen." + "\n"
        self.Text_State.insert(tk.END, self.State_Output)
        self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"已清除状态显示栏！\n")
        self.Text_State.see(tk.END)




    '''
    时间戳获取函数
    '''
    def Gain_Time_Stamp(self):
        timestamp = time.localtime(time.time())
        if timestamp.tm_hour < 10:
            time_hour = "0" + timestamp.tm_hour.__str__()
        else:
            time_hour = timestamp.tm_hour.__str__()
        if timestamp.tm_min < 10:
            time_min = "0" + timestamp.tm_min.__str__()
        else:
            time_min = timestamp.tm_min.__str__()
        if timestamp.tm_sec < 10:
            time_sec = "0" + timestamp.tm_sec.__str__()
        else:
            time_sec = timestamp.tm_sec.__str__()
        time_stamp_str = time_hour + ":" + time_min + ":" + time_sec + ":"
        return time_stamp_str

    '''
    事件触发相关函数IP1-IP10
    事件:获取框内IP地址，并创建连接，如果连接成功，在下方状态栏中说明
    如果连接成功，锁定对应IP栏目
    '''
    def Confirm_IP(self, ip_number):
        # 根据 IP 号选择相应的控件和线程
        entry = getattr(self, f'Entry_IP{ip_number}')
        button = getattr(self, f'Button_IP{ip_number}_Confirm')
        thread_attr = f'IP_Thread{ip_number}'
        '''
         显示数据更新
         '''
        if button['text'] == '确认':
            self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"尝试进行IP{ip_number}连接。。。。。" + "\n")
            self.Text_State.see(tk.END)

            # 新建一个IP线程
            thread = MyThread(f"UAV{ip_number}_STATE.pkl", self.IP_array[ip_number - 1], self.Port_array[ip_number - 1],
                              name=f'IPThread{ip_number}')
            setattr(self, thread_attr, thread)

            # 尝试启动线程
            thread.start()
            time.sleep(0.1)

            if thread.connect_flag:  # IP连接成功
                self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"IP{ip_number}连接成功!" + "\n")
                self.Text_State.see(tk.END)
                entry['state'] = 'readonly'  # 该状态栏位只读
                button['text'] = '修改'  # button为修改
                # 记录线程地址
                self.threads_arr[ip_number - 1] = thread

            else:  # IP连接失败
                self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"IP{ip_number}连接失败!" + "\n")
                self.Text_State.see(tk.END)
                entry['state'] = 'normal'  # 该状态栏位可修改
                button['text'] = '确认'  # button为确认
                #关闭线程
                thread = getattr(self, thread_attr)
                thread.close()
                #将对应线程地址清除
                self.threads_arr[ip_number - 1] = None
        else:
            self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"IP{ip_number}线程关闭!" + "\n")
            self.Text_State.see(tk.END)

            # 关闭线程
            thread = getattr(self, thread_attr)
            thread.close()
            entry['state'] = 'normal'  # 该状态栏位可修改
            button['text'] = '确认'  # button为确认
            # 将对应线程地址清除
            self.threads_arr[ip_number - 1] = None

    def Confirm_IP1(self):
        self.Confirm_IP(1)

    def Confirm_IP2(self):
        self.Confirm_IP(2)

    def Confirm_IP3(self):
        self.Confirm_IP(3)

    def Confirm_IP4(self):
        self.Confirm_IP(4)

    def Confirm_IP5(self):
        self.Confirm_IP(5)

    def Confirm_IP6(self):
        self.Confirm_IP(6)

    def Confirm_IP7(self):
        self.Confirm_IP(7)

    def Confirm_IP8(self):
        self.Confirm_IP(8)

    def Confirm_IP9(self):
        self.Confirm_IP(9)

    def Confirm_IP10(self):
        self.Confirm_IP(10)

    '''
    事件触发相关函数，全部启停，对应Button_Start_Stop
    直接调用所有confirm_IP事件函数
    '''
    def Confirm_Start_Stop(self):
        if self.Button_Start_Stop['text'] == "全部开始":
            # 调用所有的事件
            for i in range(1, 11):
                getattr(self, f'Confirm_IP{i}')()

            self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + "全部线程启动!" + "\n")
            self.Text_State.see(tk.END)
            self.Button_Start_Stop['text'] = "全部停止"
            time.sleep(1)
        else:
            for i in range(1, 11):
                getattr(self, f'IP_Thread{i}').close()
            # 所有的状态栏和button置位
            self.Entry_IP1['state'] = 'normal'  # 该状态栏位可修改
            self.Button_IP1_Confirm['text'] = '确认'  # button为修改
            self.Entry_IP2['state'] = 'normal'  # 该状态栏位可修改
            self.Button_IP2_Confirm['text'] = '确认'  # button为修改
            self.Entry_IP3['state'] = 'normal'  # 该状态栏位可修改
            self.Button_IP3_Confirm['text'] = '确认'  # button为修改
            self.Entry_IP4['state'] = 'normal'  # 该状态栏位可修改
            self.Button_IP4_Confirm['text'] = '确认'  # button为修改
            self.Entry_IP5['state'] = 'normal'  # 该状态栏位可修改
            self.Button_IP5_Confirm['text'] = '确认'  # button为修改
            self.Entry_IP6['state'] = 'normal'  # 该状态栏位可修改
            self.Button_IP6_Confirm['text'] = '确认'  # button为修改
            self.Entry_IP7['state'] = 'normal'  # 该状态栏位可修改
            self.Button_IP7_Confirm['text'] = '确认'  # button为修改
            self.Entry_IP8['state'] = 'normal'  # 该状态栏位可修改
            self.Button_IP8_Confirm['text'] = '确认'  # button为修改
            self.Entry_IP9['state'] = 'normal'  # 该状态栏位可修改
            self.Button_IP9_Confirm['text'] = '确认'  # button为修改
            self.Entry_IP10['state'] = 'normal'  # 该状态栏位可修改
            self.Button_IP10_Confirm['text'] = '确认'  # button为修改

            self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + "全部线程关闭!" + "\n")
            self.Text_State.see(tk.END)
            self.Button_Start_Stop['text'] = "全部开始"
            time.sleep(1)

    def run(self):
        self.root.mainloop()

    '''
    关闭界面时，销毁卫星地图
    '''
    def on_closing(self):
        # 销毁 Tkinter 窗口
        self.root.destroy()
        plt.close(self.Map_fig)  # 关闭 Matplotlib 图形（如果需要）

    #定期更新
    def schedule_update(self):
        """定期更新无人机状态显示"""
        if all(os.path.exists(file) for file in self.pkl_files):
            self.update_text_boxes(self.pkl_files)
        else:
            self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + "某些UAV状态文件不存在，无法更新显示。\n")
            self.Text_State.see(tk.END)

        # 每隔1000毫秒（1秒）调用一次 schedule_update 方法
        self.root.after(1000, self.schedule_update)

    # 更新GUI中所有无人机的数据
    def update_text_boxes(self, pkl_files):

        self.data_for_submit, self.data_for_send = self.data_read_and_judge.read_data()

        # 向所有有地址的无人机发送数据
        #判断线程套接字是否为空，不是空，就进行数据更新

        for i in range(1,self.count+1):
            count_for_all_send=0
            if self.threads_arr[i-1]:
                self.threads_arr[i-1].update_data(self.data_for_send)
                count_for_all_send+=1
                self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"向{i}号无人机发状态信息!\n")
                self.Text_State.see(tk.END)
            else:
                #self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"{i}号无人机未连接!\n")
                self.Text_State.see(tk.END)
            if count_for_all_send >= 10:
                self.Text_State.insert(tk.END, self.Gain_Time_Stamp() + f"所有无人机均发送状态信息\n")
                self.Text_State.see(tk.END)



        for i in range(1,self.count+1):
            getattr(self, f'Text_show2_IP{i}').delete("1.0", tk.END)
            getattr(self, f'Text_show2_IP{i}').insert(tk.END, f"{self.data_for_submit[i-1]['side']}\n")

            getattr(self, f'Text_show3_IP{i}').delete("1.0", tk.END)
            getattr(self, f'Text_show3_IP{i}').insert(tk.END, f"{self.data_for_submit[i-1]['sysid']}\n")

            getattr(self, f'Text_show4_IP{i}').delete("1.0", tk.END)
            getattr(self, f'Text_show4_IP{i}').insert(tk.END, f"{self.data_for_submit[i-1]['flight_mode']}\n")

            getattr(self, f'Text_show5_IP{i}').delete("1.0", tk.END)
            getattr(self, f'Text_show5_IP{i}').insert(tk.END, f"{self.data_for_submit[i-1]['task_state']}\n")

            getattr(self, f'Text_show6_IP{i}').delete("1.0", tk.END)
            getattr(self, f'Text_show6_IP{i}').insert(tk.END, f"{self.data_for_submit[i-1]['lat']}\n")  # 纬度

            getattr(self, f'Text_show7_IP{i}').delete("1.0", tk.END)
            getattr(self, f'Text_show7_IP{i}').insert(tk.END, f"{self.data_for_submit[i-1]['lon']}\n")  # 经度

            getattr(self, f'Text_show8_IP{i}').delete("1.0", tk.END)
            getattr(self, f'Text_show8_IP{i}').insert(tk.END, f"{self.data_for_submit[i-1]['alt']}\n")  # 经度

            getattr(self, f'Text_show9_IP{i}').delete("1.0", tk.END)
            getattr(self, f'Text_show9_IP{i}').insert(tk.END, f"{self.data_for_submit[i-1]['hdg']}\n")

            getattr(self, f'Text_show10_IP{i}').delete("1.0", tk.END)
            getattr(self, f'Text_show10_IP{i}').insert(tk.END, f"{self.data_for_submit[i-1]['tar']}\n")


            if self.data_for_submit[i-1]['sysid'] == 'A3':
                Red_neighbor_show = f"{self.Gain_Time_Stamp()}\n"
                if not self.data_for_submit[i-1]['neighbor']: #如果数据为空
                    temp = f"敌方:x1:0,y1:0,x2:0,y2:0, \n"+\
                           f"友方:x1:0,y1:0,x2:0,y2:0 \n"
                    Red_neighbor_show+=temp
                    self.Text_Detect_Red.insert(tk.END, Red_neighbor_show)
                    self.Text_Detect_Red.see(tk.END)
                else:
                    for j in range(1,len(self.data_for_submit[i-1]['neighbor'])+1):
                        if self.data_for_submit[i-1]['neighbor'][j-1]=='Hostile':
                            temp=f"敌方:x1:{self.data_for_submit[i-1]['x1'][j-1]},y1:{self.data_for_submit[i-1]['y1'][j-1]},"\
                                    +f"x2:{self.data_for_submit[i-1]['x2'][j-1]},y2:{self.data_for_submit[i-1]['y2'][j-1]}, \n"
                            Red_neighbor_show+=temp
                        elif self.data_for_submit[i-1]['neighbor'][j-1]=='Friend':
                            temp=f"友方:x1:{self.data_for_submit[i-1]['x1'][j-1]},y1:{self.data_for_submit[i-1]['x2'][j-1]},"\
                                    +f"x2:{self.data_for_submit[i-1]['x1'][j-1]},y2:{self.data_for_submit[i-1]['y2'][j-1]}, \n"
                            Red_neighbor_show+=temp
                    self.Text_Detect_Red.insert(tk.END, Red_neighbor_show)
                    self.Text_Detect_Red.see(tk.END)
            elif self.data_for_submit[i-1]['sysid'] == 'B3':
                Blue_neighbor_show = f"{self.Gain_Time_Stamp()} \n"
                if not self.data_for_submit[i-1]['neighbor']: #如果数据为空
                    temp = f"敌方:x1:0,y1:0,x2:0,y2:0, \n"+\
                           f"友方:x1:0,y1:0,x2:0,y2:0 \n"
                    Blue_neighbor_show+=temp
                    self.Text_Detect_Blue.insert(tk.END, Blue_neighbor_show)
                    self.Text_Detect_Blue.see(tk.END)
                else:
                    for j in range(1, len(self.data_for_submit[i - 1]['neighbor']) + 1):
                        if self.data_for_submit[i-1]['neighbor'][j-1]=='Hostile':
                            temp=f"敌方:x1:{self.data_for_submit[i-1]['x1'][j-1]},y1:{self.data_for_submit[i-1]['y1'][j-1]},"\
                                    +f"x2:{self.data_for_submit[i-1]['x2'][j-1]},y2:{self.data_for_submit[i-1]['y2'][j-1]} \n"
                            Blue_neighbor_show+=temp
                        elif self.data_for_submit[i-1]['neighbor'][j-1]=='Friend':
                            temp=f"友方:x1:{self.data_for_submit[i-1]['x1'][j-1]},y1:{self.data_for_submit[i-1]['x2'][j-1]},"\
                                    +f"x2:{self.data_for_submit[i-1]['x1'][j-1]},y2:{self.data_for_submit[i-1]['y2'][j-1]} \n"
                            Blue_neighbor_show+=temp
                    self.Text_Detect_Blue.insert(tk.END, Blue_neighbor_show)
                    self.Text_Detect_Blue.see(tk.END)


