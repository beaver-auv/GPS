import serial
import time
import pynmea2

gps1_port = '/dev/ttyAMA0'
gps2_port = '/dev/ttyAMA1'
baud = 9600

gps1 = serial.Serial(gps1_port, baudrate=baud, timeout=0.5)
gps2 = serial.Serial(gps2_port, baudrate=baud, timeout=0.5)

def handle_line(line, label):
    if not line.startswith('$') or 'GGA' not in line:
        return

    try:
        msg = pynmea2.parse(line)
        print(
            f"{label} | "
            f"Timestamp: {msg.timestamp}, "
            f"Lat: {msg.latitude:.6f}, "
            f"Lon: {msg.longitude:.6f}, "
            f"Altitude: {msg.altitude} {msg.altitude_units}, "
            f"Satellites: {msg.num_sats}"
        )
    except pynmea2.ParseError:
        pass
    except AttributeError:
        pass  # sentence parsed but missing GGA fields

while True:
    try:
        line1 = gps1.readline().decode(errors='ignore').strip()
        line2 = gps2.readline().decode(errors='ignore').strip()

        handle_line(line1, "GPS1")
        handle_line(line2, "GPS2")

    except Exception as e:
        print(e)

    time.sleep(0.01)
