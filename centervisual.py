import os
import string
from datetime import datetime
import numpy as np
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

class ResultMap3D:
    def __init__(self, dir_path: string, option: int):
        # 标准时间
        self.referTime = datetime(2008, 2, 2, 18, 44, 58)
        self.time_format = '%Y-%m-%d %H:%M:%S'
        self.dir_path = dir_path
        self.option = option
        # 将聚类结果储存在一个label的列表之中
        self.labels = []
        # 将数据点储存在一个points的列表之中
        self.points = []
        # 将数据点的时间储存在一个time_span之中
        self.time_span = [float('inf'),0]
        self.clusters = {}  # {label: (time, [x, y])}
        self.cluster_centers = {}  # {label: (x_center, y_center, t_center)}
        self.colors = ['y', 'r', 'g', 'b', 'c', 'm', 'k', 'orange', 'lightcoral', 'fuchsia', 'slategray', 'lime', 'brown', 'olive', 'purple', 'teal', 'gold', 'navy', 'pink', 'skyblue', 'peru', 'crimson', 'darkgreen', 'orchid', 'steelblue', 'sienna', 'royalblue', 'indigo', 'darkorange', 'darkviolet', 'darkred', 'darkcyan', 'darkmagenta', 'darkslategray', 'darkolivegreen', 'darkgoldenrod', 'darkorchid', 'darkslateblue', 'darkturquoise', 'darkkhaki']

    def readFiles(self):
        files = os.listdir(self.dir_path)
        for file in files:
            file_path = os.path.join(self.dir_path, file)
            if os.path.isfile(file_path) and file_path.endswith(".txt"):
                with open(file_path, "r") as openFile:
                    line1 = openFile.readline()
                    line2 = openFile.readline()
                    n_lines_to_skip = int(line2.strip().split()[0])
                    for _ in range(n_lines_to_skip):
                        next(openFile)
                    line = openFile.readline()
                    while line:
                        if self.option == 0: # 原始数据可视化
                            ls = line.split(",")
                            label = -1
                            point = ()
                            tp = ls[1]
                            t = datetime.strptime(tp, self.time_format)
                            diff_second = (t - self.referTime).days * 86400 + (t - self.referTime).seconds
                            if self.time_span.count(t) == 0:
                                self.time_span.append(t)
                            print(t)
                            if ls[0].isnumeric():
                                label = int(ls[0])
                            if is_float(ls[2]) and is_float(ls[3]):
                                point = (float(ls[2]), float(ls[3]))
                            if label != -1 and point != ():
                                if label not in self.clusters:
                                    self.clusters[label] = []
                                self.clusters[label].append((diff_second, point))
                                if self.labels.count(label) == 0:
                                    self.labels.append(label)
                                self.points.append(point)
                            line = openFile.readline()
                        elif self.option == 1: # 聚类结果3D可视化
                            ls = line.split(", ")
                            label = -1
                            point = ()
                            if ls[1].isnumeric():
                                label = int(ls[1])
                            ls[0] = ls[0].lstrip("[").rstrip("]").split(",")
                            diff_second = float(ls[0][2])
                            if is_float(ls[0][0]) and is_float(ls[0][1]):
                                point = (float(ls[0][0]), float(ls[0][1]))
                            if label != -1 and point != ():
                                if label not in self.clusters:
                                    self.clusters[label] = []
                                self.clusters[label].append((diff_second, point))
                                if self.labels.count(label) == 0:
                                    self.labels.append(label)
                                self.points.append(point)
                            if float(ls[0][2])<self.time_span[0] :self.time_span[0]=float(ls[0][2])
                            if float(ls[0][2])>self.time_span[1] :self.time_span[1]=float(ls[0][2])
                            line = openFile.readline()
    
    def calculate_cluster_centers(self):
        for label, time_point in self.clusters.items():
            t_sum = 0
            x_sum = 0
            y_sum = 0
            num_points = len(time_point)
            for tp in time_point:
                t_sum += tp[0]
                x_sum += tp[1][0]
                y_sum += tp[1][1]
            t_center = t_sum / num_points
            x_center = x_sum / num_points
            y_center = y_sum / num_points
            self.cluster_centers[label] = (x_center, y_center, t_center, num_points)

        
    def draw_3D(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # print(len(self.points))
        # 设置坐标轴标签
        ax.set_xlabel('longitude')
        ax.set_ylabel('latitude')
        ax.set_zlabel('time')

        # 计算并绘制聚类中心
        self.calculate_cluster_centers()
        for label, center in self.cluster_centers.items():
            if label != 0:
                x_center, y_center, t_center, num_points = center
                marker_size = num_points * 0.5  # 设定标记大小，点数越多，标记越大
                ax.scatter(x_center, y_center, t_center, c=self.colors[(label%40)], marker='o', s=marker_size)
        plt.savefig("./visualimg/centervisual.png")
        # plt.show()

def visual2():
    folder_path = "E:\\graduation\\back\\result"
    res = ResultMap3D(folder_path, 1)
    res.readFiles()
    res.draw_3D()

if __name__ == "__main__":
    visual2()