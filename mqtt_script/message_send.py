import triad_openvr
import time
import sys
import paho.mqtt.client as mqtt
import threading
v = triad_openvr.triad_openvr()
v.print_discovered_objects()

HOST = "10.2.9.223"
PORT = 1883
count = 1
hmds = ["hmd_x:","hmd_y:","hmd_z:","hmd_qx:","hmd_qy:","hmd_qz:"]
hands = ["hand_x:","hand_y:","hand_z:","hand_qx:","hand_qy:","hand_qz:"]


def on_connect(client,userdata,flags,rc):
    print("Connected with result code"+str(rc))
    
# publish 消息
def on_publish(client,topic, payload, qos):
    client.publish(topic, payload, qos)

def on_message(clietn, userdata, msg):
    print("Success!")

def loop(self, timeout=None):
    thread = threading.Thread(target=self._loop, args=(timeout,))
    # thread.setDaemon(True)
    thread.start()

def _loop(self, timeout=None):
    if not timeout:
        self.client.loop_forever()
    else:
        self.client.loop(timeout)

def publish_loop(self):
    pass       

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, PORT, 60)
client.loop()

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[0])
else:
    print("Invalid number of arguments")
    interval = False
    
if interval:
    while(True):
        start = time.time()
        txt = ""
        txt2 = ""
        txt3 = ""
        txt4 = ""
        i = 0
        j = 0
        for each in v.devices["hmd_1"].get_pose_euler():
            txt += hmds[i]
            if i<3:
                txt += "%d" % (each*100)
            else:
                txt += "%d" % each
            txt += ","
            if i==4 or i==5:
                txt3 += hmds[i]
                txt3 += "%d" % each
                txt3 += ","
            i += 1

        for each in v.devices["controller_1"].get_pose_euler():
            txt2 += hands[j]
            if j<3:
                txt2 += "%d" % (each*100)
            else:
                txt2 += "%d" % each
            txt2 += ","
            j += 1
        if(count == 10):
            client.connect(HOST, PORT, 60)
            count = 1
        txt4 = "\n" + txt + "\n" + txt2
        print("\n" + txt4, end="")
        on_publish(client,"hmd",txt4,1)
        count = count +1
        '''
        sleep_time = 0.01 #interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)
        '''
