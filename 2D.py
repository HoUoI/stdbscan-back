import os
import matplotlib.pyplot as plt
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
# 假设聚类结果存储在一个名为"labels"的列表中
labels = []
# 假设数据点的坐标存储在一个名为"points"的列表中
points = []
labels_with_points = []
clusters = {}

folder_path = "E:\\graduation\\back\\2Dresult"
files = os.listdir(folder_path)
for file in files:
    file_path = os.path.join(folder_path, file)
    if os.path.isfile(file_path) and file_path.endswith(".txt"):
        with open(file_path, "r") as openFile:
            line1 = openFile.readline()
            line2 = openFile.readline()
            n_lines_to_skip = int(line2.strip().split()[0])
            for _ in range(n_lines_to_skip):
                next(openFile)
            line = openFile.readline()
            while line:
                ls = line.split(", ")
            
                label = -1
                point = ()
                if ls[1].isnumeric():
                    label = int(ls[1])
                ls[0] = ls[0].lstrip("[").rstrip("]").split(",")
                if is_float(ls[0][0]) and is_float(ls[0][1]):
                    point = (float(ls[0][0]), float(ls[0][1]))
                if label != -1 and point != ():
                    if label not in clusters:
                        clusters[label] = []
                    clusters[label].append(point)
                    labels_with_points.append((label, point))
                    if labels.count(label) == 0:
                        labels.append(label)
                    points.append(point)
                line = openFile.readline()



print(labels)
print(points)
print(labels_with_points)


# 可视化聚类结果
colors = ['y', 'r', 'g', 'b', 'c', 'm', 'k', 'orange', 'lightcoral', 'fuchsia', 'slategray', 'lime', 'brown', 'olive', 'purple', 'teal', 'gold', 'navy', 'pink', 'skyblue', 'peru', 'crimson', 'darkgreen', 'orchid', 'steelblue', 'sienna', 'royalblue', 'indigo', 'darkorange', 'darkviolet', 'darkred', 'darkcyan', 'darkmagenta', 'darkslategray', 'darkolivegreen', 'darkgoldenrod', 'darkorchid', 'darkslateblue', 'darkturquoise', 'darkkhaki']  # 指定不同类别的颜色
for label, cluster_points in clusters.items():
    x = [point[0] for point in cluster_points]
    y = [point[1] for point in cluster_points]
    plt.scatter(x, y, s=10, c=colors[label], label=f'Cluster {label}', marker='*')

plt.xlabel('longitude')
plt.ylabel('latitude')
plt.show()