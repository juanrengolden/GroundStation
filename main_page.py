import tkinter as tk
import subprocess
import threading
import socket
import time
import pickle
from main_class import main_Class

import os

'''
全局变量区
'''
'''
def run_script(script_name):
    """运行指定的Python脚本"""
    subprocess.run(["python", script_name])
'''

if __name__ == "__main__":
    root = tk.Tk()
    GCS = main_Class(root)  # 实例化地面站


    #  创建线程thread_1 测试是否可以接受数据
    #  Todo 后续采用真实数据
    #thread1 = threading.Thread(target=run_script, args=("server_socket.py",))
    # 启动线程
    #thread1.start()

    GCS.run()  # 运行地面站
