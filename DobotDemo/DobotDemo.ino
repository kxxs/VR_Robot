#include "stdio.h"
#include "Protocol.h"
#include "command.h"
#include "FlexiTimer2.h"
#include <Servo.h>

//Set Serial TX&RX Buffer Size
#define SERIAL_TX_BUFFER_SIZE 128
#define SERIAL_RX_BUFFER_SIZE 256

Servo myservo1; //lower servo pin 10
Servo myservo2; //upper servo pin 11
String str = "";
int value;
int zerox = 0;
int zeroy = 0;
int zeroz = 0;
int trigger, home_button;
int pos1 = 0;
int pos2 = 0;
int hmd_x = 0;
int hmd_y = 0;
int hmd_z = 0;
int hand_x = 0;
int hand_y = 0;
int hand_z = 0;
int hand_qx = 0;
int hand_qy = 0;
int hand_qz = 0;
int hmd_qx = 0;
int hmd_qy = 0;
int hmd_qz = 0;
int i;

long int goalx,  goalz = 0;
long int goaly = 0;
int r = 0;

char target1[] = "mx";
char target2[] = "mz";
char target3[] = "my";
char target4[] = "ax";
char target5[] = "az";
char target6[] = "ay";
char target7[] = "mqz";//便于确定相应数值，不发生错位现象
char target8[] = "mqy";
char target9[] =  "aqz";
char target10[] =  "aqx";
char target11[] =  "trig";
char target12[] =  "menu";


//#define JOG_STICK
/*********************************************************************************************************
** Global parameters
*********************************************************************************************************/
EndEffectorParams gEndEffectorParams;

JOGJointParams  gJOGJointParams;
JOGCoordinateParams gJOGCoordinateParams;
JOGCommonParams gJOGCommonParams;
JOGCmd          gJOGCmd;

PTPCoordinateParams gPTPCoordinateParams;
PTPCommonParams gPTPCommonParams;
PTPCmd          gPTPCmd;

uint64_t gQueuedCmdIndex;

/*********************************************************************************************************
** Function name:       setup
** Descriptions:        Initializes Serial
** Input parameters:    none
** Output parameters:   none
** Returned value:      none
*********************************************************************************************************/
void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial2.begin(115200);
  myservo1.attach(10); //upper servo
  myservo2.attach(11); // lower servo
  printf_begin();
  //Set Timer Interrupt
  FlexiTimer2::set(100, Serialread);
  FlexiTimer2::start();

  InitRAM();

  ProtocolInit();

  SetJOGJointParams(&gJOGJointParams, true, &gQueuedCmdIndex);

  SetJOGCoordinateParams(&gJOGCoordinateParams, true, &gQueuedCmdIndex);

  SetJOGCommonParams(&gJOGCommonParams, true, &gQueuedCmdIndex);

  printf("\r\n======Enter demo application======\r\n");

  SetPTPCmd(&gPTPCmd, false, &gQueuedCmdIndex);
}

/*********************************************************************************************************
** Function name:       Serialread
** Descriptions:        import data to rxbuffer
** Input parametersnone:
** Output parameters:
** Returned value:
*********************************************************************************************************/
void Serialread()
{
  while (Serial1.available()) {
    uint8_t data = Serial1.read();
    if (RingBufferIsFull(&gSerialProtocolHandler.rxRawByteQueue) == false) {
      RingBufferEnqueue(&gSerialProtocolHandler.rxRawByteQueue, &data);
    }
  }
}
/*********************************************************************************************************
** Function name:       Serial_putc
** Descriptions:        Remap Serial to Printf
** Input parametersnone:
** Output parameters:
** Returned value:
*********************************************************************************************************/
int Serial_putc( char c, struct __file * )
{
  Serial.write( c );
  return c;
}

/*********************************************************************************************************
** Function name:       printf_begin
** Descriptions:        Initializes Printf
** Input parameters:
** Output parameters:
** Returned value:
*********************************************************************************************************/
void printf_begin(void)
{
  fdevopen( &Serial_putc, 0 );
}

/*********************************************************************************************************
** Function name:       InitRAM
** Descriptions:        Initializes a global variable
** Input parameters:    none
** Output parameters:   none
** Returned value:      none
*********************************************************************************************************/
void InitRAM(void)
{
  //Set JOG Model
  gJOGJointParams.velocity[0] = 100;
  gJOGJointParams.velocity[1] = 100;
  gJOGJointParams.velocity[2] = 100;
  gJOGJointParams.velocity[3] = 100;
  gJOGJointParams.acceleration[0] = 80;
  gJOGJointParams.acceleration[1] = 80;
  gJOGJointParams.acceleration[2] = 80;
  gJOGJointParams.acceleration[3] = 80;

  gJOGCoordinateParams.velocity[0] = 100;
  gJOGCoordinateParams.velocity[1] = 100;
  gJOGCoordinateParams.velocity[2] = 100;
  gJOGCoordinateParams.velocity[3] = 100;
  gJOGCoordinateParams.acceleration[0] = 80;
  gJOGCoordinateParams.acceleration[1] = 80;
  gJOGCoordinateParams.acceleration[2] = 80;
  gJOGCoordinateParams.acceleration[3] = 80;

  gJOGCommonParams.velocityRatio = 50;
  gJOGCommonParams.accelerationRatio = 50;

  gJOGCmd.cmd = AP_DOWN;
  gJOGCmd.isJoint = JOINT_MODEL;



  //Set PTP Model
  gPTPCoordinateParams.xyzVelocity = 100;
  gPTPCoordinateParams.rVelocity = 100;
  gPTPCoordinateParams.xyzAcceleration = 80;
  gPTPCoordinateParams.rAcceleration = 80;

  gPTPCommonParams.velocityRatio = 50;
  gPTPCommonParams.accelerationRatio = 50;

  gPTPCmd.ptpMode = MOVL_XYZ;
  gPTPCmd.x = 200;
  gPTPCmd.y = 0;
  gPTPCmd.z = 0;
  gPTPCmd.r = 0;

  gQueuedCmdIndex = 0;


}

/*********************************************************************************************************
** Function name:       loop
** Descriptions:        Program entry
** Input parameters:    none
** Output parameters:   none
** Returned value:      none
*********************************************************************************************************/

void loop()
{
  //  for (; ;)
  //  {
  //    while (Serial2.available())
  //    {
  //      str += char(Serial2.read());
  //      Serial.print(str);
  //      str = "";
  //    }
  //  }

  Serial2.find(target8);
  pos2 = 90 - Serial2.parseInt();
  //Serial.println(pos2_b4);
  Serial2.find(target7);
  pos1 = 90 + Serial2.parseInt();
  Serial2.find(target4);
  hand_x = 0 - Serial2.parseInt();
  Serial2.find(target5);
  hand_y = Serial2.parseInt();
  Serial2.find(target6);
  hand_z = Serial2.parseInt();
  Serial2.find(target11);
  trigger = Serial2.parseInt();
  Serial2.find(target12);
  home_button = Serial2.parseInt();

  Serial.print(pos1);
  Serial.print(pos2);
  myservo1.write(pos1);
  myservo2.write(pos2);

  if (home_button == 1 or trigger == 1 ) {
    zerox = hand_x;
    zeroy = hand_y;
    zeroz = hand_z;
  }

//  Serial.print("hmd_x = ");
//  Serial.print(hmd_x);
//  Serial.print(" hmd_y = ");
//  Serial.print(hmd_y);
//  Serial.print(" hmd_z = ");
//  Serial.print(hmd_z);
//  Serial.print("\n");
//
//
//  Serial.print("hand_x = ");
//  Serial.print(hand_x);
//  Serial.print(" hand_y = ");
//  Serial.print(hand_y);
//  Serial.print(" hand_z = ");
//  Serial.print(hand_z);
//  Serial.print("\n");
//  dx = (hand_x - zerox) / 2;
//  dy = (hand_y - zeroy) / 2;
//  dz = (hand_z - zeroz) / 2;
//  Serial.print("dx = ");
//  Serial.print(dx);
//  Serial.print("dy = ");
//  Serial.print(dy);
//  Serial.print("dz = ");
//  Serial.print(dz);
//  Serial.print(",last_dx=");
//  Serial.print(last_dx);
//  Serial.print(",last_dy=");
//  Serial.print(last_dy);
//  Serial.print(",last_dz=");
//  Serial.print(last_dz);
//  Serial.print("\n\n");

  value = 0;
  static uint32_t timer = millis();
  static uint32_t count = 0;

  static uint32_t timer_move = millis();
  int tempofcount;

  if (millis() - timer > 500) //以下为主要修改区域
  {
    timer = millis();    
    goalx = hand_x - zerox;//南北方向，以南为正
    goaly = hand_y - zeroy ;//东西方向，以西为正
    goalz = hand_z - zeroz; //采用相对坐标的形式进行控制，手部相对于头部的坐标。垂直方向减少500毫米
    r = sqrt(goalx * goalx + goaly * goaly);
    Serial.write("*goalx=");
    Serial.print(goalx);
    Serial.write(",goaly=");
    Serial.print(goaly);
    Serial.write(",goalz=");
    Serial.print(goalz);
    Serial.write("\n");

    Serial.write(",r =");
    Serial.print(r);
    Serial.write("\n");

    if (r > 10)
    {
      if ( r < 20)//防止目标点越界
      {
        goalx = goalx / r * 20;
        goaly = goaly / r * 20;
      }
      else if ( r > 29)//防止目标点越界
      {
        goalx = goalx / r * 29;
        goaly = goaly / r * 29;
      }
      if (goalz > 20)//防止目标点越界
      {
        goalz = 20;
      }
      else if (goalz < -5)//防止目标点越界
      {
        goalz = -5;
      }
      gPTPCmd.x = goalx * 10;
      gPTPCmd.y = goaly * 10; //设置目标点
      gPTPCmd.z = goalz * 10;
      Serial.write("goalx=");
      Serial.print(goalx);
      Serial.write(",goaly=");
      Serial.print(goaly);
      Serial.write(",goalz=");
      Serial.print(goalz);
      Serial.write("\n");
    }

    Serial.write("X=");
    Serial.print(gPTPCmd.x);
    Serial.write(",Y=");
    Serial.print(gPTPCmd.y);
    Serial.write(",Z=");
    Serial.print(gPTPCmd.z);
    Serial.write("\n");

    SetPTPCmd(&gPTPCmd, false, &gQueuedCmdIndex);//以上为主要修改区域
    ProtocolProcess();
    //delay(200);
    Serial.write("***********\n");
  }

}

