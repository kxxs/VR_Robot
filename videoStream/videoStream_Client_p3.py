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
import time

camera_settings = sl.PyCAMERA_SETTINGS.PyCAMERA_SETTINGS_BRIGHTNESS
str_camera_settings = "BRIGHTNESS"
step_camera_settings = 1

# socket.AF_INET用于服务器与服务器之间的网络通信
# socket.SOCK_STREAM代表基于TCP的流式socket通信
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 连接服务端
address_server = ('10.2.12.66', 8010)
sock.connect(address_server)

def open_cam_usb(dev, width, height):
    # We want to set width and height here, otherwise we could just do:
    #     return cv2.VideoCapture(dev)
    gst_str = ("v4l2src device=/dev/video{} ! "
               "video/x-raw, width=(int){}, height=(int){}, format=(string)RGB ! "
               "videoconvert ! appsink").format(dev, width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

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

    #print(time())
    left_img = left.get_data()
    right_img = right.get_data()
    left_img = cv2.resize(left_img,(640,480))
    right_img = cv2.resize(right_img,(640,480))
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),80] #设置编码参数
    # 首先对图片进行编码，因为socket不支持直接发送图片
    result1, imgencode1 = cv2.imencode('.jpg', left_img)
    result2, imgencode2 = cv2.imencode('.jpg', right_img)
    array_left = numpy.array(imgencode1)
    array_right = numpy.array(imgencode2)
    stringData1 = array_left.tostring()
    stringData2 = array_right.tostring()
    # 首先发送图片编码后的长度
    sock.send(bytes(str(len(stringData1)).ljust(16),encoding="utf8"))
    sock.send(bytes('left'.ljust(16),encoding="utf8"))
    sock.send(stringData1)
    sock.send(bytes(str(len(stringData2)).ljust(16),encoding="utf8"))
    sock.send(bytes('right'.ljust(16),encoding="utf8"))
    sock.send(stringData2)



sock.close()
cv2.destroyAllWindows()
