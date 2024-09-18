# Python地面站
作者:JuanRenGolden

## 2024年9月18日
经过测试，实机连接10架无人机成功。

## 2024年9月16日

简介：采用TCP通信的python地面站，基于双云5.8G基站实现通信组网，能够实现多架飞行器消息的实时收发和显示；采用天地图获取地图信息，实现实时地图显示。正在实机测试中。

需要环境：tkinter, cartopy

方法：
1. 安装支持环境，并自行前往天地图https://vgimap.tianditu.gov.cn/注册
2. 将key写入geoMap_Class.py
3. 联网后直接运行main_page.py

后续：
1. 实现多机实机测试
2. 完善线程启停
3. 实现在地图上的实时轨迹绘制


