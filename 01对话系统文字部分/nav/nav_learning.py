# coding:utf-8
import numpy
from pylab import *
from PIL import Image


# 定义一个含有障碍物的20×20的栅格地图
# 10表示可通行点
# 0表示障碍物
# 7表示起点
# 5表示终点
# map_grid = numpy.full((20, 20), int(10), dtype=numpy.int8)  # 初始化全是可通行点
# # print(map_grid)
# map_grid[3, 3:8] = 0
# map_grid[3:10, 7] = 0
# map_grid[10, 3:8] = 0
# map_grid[17, 13:17] = 0
# map_grid[10:17, 13] = 0
# map_grid[10, 13:17] = 0
# map_grid[300, 200] = 7
# map_grid[15, 15] = 5
# 画出定义的栅格地图

# plt.imshow(map_grid, cmap=plt.cm.hot, interpolation='nearest', vmin=0, vmax=10)
# plt.colorbar()
# xlim(-1, 20)  # 设置x轴范围
# ylim(-1, 20)  # 设置y轴范围
# my_x_ticks = numpy.arange(0, 20, 1)
# my_y_ticks = numpy.arange(0, 20, 1)
# plt.xticks(my_x_ticks)
# plt.yticks(my_y_ticks)
# plt.grid(True)
# plt.show()


class AStar(object):
    """
    创建一个A*算法类
    """

    def __init__(self,s,e,shape_of_map):
        """
        初始化
        """
        self.f = 0
        self.g = 0
        self.last_point = numpy.array([])  # 上一个目标点不断取得更新
        self.current_point = numpy.array([])  # 当前目标点不断取得更新
        self.open = numpy.array([[], []])  # 先创建一个空的open表
        self.closed = numpy.array([[], []])  # 先创建一个空的closed表
        self.start = numpy.array(s)  # 起点坐标
        self.goal = numpy.array(e)  # 终点坐标
        self.map_shape = shape_of_map

    def h_value_tem(self, cur_p):
        """
        计算拓展节点和终点的h值
        :param cur_p:子搜索节点坐标
        :return:
        """
        h = (cur_p[0] - self.goal[0]) ** 2 + (cur_p[1] - self.goal[1]) ** 2
        h = numpy.sqrt(h)  # 计算h
        return h

    def g_value_tem(self, chl_p, cu_p):
        """
        计算拓展节点和父节点的g值
        其实也可以直接用1或者1.414代替
        :param chl_p:子节点坐标
        :param cu_p:父节点坐标，也就是self.current_point
        :return:返回子节点到父节点的g值，但不是全局g值
        """
        # 这里可以加速！！
        g1 = cu_p[0] - chl_p[0]
        g2 = cu_p[1] - chl_p[1]
        g = g1 ** 2 + g2 ** 2
        g = numpy.sqrt(g)
        return g

    def f_value_tem(self, chl_p, cu_p):
        """
        求出的是临时g值和h值的和，还需加上累计g值得到全局f值
        :param chl_p: 父节点坐标
        :param cu_p: 子节点坐标
        :return:
        """
        f = self.g_value_tem(chl_p, cu_p) + self.h_value_tem(cu_p)
        return f

    def min_f(self):
        """
        找出open中f值最小的节点坐标，记录为current_point
        :return:返回open表中最小值的位置索引和在map_grid中的坐标
        对撞墙后的处理方式是，随机选择一个方向进行搜索
        并且将open列表清零，不然一直是死循环
        这种处理方式以后待改进！！！
        """
        tem_f = []  # 创建一个记录f值的临时列表
        for i in range(self.open.shape[1]):
            # 计算拓展节点的全局f值
            f_value = self.f_value_tem(self.current_point, self.open[:, i]) + self.g
            tem_f.append(f_value)
        index = tem_f.index(min(tem_f))  # 返回最小值索引
        location = self.open[:, index]  # 返回最小值坐标
        # print('打印位置索引和地图坐标：')
        # print(index, location)
        return index, location

    def child_point(self, x):
        """
        拓展的子节点坐标
        :param x: 父节点坐标
        :return: 无返回值，子节点存入open表
        当搜索的节点撞墙后，如果不加处理，会陷入死循环
        """
        # self.open = numpy.array([[], []])  # 先创建一个空的open表
        # 开始遍历周围8个节点
        for j in range(-1, 2, 1):
            for q in range(-1, 2, 1):
                if j == 0 and q == 0:  # 搜索到父节点去掉
                    continue

                # print(map_grid[int(x[0] + j), int(x[1] + q)])
                if map_grid[int(x[0] + j), int(x[1] + q)] == 0:  # 搜索到障碍物去掉
                    continue
                if x[0] + j < 0 or x[0] + j > self.map_shape[0]-1 or x[1] + q < 0 or x[1] + q > self.map_shape[1]-1:  # 搜索点出了边界去掉
                    continue
                # 在open表中，则去掉搜索点
                a = self.judge_location(x, j, q, self.open)
                if a == 1:
                    continue
                # 在closed表中,则去掉搜索点
                b = self.judge_location(x, j, q, self.closed)
                if b == 1:
                    continue

                m = numpy.array([x[0] + j, x[1] + q])
                self.open = numpy.c_[self.open, m]  # 搜索出的子节点加入open
                # print('打印第一次循环后的open：')
                # print(self.open)

    def judge_location(self, x, j, q, list_co):
        """
        判断拓展点是否在open表或者closed表中
        :return:
        """
        jud = 0
        for i in range(list_co.shape[1]):

            if x[0] + j == list_co[0, i] and x[1] + q == list_co[1, i]:

                jud = jud + 1
            else:
                jud = jud
        # if a != 0:
        #     continue
        return jud

    def draw_path(self):
        for i in range(self.closed.shape[1]):
            
            x = self.closed[:, i]
            print("xxxx  ",x)

            map_grid[int(x[0]), int(x[1])] = 0
        
        im_2 = Image.fromarray(map_grid)
        im_2.convert('L')
        im_2.show()


        # plt.imshow(map_grid, cmap=plt.cm.hot, interpolation='nearest', vmin=0, vmax=10)
        # plt.colorbar()
        # xlim(-1, 20)  # 设置x轴范围
        # ylim(-1, 20)  # 设置y轴范围
        # my_x_ticks = numpy.arange(0, 20, 1)
        # my_y_ticks = numpy.arange(0, 20, 1)
        # plt.xticks(my_x_ticks)
        # plt.yticks(my_y_ticks)
        # plt.grid(True)
        # plt.show()


    def main(self):
        """
        main函数
        :return:
        """
        self.open = numpy.column_stack((self.open, self.start))  # 起点放入open
        self.current_point = self.start  # 起点放入当前点，作为父节点
        # self.closed
        ite = 1
        while ite <= 200000:
            # print("ite",ite)
            # open列表为空，退出
            if self.open.shape[1] == 0:
                print('路径规划失败！')
                return

            last_point = self.current_point  # 上一个目标点不断取得更新

            index, self.current_point = self.min_f()  # 判断open表中f值
            # print('检验第%s次当前点坐标' % ite)
            # print(self.current_point)

            # 选取open表中最小f值的节点作为best，放入closed表
            self.closed = numpy.c_[self.closed, self.current_point]

            if self.current_point[0] == self.goal[0] and self.current_point[1] == self.goal[1]:  # 如果best是目标点，退出
                print('路径规划成功！')
                return

            self.child_point(self.current_point)  # 生成子节点
            self.open = delete(self.open, index, axis=1)  # 删除open中最优点
            # print(self.open)

            self.g = self.g + self.g_value_tem(self.current_point, last_point)

            ite = ite+1

im_1 = Image.open('./test.png')
L = im_1.convert('L')
# L = np.full((400,400),255,dtype=numpy.int8)
map_grid = np.asarray(L)
map_grid.flags.writeable=True  # 可写模式
a1 = AStar(s=[100,200],e=[105,15],shape_of_map=[400,400])
a1.main()
a1.draw_path()
