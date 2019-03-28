# -*- coding: UTF-8 -*-
'''
Haar Cascade Face detection with OpenCV  
'''

from picamera import PiCamera
from aip import AipFace
import urllib.request
import RPi.GPIO as GPIO
import base64
import time
import cv2
import pymysql.cursors
import pymysql
import sys
import datetime
import urllib3

import numpy as np
import cv2

# OpenCV 包含很多预训练分类器
#加载分类器
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

# For each person, enter one numeric face id
face_id = input('\n enter user id end press <enter > ==>  ')

count = 0#测试用

#在循环内部调用摄像头，并以grayscale模式加载我们的输入视频
while True:
    ret, img = cap.read()
    #img = cv2.flip(img, -1)#旋转图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray= cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)#灰度图像转为彩色图像

    #调用分类器函数（比例因子、邻近数、人脸检测的最小尺寸）
    '''
    gray 表示输入 grayscale 图像
    scaleFactor 表示每个图像缩减的比例大小
    minNeighbors 表示每个备选矩形框具备的邻近数量。数字越大，假正类越少
    minSize 表示人脸识别的最小矩形大小
    '''
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(30, 30)
    )

    #函数将检测到的人脸的位置返回为一个矩形，左上角 (x,y)，w 表示宽度，h 表示高度 ==> (x,y,w,h)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        count += 1
        print("这是一条测试数据"+str(count))
        #cv2.imwrite("./dataset/faceimage.jpg", gray[y:y+h,x:x+w])#写入黑白
        cv2.imwrite("./dataset/faceimage.jpg", img[y:y+h,x:x+w])#写入彩色

    cv2.imshow('video',img)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()
