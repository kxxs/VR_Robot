import RPi.GPIO as GPIO  
import time  
import signal  
import atexit  
import math
atexit.register(GPIO.cleanup)    
    
servopinA = 20
servopinB = 26
servopinC = 19
servopinD = 6
servopinE = 5
servopinF = 12


GPIO.setmode(GPIO.BCM)  
GPIO.setup(servopinA, GPIO.OUT, initial=False)
GPIO.setup(servopinB, GPIO.OUT, initial=False)
GPIO.setup(servopinC, GPIO.OUT, initial=False)
GPIO.setup(servopinD, GPIO.OUT, initial=False)
GPIO.setup(servopinE, GPIO.OUT, initial=False)
GPIO.setup(servopinF, GPIO.OUT, initial=False)
p1 = GPIO.PWM(servopinA,50) #50HZ  
p2 = GPIO.PWM(servopinB,50)
p3 = GPIO.PWM(servopinC,50)
p4 = GPIO.PWM(servopinD,50)
p5 = GPIO.PWM(servopinE,50)
p6 = GPIO.PWM(servopinF,50)
p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)
p5.start(0)
p6.start(0)
time.sleep(2)  
'''
####################
while (True):
    for i in range(180,0,-10):
        p4.ChangeDutyCycle(2.5 + i/10)
    #p2.ChangeDutyCycle(2.5 + i/10)
    #p1.ChangeDutyCycle(2.5 + i/10)
        #p4.ChangeDutyCycle(2.5 + i/10)
        #p5.ChangeDutyCycle(2.5 + i/10)
        #p6.ChangeDutyCycle(2.5 + i/10)
        print(".")
        time.sleep(0.3)
    for i in range(0,180,10):
        p4.ChangeDutyCycle(2.5 + i/10)
    #p2.ChangeDutyCycle(2.5 + i/10)
    #p1.ChangeDutyCycle(2.5 + i/10)
        #p4.ChangeDutyCycle(2.5 + i/10)
        #p5.ChangeDutyCycle(2.5 + i/10)
        #p6.ChangeDutyCycle(2.5 + i/10)
        print(".")
        time.sleep(0.3)
 '''
######################
def ZhuaZhuaLe(d, e, f):
    #e:shake head
    #d:nod
    #f:open and close mouth
    if f == 1:
        print("close")
        p5.ChangeDutyCycle(2.5)
    else :
        print("open")
        p5.ChangeDutyCycle(7.5)
    print("")
    print("D = ",d)
    print("e = ",e)
    p4.ChangeDutyCycle(2.5 + d/10)
    p6.ChangeDutyCycle(2.5 + e / 10)
    
    time.sleep(0.5) 
    #p4.stop()
    #p5.stop()
    #p6.stop()
    
######################
# control code, waiting for test
# a, b, c, d, e
def move(a, b, c):
    l1 = 0.1
    l2 = 0.09
    x = math.sqrt(a * a + b * b)
    y = c
    print("(x * x + y * y - l1 * l1 - l2 * l2)/ (2 * l1 * l2) = ", (x * x + y * y - l1 * l1 - l2 * l2)/ (2 * l1 * l2))
    t = (-x * x - y * y + l1 * l1 + l2 * l2)/ (2 * l1 * l2)
    alpa = math.acos(-t)
    beta = math.acos((l1 * l1 - l2 * l2 +x * x + y * y)/ (2 * l1 * math.sqrt(x * x+ y * y))) + math.atan(y / x) 
    if a < 0.005 and a > -0.005:
        sigma = math.pi / 2
    else:
        sigma = math.atan (b / a)
    #print("sigma =", sigma / math.pi * 180)
    if sigma < 0 :
        sigma = sigma + math.pi
    print("alpa =", alpa / math.pi * 180)
    print("beta =", beta / math.pi * 180)
    print("sigma =", sigma / math.pi * 180)
    alpa = alpa / math.pi * 10 + 2.5
    beta = beta / math.pi * 10 + 2.5
    sigma = sigma / math.pi * 10 + 2.5
    p2.ChangeDutyCycle(alpa)
    p1.ChangeDutyCycle(beta)
    p3.ChangeDutyCycle(sigma)
    time.sleep(0.5)  
def begin():
    p1.start(0)
    p2.start(0)
    p3.start(0)
    p4.start(0)
    p5.start(0)
    p6.start(0)
    
def stop():
    p1.stop()
    p2.stop()
    p3.stop()
    p4.stop()
    p5.stop()
    p6.stop()

while (True): 
    a = 0.0
    b = 0.03
    c = 0.15
    move (a,b,c)
    d = 50
    e = 110
    f = 1
    ZhuaZhuaLe(d, e, f)
    d = 40
    e = 100
    f = 1
    ZhuaZhuaLe(d, e, f)
    d = 30
    e = 90
    f = 1
    ZhuaZhuaLe(d, e, f)
    d = 20
    e = 80
    f = 1
    ZhuaZhuaLe(d, e, f)
    d = 10
    e = 70
    f = 1
    ZhuaZhuaLe(d, e, f)
    d = 5
    e = 60
    f = 1
    ZhuaZhuaLe(d, e, f)
    stop()
    #p4.ChangeDutyCycle(2.5)
######################

