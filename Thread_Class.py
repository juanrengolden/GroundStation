import tkinter as tk
import subprocess
import threading
import socket
import time
import pickle


# 多线程类，用于改写相关参数
class MyThread(threading.Thread):
    def __init__(self, filename, host, port, name=None):
        threading.Thread.__init__(self, name=name)
        self.server_socket = None
        self.thread_flag = True  # 判断是否停止线程
        self.connect_flag = False  # 判断IP是否连接上
        self.number = 1
        self.filename = filename  # 数据保存的文件名
        self.host = host  # ip地址
        self.port = port  # 端口
        self.refused_count = 0  # 断连计数

        # 数据接收
        self.command_start_count = 0 #起飞计数
        self.command_count = 0 #发送计数
        self.command_stop_count = 0 #降落计数

        self.start_command_flag=False #起飞命令标志位
        self.command_start=[] #起飞命令接收

        self.command_flag = False  # 空战命令标志位
        self.command = []   #命令接收

        self.stop_command_flag=False#降落命令标志位
        self.command_stop=[] #降落命令接收

        self.data_received = [] # 状态量接收

    #保存数据
    def save_data_to_file(self, data):
        """将数据保存到文件中"""
        try:
            with open(self.filename, 'wb') as file:
                pickle.dump(data, file)
            print(f"数据已保存到文件：{self.filename}")
        except Exception as e:
            print(f"保存数据时发生错误：{e}")

    def close(self):
        """关闭线程"""
        self.thread_flag = False  # 关闭线程

    def update_data(self,data):
        """更新数据内容"""
        self.data_received = data

    #开始起飞
    def start_command_flight(self,command):
        # 开始发送起飞命令
        self.start_command_flag = True
        self.command_start =command
    #开始对抗
    def start_command(self,command):
        #开始发送
        self.command_flag = True
        self.command = command    #记录当前指令
    #开始降落
    def start_command_stop(self,command):
        # 开始发送降落命令
        self.stop_command_flag = True
        self.command_stop = command


    #当地面站是服务端时的收发方法，已经弃用。如果要使用，将函数名改为run
    def run_server(self):
        """运行线程: 开启TCP监听，处理数据后在对应的框内显示"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")
        try:
            while self.thread_flag:
                self.connect_flag = True  # 判断IP是否连接上
                try:
                    client_socket, addr = self.server_socket.accept()
                    print(f"Connection from {addr}")
                    threading.Thread(target=self.handle_client, args=(client_socket,)).start()
                except socket.error as e:
                    print(f"Socket error: {e}")
                # print(threading.current_thread().name + ' test ', self.number)
                # self.number += 1
                time.sleep(2)
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.server_socket.close()
            print("Server shutdown complete.")


    def handle_client(self, client_socket):
        """处理客户端的数据接收和处理"""
        try:
            while True:
                data = client_socket.recv(1024)  # 接收数据
                if not data:
                    break  # 没有数据表示客户端已经断开连接
                try:
                    received_dict = pickle.loads(data)
                    # 保存接收到的数据
                    self.save_data_to_file(received_dict)
                    print(f"Received dictionary: {received_dict}")

                except Exception as e:
                    print(f"Error deserializing data: {e}")
        finally:
            client_socket.close()


    def connect_to_server(self):
        """ 尝试连接到服务器，如果连接失败则等待再次尝试 """
        while self.thread_flag:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((self.host, self.port))
                print(f"Client tries to connect to {self.host}:{self.port}")

                # 连接成功后，标志位置位
                self.connect_flag = True
                print(f"成功连接到服务器 {self.host}:{self.port}")
                while self.thread_flag:

                    #发送起飞指令
                    if self.start_command_flag:
                        if self.command_start_count<5:
                            command_byte = pickle.dumps(self.command_start, protocol=2)
                            print(f"{self.Gain_Time_Stamp()}开始向服务端{self.host}:{self.port}发送起飞指令:{self.command_start}, 次数:{self.command_start_count+1}")
                            sock.send(command_byte)

                            self.command_start_count += 1
                            time.sleep(0.5)
                        else:
                            self.start_command_flag = False
                            self.command_start_count =0
                            print(f"{self.Gain_Time_Stamp()}已向服务端{self.host}:{self.port}发送完成起飞指令")

                    # 发送对抗指令
                    if self.command_flag:
                        if self.command_count<5:
                            command_byte = pickle.dumps(self.command, protocol=2)
                            print(f"{self.Gain_Time_Stamp()}开始向服务端{self.host}:{self.port}发送空战指令:{self.command}, 次数:{self.command_count+1}")
                            sock.send(command_byte)

                            self.command_count += 1
                            time.sleep(0.5)
                        else:
                            self.command_flag = False
                            self.command_count =0
                            print(f"{self.Gain_Time_Stamp()}已向服务端{self.host}:{self.port}发送完成空战指令")

                    # 发送降落指令
                    if self.stop_command_flag:
                        if self.command_stop_count<5:
                            command_byte = pickle.dumps(self.command_stop, protocol=2)
                            print(f"{self.Gain_Time_Stamp()}开始向服务端{self.host}:{self.port}发送降落指令:{self.command_stop}, 次数:{self.command_stop_count+1}")
                            sock.send(command_byte)

                            self.command_stop_count += 1
                            time.sleep(0.5)
                        else:
                            self.stop_command_flag = False
                            self.command_stop_count =0
                            print(f"{self.Gain_Time_Stamp()}已向服务端{self.host}:{self.port}发送完成降落指令")

                    #发送状态量
                    if self.data_received:
                        state_byte = pickle.dumps(self.data_received,protocol=2)
                        print(f"向服务端{self.host}:{self.port}发送状态")
                        sock.send(state_byte)
                        time.sleep(1)

                    #接收数据
                    data = sock.recv(4096)
                    if not data:
                        print("服务端数据为空, 销毁套接字并重连")
                        break

                    # 打印连接到的消息
                    #print(data)
                    #print(len(data))
                    received_dict = pickle.loads(data)
                    #print("Received dictionary:", received_dict)
                    self.save_data_to_file(received_dict)
                    print(f"{self.Gain_Time_Stamp()} Received dictionary: {received_dict}")

            except (EOFError, pickle.UnpicklingError) as e:
                self.connect_flag = False
                print("Failed to decode data:", e)
            except ConnectionRefusedError:
                self.connect_flag = False
                print(f"与服务端的连接被拒绝 {self.host}:{self.port} .")
                self.refused_count+=1
                # 五次被拒绝后，结束该线程
                if self.refused_count>=5:
                    self.thread_flag = False
            finally:
                #关闭socket连接
                sock.close()
                #print(f"与服务端 {self.host}:{self.port} 的连接关闭")


    def run(self):
        print(f"Client starts to connect to {self.host}:{self.port}")
        try:
            # 启动连接线程
            connection_thread = threading.Thread(target=self.connect_to_server)
            connection_thread.start()
        except Exception as e:
            print(f"Socket error: {e}")



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












