# coding:utf-8

# 本程序首先实现5楼A座的路径规划
# 计划输入 A513--A520，输出中间的节点

import xlrd
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
import pickle
import matplotlib.patches as mp
# 读取excel中的数据，生成“图”数据结构,应该将“图”持久化，不用每次都生成

class pathPlan(object):

    def __init__(self):
        pass 


    def read_excel_1(self,file_path_1):
        start = {"起点":[132256,39797,0]} #设置起点坐标
        elevator = {"电梯1-1":[138771,42445,0]} #电梯

        data = xlrd.open_workbook(file_path_1)
        table = data.sheet_by_index(0)
        numRows = table.nrows

        room2point = dict() # 每个房间节点对应的坐标 
        room2room = dict()  # 构建图模型的邻接表

        list_1 = []  # 奇数排
        list_2 = []  # 偶数排
        for i in range(1,58):
            data_used = table.row_values(i)[9:13]
            # print("data_used",data_used)
            if data_used[0]!=0.0:
                key = data_used[0][:-2]
                room2point[key] = data_used[1:]
                num = int(key[1:])  #表示房间号的数字

                if num%2==1 and key!="A107":
                    if key not in list_1:
                        list_1.append(key)
                else:
                    if key not in list_2:
                        list_2.append(key)
        # print("list1",list_1)
        # print("list2",list_2)

        # 根据两个list生成图的邻接表
        len_list_1 = len(list_1)
        len_list_2 = len(list_2)

        for index,val in enumerate(list_1):
            temp = []
            if index==0:  # 首要特殊处理，因为其前面没有
                # temp.append('A101')
                temp.append(list_1[index+1])
                room2room[val] = temp
                
            elif index == len_list_1-1:  # 尾部要特殊处理，因为其后面没有数值
                temp.append(list_1[index-1])
                room2room[val] = temp
            else:
                temp.append(list_1[index-1])
                temp.append(list_1[index+1])
                room2room[val] = temp
        
        for index,val in enumerate(list_2):
            temp = []
            if index==0:  # 首要特殊处理，因为其前面没有
                # temp.append('A501')
                temp.append(list_2[index+1])
                room2room[val] = temp
                
            elif index == len_list_2-1:  # 尾部要特殊处理，因为其后面没有数值
                temp.append(list_2[index-1])
                room2room[val] = temp
            else:
                temp.append(list_2[index-1])
                temp.append(list_2[index+1])
                room2room[val] = temp
        
        
        for index ,val in enumerate(list_2):
            if index<=2:  # 前3个是有顺序的，可以一一对应上
                temp1 = room2room[val]
                temp1.append(list_1[index])
                room2room[val] = temp1

                temp2 = room2room[temp1[-1]]
                temp2.append(val)
                room2room[temp1[-1]] = temp2
        # 手动添加部分
        room2point['起点'] = [136139,37217,0]
        room2point['电梯1-1'] = [138771,42445,0]
        room2point['LA10'] = [133520,41150,0]
        room2point['LA11'] = [119530,46620,0]
        room2point['LA12'] = [102300,52040,0]

        room2point['LB10'] = [97870,53130,0]
        room2point['LB11'] = [74070,53025,0]
        room2point['LB12'] = [64180,52920,0]

        room2point['电梯2-1'] = [72760,54770,0]
        room2point['电梯2-2'] = [72760,54770,6000]

        room2point['B214'] = [81790,57350,6000]

        room2room["起点"] = ['A107','A105','电梯1-1','LA10']
        room2room['A107'].append("起点")
        room2room['电梯1-1'] = ['起点']
        room2room['LA10'] = ['起点','LA11']
        room2room['LA11'] = ['LA10','LA12']
        room2room['LA12'] = ['LA11','LB10']
        room2room['LB10'] = ['LA12','LB11']
        room2room['LB11'] = ['LA10','LB12']
        room2room['LB12'] = ['LA11','电梯2-1']
        room2room['电梯2-1'] = ['LB12','电梯2-2']
        room2room['电梯2-2'] = ['B214']        
    

        # print("room2room",room2room)
        # print("room2point",room2point)
        return room2point,room2room

    def read_excel_5(self,file_path):
        data = xlrd.open_workbook(file_path)
        table = data.sheet_by_index(0)
        numRows = table.nrows

        room2point = dict() # 每个房间节点对应的坐标 
        room2room = dict()  # 构建图模型的邻接表

        list_1 = []  # 奇数排(除了A519 A521)
        list_2 = []  # 偶数排
        for i in range(1,183):
            data_used = table.row_values(i)[9:13]
            
            if data_used[0]!=0.0:
                key = data_used[0][:-2]
                room2point[key] = data_used[1:]
                num = int(key[1:])
                
                if key=='A501':
                    room2room[key]=['A503']  # A501,A526特殊处理
                elif key=='A526':
                    room2room[key]=['A524']  # A501,A526特殊处理

                elif num%2==1:
                    if key not in list_1 and key!='A519' and key!='A521':
                        list_1.append(key)
                    elif key=='A519' or key=='A521':
                        list_2.append(key)
                    
                else:
                    if key not in list_2:
                        list_2.append(key)

        # 根据两个list生成图的邻接表
        len_list_1 = len(list_1)
        len_list_2 = len(list_2)
        # print("第一个list长度",len_list_1)
        # print("第二个list长度",len_list_2)

        # 根据两个list构建邻接表
        for index,val in enumerate(list_1):
            temp = []
            if index==0:  # 首要特殊处理，因为其前面没有
                temp.append('A501')
                temp.append(list_1[index+1])
                room2room[val] = temp
                
            elif index == len_list_1-1:  # 尾部要特殊处理，因为其后面没有数值
                temp.append(list_1[index-1])
                room2room[val] = temp
            else:
                temp.append(list_1[index-1])
                temp.append(list_1[index+1])
                room2room[val] = temp

        for index,val in enumerate(list_2):
            temp = []
            if index==0:  # 首要特殊处理，因为其前面没有
                # temp.append('A501')
                temp.append(list_2[index+1])
                room2room[val] = temp
                
            elif index == len_list_2-1:  # 尾部要特殊处理，因为其后面没有数值
                temp.append(list_2[index-1])
                room2room[val] = temp
            else:
                temp.append(list_2[index-1])
                temp.append(list_2[index+1])
                room2room[val] = temp
        
        # 根据两个list构建单数排和双数排之间的连接关系
        i=-2
        for index ,val in enumerate(list_2):
            if index<=5:  # 前6个是有顺序的，可以一一对应上
                temp1 = room2room[val]
                temp1.append(list_1[index])
                room2room[val] = temp1

                temp2 = room2room[temp1[-1]]
                temp2.append(val)
                room2room[temp1[-1]] = temp2
            elif 6<=index<=10:
                temp1 = room2room[val]
                temp1.append(list_1[int(math.ceil(index/2))+2])
                # print("---1111---",list_1[int(index/2)+2])
                # print(val)
                # print(temp1)
                # print()
                room2room[val] = temp1

                temp2 = room2room[temp1[-1]]
                temp2.append(val)
                room2room[temp1[-1]] = temp2 
            elif len_list_2-2<=index<=len_list_2-1:
                
                temp1 = room2room[val]
                temp1.append(list_1[i])
                room2room[val] = temp1

                temp2 = room2room[temp1[-1]]
                temp2.append(val)
                room2room[temp1[-1]] = temp2
                i+=1
            
        room2room['电梯1-5'] = ['A517','A523','A520']
        room2room['A517'] = ['A519','A515','电梯1-5']
        room2room['A520'] = ['A521','A519','电梯1-5']
        room2room['A523'] = ['A525','A522','电梯1-5']
        room2point['电梯1-5'] = [136983,43821,16200]

        # print("room2point",room2point)  # 每个房间对应坐标,dict
        # print("room2room",room2room)  # 房间之间的邻接关系,dict
        return room2point,room2room



    def find_path(self,graph, start, end, path=[]):  # 找到一条路径
            path = path + [start]
            if start == end:
                return path
            if start not in graph:
                return None
            for node in graph[start]:
                if node not in path:
                    newpath = self.find_path(graph, node, end, path)  # 递归方法
                    if newpath: 
                        return newpath
            return None

    def find_shortest_path(self,graph, start, end, path=[]): # 找到最短路径
            path = path + [start]
            if start == end:
                return path
            if  start not in graph:
                return None
            shortest = None
            for node in graph[start]:
                if node not in path:
                    newpath = self.find_shortest_path(graph, node, end, path)  # 递归方法
                    if newpath:
                        if not shortest or len(newpath) < len(shortest):
                            shortest = newpath
            return shortest
    # 将路径变为坐标点序列
    def pathRoom2Point(self,pathroom,room2point):
        pathpoint = []
        for room in pathroom:
            pathpoint.append(room2point[room])
        
        return pathpoint


    def cal_theta(self,v1,v2):
        ans = np.dot(v1,v2)
        n1 = np.linalg.norm(v1)  # 模
        n2 = np.linalg.norm(v2)
        costheta = ans/(n1*n2)
        theta = math.acos(costheta)
        cross = np.cross(v1,v2)  # 叉积用于判断方向
        if cross>0.0:
            # print('左转')
            direction = 1
        elif cross<0.0:
            # print('右转')
            direction = -1
        else:
            # print('直行')
            direction = 0
        return theta,direction

# def gen_direction(pathroom,pathpoint):
#     pathdir = ["直行"]
#     length = len(pathroom)
#     for index in range(1,length-1):
#         v1 = listsub(pathpoint[index][:2],pathpoint[index-1][:2])
#         v2 = listsub(pathpoint[index+1][:2],pathpoint[index][:2])
#         theta,direction = cal_theta(v1,v2)
#         if theta>0.7854 and direction==1:
#             pathdir.append("左转")
#         elif theta>0.785 and direction==-1:
#             pathdir.append("右转")
#         else:
#             pathdir.append("直行")
#     return pathdir

    def gen_direction(self,pathroom,pathpoint):
        pathdir = ["直行"]
        length = len(pathroom)
        v1 = self.listsub(pathpoint[1][:2],pathpoint[0][:2])
        pathLeftOrRight = []
        if v1[0]>0:
            pathLeftOrRight.append("右")
        else:
            pathLeftOrRight.append("左")

        
        for index in range(1,length-1):
            v1 = self.listsub(pathpoint[index][:2],pathpoint[index-1][:2])
            v2 = self.listsub(pathpoint[index+1][:2],pathpoint[index][:2])
            theta,direction = self.cal_theta(v1,v2)
            if theta>0.7854 and direction==1:
                pathdir.append("左转")
                pathLeftOrRight.append("")
            elif theta>0.785 and direction==-1:
                pathdir.append("右转")
                pathLeftOrRight.append("")
            else:
                pathdir.append("直行")
                if v1[0]>0:
                    pathLeftOrRight.append("右")
                else:
                    pathLeftOrRight.append("左")

            
        return pathdir,pathLeftOrRight


    # 向量减法，list2-list1
    def listsub(self,list2,list1):
        list3 = []
        for index in range(len(list1)):
            list3.append(list2[index]-list1[index])
        return list3



    # 计算转折点的索引
    def index_of_turn(self,pathdir):
        turnindex = []
        for index in range(1,len(pathdir)):
            if pathdir[index]=="左转" or pathdir[index]=="右转":
                turnindex.append(index)
        return turnindex

    def findLastElevatorIndex(self,pathroom):
        index_list = []
        for index,room in enumerate(pathroom):
            if room.find("电梯")!=-1:
                index_list.append(index)
        return index_list[-1]





    def pathdir2sentence(self,pathroom,pathpoint,pathdir):
        sentence = ""
        if pathroom[1].find("电梯")!=-1:
            temp1 = "从当前位置，朝"+pathroom[1][2]+"号"+str(pathroom[1][:2])+"方向"+pathdir[0]
        else:
            temp1 = "从当前位置，朝"+str(pathroom[1])+"方向"+pathdir[0]
        sentence = sentence+temp1

        turnindex = self.index_of_turn(pathdir)
        lastElervatorIndex = self.findLastElevatorIndex(pathroom)
        # print("pathdir",pathdir)
        # print("turnindex",turnindex)

        for index in turnindex:
            if pathroom[index].find('电梯')!=-1:  # 这里是对“电梯进行处理
                # print("pathroom[index]",pathroom[index])
                if index!=lastElervatorIndex:  
                    temp1 = "，达到"+pathroom[index][2]+"号"+pathroom[index][:2]+"后，"+"上"+pathroom[lastElervatorIndex][-1]+"楼，"
                    sentence = sentence+temp1
                else:
                    temp1 = "然后朝"+pathroom[index+1]+"方向直行"
                    sentence = sentence+temp1
            else:
            
                temp1 = "达到"+pathroom[index]+"后，"+pathdir[index]
                sentence = sentence+temp1

            

        temp1 = "到达终点"+pathroom[-1]
        sentence = sentence+temp1

        return sentence


    # 将路径变为语句------
    def path2sentence(self,pathroom,pathpoint):
        sent1 = "从当前位置出发，途经"
        for room in pathroom[1:-1]:
            sent1 = sent1+room+' '
        sent1 = sent1+"到达终点"
        # print("sentence1",sent1)
        pathdir,_ = self.gen_direction(pathroom,pathpoint)
        # print(pathdir)

        sent2 = self.pathdir2sentence(pathroom,pathpoint,pathdir)
        # print("sentence2",sent2)
        sent = sent1+'\n'+sent2
        # print("sent",sent)
        return sent


    def gen_points(self,file_path):
        data = xlrd.open_workbook(file_path)
        table = data.sheet_by_index(0)
        nrows = table.nrows  # 一共多少行
        
        # max_x = max(table.col_values(2)[1:])
        # max_y = max(table.col_values(3)[1:])
        # print(nrows)
        points = []
        temp = []
        for i in range(1,nrows):
            if table.row_values(i)[0:14]!=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]:
                a = []
                a.append(table.row_values(i)[2])
                a.append(table.row_values(i)[3])
                a.append(table.row_values(i)[5])
                temp.append(a)
            else:
                points.append(temp)
                temp = []
                
        return points

    def numOfFloor(self,file_path):
        a = file_path.split('/')
        return a[-1][:2]

# def gen_map(points,pathpoint,pathroom,pic_name,file_path):
#     # points用于绘制静态地图，pathpoint用于绘制动态的点
#     zhfont = matplotlib.font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/ukai.ttc")
#     plt.figure(figsize=(12,8))
#     X = []
#     Y = []
#     for point in points:
#         for i in range(len(point)):
            
#             X.append(point[i][0])
#             Y.append(point[i][1])
#         plt.plot(X,Y,'b')
#         X = []
#         Y = []        
#     X = []
#     Y = []
#     for i,p in enumerate(pathpoint):
#         X.append(p[0])
#         Y.append(p[1])
#         plt.annotate(pathroom[i],xy=(p[0],p[1]),fontproperties = zhfont)
#     plt.plot(X,Y,'<')#这里改，在点上加字！

#     name = numOfFloor(file_path)
#     plt.text(x = 70000,y = 110000,s = name,fontsize=20)
       
#     plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)  # 去掉留白
#     # plt.margins(0,0)
#     plt.savefig(pic_name,pad_inches = 0)
#     # plt.show()

    def gen_map(self,c1,c2,pathroomsplit):
        zhfont = matplotlib.font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/ukai.ttc")
        # plt.figure(figsize=(12,8))
        plt.figure()
        lengthoffloor = 120
        print("C1",c1)
        for i in range(len(c1)):
            plt.annotate(pathroomsplit[0][i],xy=(c1[i][0],c1[i][1]),fontproperties = zhfont)
        plt.plot(c1.T[0],c1.T[1],'c-o')

        xAdd = c1[-1][0]
        yAdd = lengthoffloor

        for i,xyz in enumerate(c2):
            c2[i][0] = c2[i][0]+xAdd
            c2[i][1] = c2[i][1]+yAdd

        for i in range(len(c2)):
            plt.annotate(pathroomsplit[1][i],xy=(c2[i][0],c2[i][1]),fontproperties = zhfont)
        plt.plot(c2.T[0],c2.T[1],'c-o')

        plt.plot([c1.T[0][-1],c2.T[0][0]],[c1.T[1][-1],c2.T[1][0]],'r--o')

        # 画电梯
        # 求电梯连线中点
        x = (c1.T[0][-1]+c2.T[0][0])/2
        y = (c1.T[1][-1]+c2.T[1][0])/2

        rect1 = mp.Rectangle((x-5, y+30), 10, 15, color='b', alpha=1.0, angle=0)
        rect2 = mp.Rectangle((x-5, y-30), 10, 15, color='b', alpha=1.0, angle=0)
        # rect2 = mp.Rectangle((x-5, y-30), 10, 15, color='r', alpha=0.5, angle=0)
        rect1.set_zorder(1) # 设置图层
        rect2.set_zorder(1) 
        plt.gca().add_patch(rect1)
        plt.gca().add_patch(rect2)
        # 加注释
        plt.annotate("乘坐电梯",xy=(x+2,y+5),fontproperties = zhfont)
        # print("画了没")



        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)  # 去掉留白
        # plt.margins(0,0)
        plt.savefig("./static/写意图2",pad_inches = 0)

    def split_path(self,pathroom,pathpoint):
        if "电梯1-1" in pathroom:
            index = pathroom.index("电梯1-1")
        elif "电梯2-1" in pathroom:
            index = pathroom.index("电梯2-1")
        pathroomhalf1 = pathroom[:index+1]
        pathroomhalf2 = pathroom[index+1:]

        pathpointhalf1 = pathpoint[:index+1]
        pathpointhalf2 = pathpoint[index+1:]

        # print("pathroomhalf1",pathroomhalf1)
        # print("pathroomthalf2",pathroomhalf2)
        return pathroomhalf1,pathroomhalf2,pathpointhalf1,pathpointhalf2

    def splitpath(self,pathroom,pathpoint):
        splitpoint = 0
        state = 0
        for index,room in enumerate(pathroom):
            if re.search('电梯',room):
                splitpoint = index
                break
            else:
                pass
        if splitpoint==0: # 不存在跨层
            return state,index,pathroom,pathpoint
        else:
            state = 1  # 存在跨层
            return state,index,[pathroom[:splitpoint+1],pathroom[splitpoint+1:]],[pathpoint[:splitpoint+1],pathpoint[splitpoint+1:]]

    def gen_xyz(self,pathpoint,pathroom,pathdir,leftorright):
        print("pathdir",pathdir)
        # zhfont = matplotlib.font_manager.FontProperties(fname="/usr/share/fonts/truetype/arphic/ukai.ttc")
        # plt.figure(figsize=(12,8))
        lengthofroom = 20
        X = [0]
        Y = [0]
        Z = []
        for i,xyz in enumerate(pathpoint):
            z = xyz[2]
            Z.append(z)
            # print("i",i)
            if i<len(pathpoint)-1:
                
                    if pathdir[i]=="直行":
                        if leftorright[i]=="左":
                            X.append(X[-1]+lengthofroom)
                            Y.append(0)
            
        coor = np.array([X,Y,Z])
        # print("之前",coor)
        c = coor.T
        # print("之后",c)
        return c

    def gen_path(self,start,end):
        # start = "A513",end = "A520"
        # /home/liu/00毕业课题/developing/03pathplan/nav/excel_data
        
        # file_path_1 = "./nav/excel_data/1F_改.xlsx"
        # file_path_5 = "./nav/excel_data/5F_改.xlsx"
        # numOfFloor(file_path_1)

        # file_path_1 = "../../../03pathplan/nav/excel_data/1F_改.xlsx"
        # file_path_5 = "../../../03pathplan/nav/excel_data/5F_改.xlsx"

        file_path_1 = "/home/liu/00毕业课题/developing/03pathplan/nav/excel_data/1F_改.xlsx"
        file_path_5 = "/home/liu/00毕业课题/developing/03pathplan/nav/excel_data/5F_改.xlsx"
        
        room2point_1, room2room_1 = self.read_excel_1(file_path_1)
        room2point_5, room2room_5 = self.read_excel_5(file_path_5)
        # print("room2room5",room2room_5)
        room2room = {**room2room_1,**room2room_5}  #l两个字典合并
        # print("room2room",room2room)
        room2room['电梯1-1'].append('电梯1-5')
        room2room['电梯1-5'].append('电梯1-1')
        room2point = {**room2point_1, **room2point_5}
        # print("room2point= ",room2point)

        # f = open('./room2point','wb')
        # pickle.dump(room2point,f)
        # f.close()

        

        pathroom = self.find_shortest_path(room2room,start,end)
        print("pathroom= ",pathroom)

        pathpoint = self.pathRoom2Point(pathroom,room2point)
        print("pathPoint= ",pathpoint)

        sent = self.path2sentence(pathroom,pathpoint)
        print("sent= ",sent)

        pathroomhalf1,pathroomhalf2,pathpointhalf1,pathpointhalf2 = self.split_path(pathroom,pathpoint)

        # 生成图片
        # points_1 = gen_points(file_path_1)
        # gen_map(points_1,pathpointhalf1,pathroomhalf1,'./static/1.png',file_path_1)

        # points_5 = gen_points(file_path_5)
        # gen_map(points_5,pathpointhalf2,pathroomhalf2,'./static/2.png',file_path_5)
        state,index,pathroomsplit,pathpointsplit = self.splitpath(pathroom,pathpoint)
        print("pathroomsplit",pathroomsplit)
        print("pathpointsplit",pathpointsplit)
        
        pathdir,leftorright = self.gen_direction(pathroomsplit[1],pathpointsplit[1])
        # print(pathroomsplit[1])
        print("pathdir",pathdir)
        # print(leftorright)
        
        c1 = self.gen_xyz(pathpointsplit[0],pathroomsplit[0],pathdir,leftorright)
        c2 = self.gen_xyz(pathpointsplit[1],pathroomsplit[1],pathdir,leftorright)
        self.gen_map(c1,c2,pathroomsplit)

        return sent

# gen_path('起点','A503')

    
# file_path_1 = "./nav/excel_data/1F_改.xlsx"
# read_excel_1(file_path_1)

# def test():
#     pathPlaner = pathPlan()
#     pathPlaner.gen_path("起点","A513")

# test()

