# -*- coding: UTF-8 -*-

from picamera import PiCamera
from aip import AipFace
import urllib.request
import RPi.GPIO as GPIO
import base64
import time
import cv2
import pymysql.cursors
import sys
import datetime

#打开数据库连接
conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='rapberry',port=3306)

#使用cursor()方法获取操作游标
cur=conn.cursor()

#获取当前时间
dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

#百度人脸识别API账号信息
APP_ID = '15777534'
API_KEY = 'iRCGkO9cV0iZOC4tNM4pjsIR'
SECRET_KEY ='WAaSwk2alCMc5fqefijAGOS9YEHLL4ga'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)#创建一个客户端用以访问百度云

#图像编码方式
IMAGE_TYPE='BASE64'
camera = PiCamera()#定义一个摄像头对象，首先使用picamera模块当中的PiCamera方法创建返回一个camera的对象
#用户组
GROUP = 'raspberry_pi'

#初始化相机并获取对原始相机捕获的引用
#照相函数
def getimage():
    #摄像界面为1024*768
    camera.resolution = (1024, 768) #设置图像的width和height
    camera.saturation = 80 # 设置图像视频的饱和度
    camera.framerate = 32 #这里可能用的Fraction是一个分数模块来存储分数1/6，保证分数运算的精度，记得调用模块
    
    time.sleep(0.1)#让相机预热
    camera.start_preview()#开始摄像
    time.sleep(2)
    camera.capture('faceimage.jpg')#拍照并保存
    time.sleep(2)
    
#对图片的格式进行转换
def transimage():
    f = open('faceimage.jpg','rb')
    img = base64.b64encode(f.read())
    return img
        
#上传到百度api进行人脸检测
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP);#在百度云人脸库中寻找有没有匹配的人脸
    if result['error_msg'] == 'SUCCESS':#如果成功了
        name = result['result']['user_list'][0]['user_id']#获取名字
        score = result['result']['user_list'][0]['score']#获取相似度
        print("相似度%d！" %score)
        if score > 80:#如果相似度大于80
            if name == 'linhaitao':
                #print("欢迎%s !" % name)
                print("欢迎林海涛")
                time.sleep(3)
            if name == 'mayun':
                #print("欢迎%s !" % name)
                print("欢迎马云")
                time.sleep(3)
            if name == "liyanhong":
                #print("欢迎%s !" % name)
                print("欢迎李彦宏")
            if name == "zhaoliying":
                #print("欢迎%s !" % name)
                print("欢迎赵丽颖")
        else:
            print("对不起，我不认识你！我不能给你开门！！！")
            name = 'Unknow'
            return 0
        current_time = time.asctime(time.localtime(time.time()))#获取当前时间

        #写入mysql
        try:
            #执行sql语句
            cur.execute("insert into person values('%s','%s')"%(name, dt))
            cur.close()
            #提交到数据库执行
            conn.commit()
            print("插入成功")
        except:
            #发生错误时回滚
            conn.rollback()
            print("插入失败")
        finally:
            #关闭数据库链接
            conn.close()
        return 1
    if result['error_msg'] == 'pic not has face':
        print('检测不到人脸，请把人脸对准摄像头重试，谢谢！')
        time.sleep(2)
        return 0
 
#主函数
if __name__ == '__main__':
    while True:
        print('准备开始人脸识别')
        if True:
            getimage()#拍照
            img = transimage()#转换照片格式
            res = go_api(img)#将转换了格式的图片上传到百度云
            if(res == 1):#是人脸库中的人
                print("开门")
            else:
                print("关门")
            print('稍等三秒进入下一个')
            time.sleep(3)
            
            