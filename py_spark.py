import subprocess
import time

# 启动 Spark Shell
spark_shell_cmd = r'D:\spark-2.1.1\bin\spark-shell.cmd'
subprocess.Popen([spark_shell_cmd], shell=True)

# 等待 Spark Shell 正确启动，这里等待 60 秒
time.sleep(10)
dataset='TDrive_CubeSP_Greedy'
jarpath=[]
datapath=[]
st=[]
en=[]
if dataset=='taxi':
    jarpath='D:\\spark-2.1.1\\examples\\jars\\taxi9keven.jar'
    datapath='0'
elif dataset=='chengdu':
    jarpath='D:\\spark-2.1.1\\examples\\jars\\chengdu10weven.jar'
    datapath='D:\\START\\distribute-ST-cluster\\code\\DBScan-VeG\\SparkMaven\\src\\main\\resources\\point_r_10w'
elif dataset=='TDrive_9k':
    jarpath='D:\\spark-2.1.1\\examples\\jars\\ex\\CubeSP_KL_TDrive.jar'
    datapath='D:\\START\\distribute-ST-cluster\\code\\DBScan-VeG\\SparkMaven\\src\\main\\resources\\taxi_log_2008_by_id'
    st='100'
    en='110'
elif dataset=='TDrive_15w':
    jarpath='D:\\spark-2.1.1\\examples\\jars\\ex\\CubeSP_KL_TDrive.jar'
    datapath='D:\\START\\distribute-ST-cluster\\code\\DBScan-VeG\\SparkMaven\\src\\main\\resources\\taxi_log_2008_by_id'
    st='1'
    en='100'
elif dataset=='TDrive_CubeSP_Greedy':
    jarpath='D:\\spark-2.1.1\\examples\\jars\\ex\\CubeSP_Greedy_TDrive.jar'
    datapath='D:\\START\\distribute-ST-cluster\\code\\DBScan-VeG\\SparkMaven\\src\\main\\resources\\taxi_log_2008_by_id'
    st='100'
    en='110'
# 提交 Spark 应用程序
spark_submit_cmd = r'D:\spark-2.1.1\bin\spark-submit.cmd'
# app_arguments = [
#     spark_submit_cmd,
#     '--class',
#     'org.apache.spark.Scala.DBScan3DDistributed.DBScan3DDistributedTest',
#     '--master',
#     'local[2]',
#     jarpath,
#     datapath,
#     'E:\\graduation\\back\\result\\result.txt',
#     '0.008',
#     '1000',
#     '40',
#     '10',
#     '0.05',
#     '0.05',
#     '3500'
# ]
# app_arguments = [
#     spark_submit_cmd,
#     '--class',
#     'org.apache.spark.Scala.DBScan3DDistributed.DBScan3DDistributedTest',
#     '--master',
#     'local[2]',
#     jarpath,
#     datapath,
#     'E:\\graduation\\back\\result\\result.txt',
#     '0.005',
#     '200',
#     '100',
#     '100',
#     '0.04',
#     '0.04',
#     '50'
# ]
app_arguments = [
    spark_submit_cmd,
    '--class',
    'org.apache.spark.Scala.DBScan3DDistributed.DBScan3DDistributedTest',
    '--master',
    'local[2]',
    jarpath,
    datapath,
    'E:\\graduation\\back\\result\\result.txt',
    '0.008',
    '1000',
    '40',
    '100',
    '0.032',
    '0.032',
    '4000',
    st,
    en,
]
subprocess.Popen(app_arguments, shell=True)
