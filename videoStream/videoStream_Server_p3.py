#!/usr/bin/python
#-*-coding:utf-8 -*-
import socket
import cv2
import numpy
import time

def recv_size(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# 接收图片
def recv_all(sock, count):
    buf = b''
    while count:
        # 这里每次只接收一个字节的原因是增强python与C++的兼容性
        # python可以发送任意的字符串，包括乱码，但C++发送的字符中不能包含'\0'，也就是字符串结束标志位
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# socket.AF_INET用于服务器与服务器之间的网络通信
# socket.SOCK_STREAM代表基于TCP的流式socket通信
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置地址与端口，如果是接收任意ip对本服务器的连接，地址栏可空，但端口必须设置
address = ('10.2.12.66', 8010)
s.bind(address) # 将Socket（套接字）绑定到地址
s.listen(1) # 开始监听TCP传入连接
print ('Waiting for images...')
# 接受TCP链接并返回（conn, addr），其中conn是新的套接字对象，可以用来接收和发送数据，addr是链接客户端的地址。
conn, addr = s.accept()
while 1:
    length1 = recv_size(conn,16).decode() #首先接收来自客户端发送的大小信息
    if isinstance (length1,str): #若成功接收到大小信息，进一步再接收整张图片
        side1 = recv_size(conn,16).decode() #首先接收来自客户端发送的大小信息
        stringData1 = recv_all(conn, int(length1))
        length2 = recv_size(conn,16).decode()
        side2 = recv_size(conn,16).decode()
        stringData2 = recv_all(conn, int(length2))

        data1 = numpy.fromstring(stringData1, dtype='uint8')
        data2 = numpy.fromstring(stringData2, dtype='uint8')

        decimg1=cv2.imdecode(data1,1) 
        decimg2=cv2.imdecode(data2,1) #解码处理，返回mat图片
        decimg1=cv2.resize(decimg1,(800,600))
        decimg2=cv2.resize(decimg2,(800,600))

        cv2.imshow(side1,decimg1)
        #cv2.waitKey(15)
        cv2.imshow(side2,decimg2)
        cv2.waitKey(1)
    #if cv2.waitKey(10) == 27:
    #    break 

s.close()
cv2.destroyAllWindows()
