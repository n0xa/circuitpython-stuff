import board
import busio
import wifi
import storage
import time
import binascii
from adafruit_datetime import datetime
from digitalio import DigitalInOut, Direction, Pull
import rtc
import socketpool
import adafruit_ntp
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=0)
print ("Setting system time")
rtc.RTC().datetime = ntp.datetime
logfile = str(datetime.isoformat(datetime.now())).replace(":","-")+"-wifi.csv"
print("LogFile:\n "+logfile)
writeheader = True
# setup
# Button A (M5 button on the front panel)
# Press and hold to pause scanning
btna = DigitalInOut(board.BTN_A)
btna.direction = Direction.INPUT
btna.pull = Pull.UP
# Button B (right side panel by the display)
# Press to enable/disable GPS and logging
btnb = DigitalInOut(board.BTN_B)
btnb.direction = Direction.INPUT
btnb.pull = Pull.UP

uart = busio.UART(board.D26, board.D36, baudrate=9600, timeout=30)
wifi.radio.stop_scanning_networks()

pause = False
logging = False

# defining these here for scope
lat = "00.00"
lon = "00.00"
alt = "00.00"

print("Scanning...")
while True:
    if not btna.value:
        if pause:
            pause = False
            print ("\nUnpaused\n") 
        else:
            pause = True
            print("\nPaused\n")
        time.sleep(5)
    if not btnb.value:
        if logging:
            logging = False
            print("\nLogging: Off\n")
        else:
            logging = True
            print("\nLogging: On\n")
        time.sleep(5)
    if pause:
        time.sleep(1)
        continue
    if logging:
        gpsfix = False
        print("-=- Logging: On -=-")
        while not gpsfix:
            data = uart.readline()
            data_string = ''.join([chr(b) for b in data])
            # We're going to manually parse GPGGA sentences.
            if data_string.startswith("GPGGA,",1):
                gps = data_string.split(",")
                # gps[4] should have latitude data if there's a fix
                if len(gps[4]) > 4:
                    # The format for NMEA coordinates is (d)ddmm.mmmm
                    # We'll shift the period over 2 spots with string
                    # slices. esp32 doesn't handle float numbers well.
                    tlat = gps[2]+gps[3]
                    lat = tlat[0:2]+"."+tlat[2:4]+tlat[5:]
                    tlon = gps[4]+gps[5]
                    lon = tlon[0:3]+"."+tlon[3:5]+tlon[6:]
                    alt = gps[9]
                    sats = gps[7] 
                    print("-=- GPS: "+sats+" sats -=-")
                    print("Lat: "+lat)
                    print("Lon: "+lon)
                    print("Alt: "+alt)
                    print("-=-=-=-=-=-")
                    gpsfix = True
                else:
                    print("-=- GPS: No Fix -=-")
                
    for network in wifi.radio.start_scanning_networks():
        chan  = network.channel
        ssid  = network.ssid
        bssid = binascii.hexlify(network.bssid,":").decode()
        if network.authmode == [wifi.AuthMode.WPA, wifi.AuthMode.PSK]:
            auth = "[WPA-PSK-CCMP+TKIP][ESS]"
        elif network.authmode == [wifi.AuthMode.WPA2, wifi.AuthMode.PSK]:
            auth = "[WPA2-PSK-CCMP+TKIP][ESS]"
        elif network.authmode == [wifi.AuthMode.WPA, wifi.AuthMode.WPA2, wifi.AuthMode.PSK]:
            auth = "[WPA-PSK-CCMP+TKIP] [WPA2-PSK-CCMP+TKIP][ESS]"
        elif network.authmode == [wifi.AuthMode.WPA2, wifi.AuthMode.ENTERPRISE]:
            auth = "[WPA2-UNKNOWN-CCMP][ESS]"
        elif network.authmode == [wifi.AuthMode.WPA2, wifi.AuthMode.WPA3, wifi.AuthMode.PSK]:
            auth = "[WPA3-UNKNOWN-CCMP][ESS]"
        elif network.authmode == [wifi.AuthMode.OPEN]:
            auth = "[ESS]"
        else:
            auth = network.authmode
        rssi  = network.rssi
        isodate = datetime.now()
        if logging:
            with open(logfile, "a") as log:
                if writeheader:
                    # This is pretty much the kismetdb-to-wiglecsv header and format.
                    log.write("WigleWifi-1.4,appRelease=M5StickCPlus,model=ESP32,release=2023.07.08.8,device=M5StickCPlus,display=M5StickCPlus,board=M5StickCPlus,brand=M5StickCPlus")
                    log.write("MAC,SSID,AuthMode,FirstSeen,Channel,RSSI,CurrentLatitude,CurrentLongitude,AltitudeMeters,AccuracyMeters,Type")
                    writeheader = False
                logentry = f"{bssid},{ssid},{auth},{isodate},{chan},{rssi},{lat},{lon},{alt},0,WIFI\n"
                print(ssid)
                log.write(logentry)
                log.flush
        else:
            print(ssid)
    wifi.radio.stop_scanning_networks()
    if not logging:
        print("-=- Logging: Off -=-")
        time.sleep(1)