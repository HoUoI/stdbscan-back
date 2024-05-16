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
        self.refer_time = datetime(2008, 2, 2, 0, 0,0)
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
                        if self.option == 1: # 聚类结果3D可视化
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
                            
    def draw_3D(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # 绘制所有数据点
        for label, time_point in self.clusters.items():
            if label != 0:
                t = [tp[0] for tp in time_point]
                x = [tp[1][0] for tp in time_point]
                y = [tp[1][1] for tp in time_point]
                ax.scatter(x, y, t, c=self.colors[(label % 40)], marker='o')

        # 设置坐标轴标签
        ax.set_xlabel('longitude')
        ax.set_ylabel('latitude')
        ax.set_zlabel('time')
        
        plt.savefig("./visualimg/resultvisual.png")
        # plt.show()

def visual1():
    folder_path = "E:\\graduation\\back\\result"
    res = ResultMap3D(folder_path, 1)
    res.readFiles()
    res.draw_3D()

if __name__ == "__main__":
    visual1()