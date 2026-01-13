import serial,time,pynmea2

gps1_port = '/dev/serial0'
gps2_port = '/dev/serial1'

baud = 9600
gps1_serialPort = serial.Serial(gps1_port, baudrate = baud, timeout = 0.5)
gps2_serialPort = serial.Serial(gps2_port, baudrate = baud, timeout = 0.5)

while True:
    str = ''
    try:
        gps1_str = gps1_serialPort.readline().decode().strip()
        gps2_str = gps2_serialPort.readline().decode().strip() #serial port data
    except Exception as e:
        print(e)

    if 'GGA' in gps1_str or 'GGA' in gps2_str:  #whychange
        gps1_msg = None
        gps2_msg = None
        try:
            gps1_msg = pynmea2.parse(gps1_str)
            gps2_msg = pynmea2.parse(gps2_str)
            gps1_strMsg = "Timestamp: %s,Lat: %s Lon: %s,Altitude: %s %s,Satellites: %s" % (gps1_msg.timestamp,round(gps1_msg.latitude,6),round(gps1_msg.longitude,6),gps1_msg.altitude,gps1_msg.altitude_units,gps1_msg.num_sats)
            gps2_strMsg = "Timestamp: %s,Lat: %s Lon: %s,Altitude: %s %s,Satellites: %s" % (gps2_msg.timestamp,round(gps2_msg.latitude,6),round(gps2_msg.longitude,6),gps2_msg.altitude,gps2_msg.altitude_units,gps2_msg.num_sats)
            print(gps1_strMsg)  
            print(gps2_strMsg)
        except Exception as e:
            print(e)
    time.sleep(0.01)
    


