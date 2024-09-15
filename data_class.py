import numpy as np
import os
import pickle
import copy

## 用于数据的记录和处理
## 具体方法是，从文本中加载数据，并进行处理
class data_class:
    def __init__(self,pkl_files,count):
        self.pkl_files= pkl_files
        self.count = count

        self.flight_style = 2   #飞行模式: 1为固定翼 2为旋翼 3垂起固定翼
        """
            detection=[
        {
            'x1': 100,    # 检测框左上角的X坐标
            'y1': 150,    # 检测框左上角的Y坐标
            'x2': 200,    # 检测框右下角的X坐标
            'y2': 250,    # 检测框右下角的Y坐标
            'cls': "Hostlie",  # 检测到的对象类别"Hostile","Friend"
            'track_id': 2
        },
    ]
        state = {'side': 1,         # 1是红方，2是蓝方           
                 'sysid': 1,        # 飞行器id: 红方:161-165, 蓝方177-181
                 'flight_mode': 'STABILIZE',  # 采用飞行模式判断
                 'task_state': 1,   # 任务模式判断
                 'lat': 1,          # 纬度
                 'lon': 0,          # 经度
                 'alt': 0,          # 高度
                 'hdg': 0,          # 航向角
                 'tar': 1.0,
                 'Detections':detection #视觉检测结果
                 }        # 目标(目标对应id)
        
        """


        # 字典数组，用于存储所有读取到的数据
        self.state_record = []
        #字典数组，可能还需要存储上一周期的数据

    # 数据读取
    def read_data(self):
        # 数据获取
        data_dict=[]
        data_dict_for_send = []
        for i in range(1,self.count+1):
            with open(self.pkl_files[i - 1], 'rb') as file:
                data = pickle.load(file)

            data_for_send = data.copy()
            del data_for_send['Detections']
            data_dict_for_send.append(data_for_send)

            # 用于承接处理后的数据
            data_judged = {
                'side': "",
                'sysid':"",
                'flgiht_mode':"",
                'task_state':"",
                'lat':0,
                'lon':0,
                'hdg':0,
                'tar':"",
                'x1':[],
                'y1':[],
                'x2':[],
                'y2':[],
                'neighbor':[],
            }


            # 读取数据并处理
            data_judged["side"] = self.side_judge(data['side'])
            data_judged["sysid"] = self.sysid_judge(data['sysid'])
            data_judged["flight_mode"] = (data['flight_mode'])
            data_judged["task_state"] = self.task_mode_judge(data['task_state'])
            data_judged["lat"] = data['lat']
            data_judged["lon"] = data['lon']
            data_judged["alt"] = data['alt']
            data_judged["hdg"] = data['hdg']
            data_judged["tar"] = self.sysid_judge(data['tar'])

            # 视觉相关数据
            if not data['Detections']: #如果Detections为空
                data_judged['x1'] = []
                data_judged['y1'] = []
                data_judged['x2'] = []
                data_judged['y2'] = []
                data_judged['neighbor'] = []
            elif isinstance(data['Detections'], dict):  #Detections有一组数据，此时为一个字典
                data_judged['x1'].append(data['Detections']['x1'])
                data_judged['x1'].append(data['Detections']['y1'])
                data_judged['x1'].append(data['Detections']['x2'])
                data_judged['x1'].append(data['Detections']['y2'])
                data_judged['neighbor'].append(data['Detections']['cls'])
            else:   #Detections有两个以上数据
                #记录字典内得到的数据
                for Detection in data['Detections']:
                    # print(Detection)
                    data_judged['x1'].append(Detection['x1'])
                    data_judged['y1'].append(Detection['y1'])
                    data_judged['x2'].append(Detection['x2'])
                    data_judged['y2'].append(Detection['y2'])
                    data_judged['neighbor'].append(Detection['cls'])

            #生成一个新的字典
            data_dict.append(data_judged)
        return data_dict, data_dict_for_send

    # 获取飞行模式
    def flight_mode_judge(self, mode):
        mode_dict={}
        if self.flight_style == 1:  #固定翼
            mode_dict = {
                0: lambda :"MANUAL",
                1: lambda:"CIRCLE",
                2: lambda:"STABILIZE",
                3: lambda:"TRAINING",
                4: lambda:"ACRO",
                5: lambda:"FBWA",
                6: lambda:"FBWB",
                7: lambda: "CRUISE",
                8: lambda: "AUTOTUNE",
                9: lambda: "UNKOWN",
                10: lambda: "AUTO",
                11: lambda: "RTL",
                12: lambda: "LOITER",
                13: lambda: "TAKEOFF",
                14: lambda: "AVIOD_ADSB",
                15: lambda: "GUIDED",
                16: lambda: "INITIALISING",
            }
        elif self.flight_style == 2:     #旋翼
            mode_dict = {
                0: lambda: "STABILIZE",
                1: lambda: "ACRO",
                2: lambda: "ALTHOLD",
                3: lambda: "AUTO",
                4: lambda: "GUIDED",
                5: lambda: "LOITER",
                6: lambda: "RTL",
                7: lambda: "CIRCLE",
                8: lambda: "UNKOWN",
                9: lambda: "LAND",
                17: lambda: "BRAKE"
            }
        else:                       #垂起
            mode_dict = {
                0: lambda:"MANUAL",
                1: lambda:"CIRCLE",
                2: lambda:"STABILIZE",
                3: lambda:"TRAINING",
                4: lambda:"ACRO",
                5: lambda:"FBWA",
                6: lambda:"FBWB",
                7: lambda: "CRUISE",
                8: lambda: "UNKOWN",
                9: lambda: "UNKOWN",
                10: lambda: "AUTO",
                11: lambda: "RTL",
                12: lambda: "LOITER",
                13: lambda: "TAKEOFF",
                14: lambda: "AVIOD_ADSB",
                15: lambda: "GUIDED",
                16: lambda: "INITIALISING",
                17: lambda: "QSTABILIZE",
                18: lambda: "QHOVER",
                19: lambda: "QLOITER",
                20: lambda: "QLAND",
                21: lambda: "QRTL",
            }
        return mode_dict.get(mode,lambda: "Invalid option")()

    # 获取任务模式
    def task_mode_judge(self,task_mode):
        task_mode_dict={
            0: lambda: "INITIAL",       # 程序初启动
            1: lambda: "TAKEOFF",       # 无人机正在起飞，未达到指定高度
            2: lambda: "APPROACH",      # 无人机靠近
            3: lambda: "COMBAT",        # 无人机对抗
            4: lambda: "TASK_STOP",     # 无人机悬停
            5: lambda: "LAND",          # 无人机降落
            6: lambda: "FENCE",         # 无人机围栏阶段
            7: lambda: "MANUAL",        # 手飞阶段
        }
        return task_mode_dict.get(task_mode, lambda: "Invalid option")()

    # 获取阵营
    def side_judge(self, side):
        side_dict={
            1: lambda: "RED",       # 红方
            2: lambda: "BLUE",      # 蓝方
        }
        return side_dict.get(side, lambda: "Invalid option")()

    # 获取飞行器id
    def sysid_judge(self, sysid):
        sysid_dict = {
            161: lambda: "A1",       #
            162: lambda: "A2",       #
            163: lambda: "A3",          #
            164: lambda: "A4",          #
            165: lambda: "A5",        #
            177: lambda: "B1",    #
            178: lambda: "B2",  #
            179: lambda: "B3",  #
            180: lambda: "B4",  #
            181: lambda: "B5",  #
        }
        return sysid_dict.get(sysid, lambda: "Invalid option")()











