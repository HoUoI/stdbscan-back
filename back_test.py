from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import time
from resultvisual import visual1
from centervisual import visual2
app = Flask(__name__)
CORS(app)

@app.route('/cluster', methods=['GET'])
def cluster():
    # 从前端获取参数
    dataset = request.args.get('dataset')
    eps1 = request.args.get('eps1')
    eps2 = request.args.get('eps2')
    minpts = request.args.get('minpts')
    k = request.args.get('k')
    x_bounding = request.args.get('x_bounding')
    y_bounding = request.args.get('y_bounding')
    t_bounding = request.args.get('t_bounding')

    # 启动 Spark Shell
    spark_shell_cmd = r'D:\spark-2.1.1\bin\spark-shell.cmd'
    subprocess.Popen([spark_shell_cmd], shell=True)

    # 等待 Spark Shell 正确启动，这里等待 60 秒
    time.sleep(10)

    jarpath=[]
    datapath=[]
    st=[]
    en=[]
    if dataset=='TDrive_ESP':
        jarpath='D:\\spark-2.1.1\\examples\\jars\\ex\\ESP_TDrive.jar'
        datapath='0'
        st='0'
        en='0'
    elif dataset=='chengdu':
        jarpath='D:\\spark-2.1.1\\examples\\jars\\chengdu10weven.jar'
        datapath='D:\\START\\distribute-ST-cluster\\code\\DBScan-VeG\\SparkMaven\\src\\main\\resources\\point_r_10w'
        st='0'
        en='0'
    elif dataset=='TDrive_CubeSP_KL':
        jarpath='D:\\spark-2.1.1\\examples\\jars\\ex\\CubeSP_KL_TDrive.jar'
        datapath='D:\\START\\distribute-ST-cluster\\code\\DBScan-VeG\\SparkMaven\\src\\main\\resources\\taxi_log_2008_by_id'
        st='100'
        en='110'
    elif dataset=='TDrive_CubeSP_Greedy':
        jarpath='D:\\spark-2.1.1\\examples\\jars\\ex\\CubeSP_Greedy_TDrive.jar'
        datapath='D:\\START\\distribute-ST-cluster\\code\\DBScan-VeG\\SparkMaven\\src\\main\\resources\\taxi_log_2008_by_id'
        st='100'
        en='110'
    elif dataset=='NYtrip':
        jarpath='D:\\spark-2.1.1\\examples\\jars\\ex\\NYtrip.jar'
        datapath='D:\\START\\distribute-ST-cluster\\code\\DBScan-VeG\\SparkMaven\\src\\main\\resources\\taxi_log_2008_by_id'
        st='0'
        en='0'

    # 提交 Spark 应用程序
    spark_submit_cmd = r'D:\spark-2.1.1\bin\spark-submit.cmd'
    app_arguments = [
        spark_submit_cmd,
        '--class',
        'org.apache.spark.Scala.DBScan3DDistributed.DBScan3DDistributedTest',
        '--master',
        'local[2]',
        jarpath,
        datapath,
        'E:\\graduation\\back\\result\\result.txt',
        eps1,
        eps2,
        minpts,
        k,
        x_bounding,
        y_bounding,
        t_bounding,
        st,
        en,
    ]
    spark_process = subprocess.Popen(app_arguments, shell=True)
    spark_process.wait()
    
    file_path = "./result/result.txt"  # 替换为你的文件路径
    allcluster=[]
    with open(file_path, "r") as file:
        totaltime = file.readline().strip()  # 读取第一行
        totalcluster = file.readline().strip()  # 读取第二行
        n_lines_to_skip = int(totalcluster.split()[0])
        for _ in range(n_lines_to_skip):
            s = file.readline()
            allcluster.append(s.strip())  # 将读取的行添加到列表中，并去除首尾空白字符
            print(s)
    data = {'totaltime': totaltime, 'totalcluster': totalcluster,'allcluster': allcluster}
    return jsonify(data)

@app.route('/resultvisual', methods=['GET'])
def revisual():
    visual1()
    image_path = './visualimg/resultvisual.png'
    return send_file(image_path)


@app.route('/centervisual', methods=['GET'])
def cevisual():
    visual2()
    image_path = './visualimg/centervisual.png'
    return send_file(image_path)

if __name__ == '__main__':
    app.run(debug=True)

