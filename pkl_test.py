import pickle

# 用于生成规定格式的pkl文件
if __name__ == "__main__":
    detection = [
        {
            'x1': 100,  #
            'y1': 150,
            'x2': 200,
            'y2': 250,
            'cls': "Hostlie",  # 目标类别
        },
        {
            'x1': 200,  #
            'y1': 250,
            'x2': 300,
            'y2': 450,
            'cls': "Friend",  # 目标类别
        },
    ]
    state = {'side': 0,
             'sysid': 0,
             'flight_mode': 'STABILIZE',
             'task_state': 1,
             'lat': 1,
             'lon': 0,
             'alt': 0,
             'hdg': 0,
             'tar': 177,
             'Detections': detection
             }
    '''
    with open('UAV10_STATE.pkl','wb') as file:
        pickle.dump(state,file)
        print("文件已创建")
    '''
    for i in range(161,166):
        data_address = f'UAV{i-160}_STATE.pkl'
        state['side'] = 1
        state['sysid'] =i
        with open(data_address,'wb') as file:
            pickle.dump(state, file)
            print(f"文件{data_address}已创建")

    for i in range(177,182):
        data_address = f'UAV{i-171}_STATE.pkl'
        state['side'] = 2
        state['sysid'] =i
        with open(data_address,'wb') as file:
            pickle.dump(state, file)
            print(f"文件{data_address}已创建")




