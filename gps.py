import serial,time,pynmea2

port = '/dev/serial0'
baud = 9600
serialPort = serial.Serial(port, baudrate = baud, timeout = 0.5)

while True:
    str = ''
    try:
        str = serialPort.readline().decode().strip()
    except Exception as e:
        print(e)
    #print(str)
        
    if str.find('GGA') > 0:
        msg = None
        try:
            msg = pynmea2.parse(str)
            strMsg = "Timestamp: %s,Lat: %s Lon: %s,Altitude: %s %s,Satellites: %s" % (msg.timestamp,round(msg.latitude,6),round(msg.longitude,6),msg.altitude,msg.altitude_units,msg.num_sats)
            print(strMsg)             
        except Exception as e:
            print(e)
    time.sleep(0.01)
