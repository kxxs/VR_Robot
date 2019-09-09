#!/usr/bin/python
#-*-coding:utf-8 -*-
import socket
import cv2
import numpy
import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl
import numpy as np
#import matplotlib.pyplot as plt
import re
import sys
import pdb

camera_settings = sl.PyCAMERA_SETTINGS.PyCAMERA_SETTINGS_BRIGHTNESS
str_camera_settings = "BRIGHTNESS"
step_camera_settings = 1

# socket.AF_INET用于服务器与服务器之间的网络通信
# socket.SOCK_STREAM代表基于TCP的流式socket通信
#sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 连接服务端
#address_server = ('10.2.12.138', 8010)
#sock.connect(address_server)

init = zcam.PyInitParameters()
cam = zcam.PyZEDCamera()
if not cam.is_opened():
    print("Opening ZED Camera...")
status = cam.open(init)
if status != tp.PyERROR_CODE.PySUCCESS:
    print(repr(status))
    exit()
left = core.PyMat()
right = core.PyMat() 

while True: 
    runtime = zcam.PyRuntimeParameters()
    err = cam.grab(runtime)
    if err == tp.PyERROR_CODE.PySUCCESS:
        cam.retrieve_image(left, sl.PyVIEW.PyVIEW_LEFT)
        cam.retrieve_image(right, sl.PyVIEW.PyVIEW_RIGHT)
    left_img = left.get_data()
    right_img = right.get_data()
    left_img = cv2.resize(left_img,(1080,720))
    right_img = cv2.resize(right_img,(1080,720))

    cv2.imshow("left", left_img)
    cv2.imshow("right", right_img)
    key = cv2.waitKey(1)
    '''
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90] #设置编码参数
    # 首先对图片进行编码，因为socket不支持直接发送图片
    result1, imgencode1 = cv2.imencode('.jpg', left_img)
    result2, imgencode2 = cv2.imencode('.jpg', right_img)
    array_left = numpy.array(imgencode1)
    array_right = numpy.array(imgencode2)
    stringData1 = array_left.tostring()
    stringData2 = array_right.tostring()
    # 首先发送图片编码后的长度
    sock.send(str(len(stringData1)).ljust(16))
    sock.send('left'.ljust(16))
    for i in range (0,len(stringData1)):
        sock.send(stringData1[i])
    sock.send(str(len(stringData2)).ljust(16))
    sock.send('right'.ljust(16))
    for i in range (0,len(stringData2)):
        sock.send(stringData2[i])
    '''



#sock.close()
cv2.destroyAllWindows()
