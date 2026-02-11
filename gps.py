import serial
import time
import pynmea2

gps1_port = '/dev/ttyAMA0'
gps2_port = '/dev/ttyAMA1'
baud = 9600

gps1 = serial.Serial(gps1_port, baudrate=baud, timeout=0.5)
gps2 = serial.Serial(gps2_port, baudrate=baud, timeout=0.5)

# Dictionary to store the latest data from each GPS
latest = {"GPS1": None, "GPS2": None}
origin = None

def latlon_to_xy(lat, lon, lat0, lon0): #
    R = 6378137.0
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    lat0_rad = math.radians(lat0)
    lon0_rad = math.radians(lon0)

    dlat = lat_rad - lat0_rad
    dlon = lon_rad - lon0_rad

    x = dlon * math.cos(lat0_rad) * R
    y = dlat * R
    return x, y

def handle_line(line, label):
    if not line.startswith('$') or 'GGA' not in line:
        return

    try:
        msg = pynmea2.parse(line)

        latest[label] = {
            "lat": msg.latitude,
            "lon": msg.longitude,
            "alt": float(msg.altitude),
            "sats": int(msg.num_sats)
        }

# for debugging
        print( 
            label,
            "Lat:", msg.latitude,
            "Lon:", msg.longitude,
            "Alt:", msg.altitude,
            "Sats:", msg.num_sats
        ) 

    except (pynmea2.ParseError, AttributeError):
        pass  # sentence parsed but missing GGA fields

def print_average():
    global origin

    if not (latest["GPS1"] and latest["GPS2"]):
        return

    g1, g2 = latest["GPS1"], latest["GPS2"]

    avg_lat = (g1["lat"] + g2["lat"]) / 2
    avg_lon = (g1["lon"] + g2["lon"]) / 2
    avg_alt = (g1["alt"] + g2["alt"]) / 2

    # Set origin on first valid averaged fix
    if origin is None:
        origin = {"lat": avg_lat, "lon": avg_lon}
        print("ORIGIN SET | Lat:", origin["lat"], "Lon:", origin["lon"])

    # Convert to local XY
    x, y = latlon_to_xy(avg_lat, avg_lon, origin["lat"], origin["lon"])

    print(
        "AVERAGED |",
        "Lat:", avg_lat,
        "Lon:", avg_lon,
        "Alt:", avg_alt,
        "| X(East)m:", round(x, 2),
        "Y(North)m:", round(y, 2),
        "| Total Sats:", g1["sats"] + g2["sats"]
    )
    )

while True:
    line1 = gps1.readline().decode(errors='ignore').strip()
    line2 = gps2.readline().decode(errors='ignore').strip()

    handle_line(line1, "GPS1")
    handle_line(line2, "GPS2")

    print_average()
    time.sleep(0.01)
