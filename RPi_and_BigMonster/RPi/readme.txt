树莓派控制台
接收：
  用pysocket接收来自计算机的指令，然后加以处理调用c程序发送给大车，加以控制
  Recive_CMD类：
    字段：IP, PORT, data, addr, verify
    方法：init, Recive_Data, Recive_Point, Recive_PID, Recive_speed 
