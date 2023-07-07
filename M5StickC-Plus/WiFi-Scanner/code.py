import board
import busio
import wifi
import storage
import time
import binascii
from adafruit_datetime import datetime

uart = busio.UART(board.D26, board.D36, baudrate=9600, timeout=30)
wifi.radio.stop_scanning_networks()
lat="01"
lon="02"
alt="202.300"
accuracy="0"

print("Waiting for GPS fix...", end="")
while True:
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
            print(lat,lon)
            with open("/log.csv", "a") as log:
                for network in wifi.radio.start_scanning_networks():
                    chan  = network.channel
                    ssid  = network.ssid
                    bssid = binascii.hexlify(network.bssid,":").decode()
                    if network.authmode == [wifi.AuthMode.WPA, wifi.AuthMode.PSK]:
                        auth = "[WPA-PSK-CCMP+TKIP][ESS]"
                    elif network.authmode == [wifi.AuthMode.WPA2, wifi.AuthMode.PSK]:
                        auth = "[WPA2-PSK-CCMP+TKIP][ESS]"
                    elif network.authmode == [wifi.AuthMode.OPEN]:
                        auth = "[ESS]"
                    else:
                        auth = network.authmode
                    rssi  = network.rssi
                    iso_date_string = "2020-04-05T05:04:45.752301"
                    isodate = datetime.fromisoformat(iso_date_string)
                    logentry = f"{bssid},{ssid},{auth},{isodate},{rssi},{lat},{lon},{alt},{accuracy},WIFI"
                    print(logentry)
                    log.write(logentry)
                    log.flush
                wifi.radio.stop_scanning_networks()
            
        else:
            # Print a . to indicate that we're getting GPS data,
            # but there's not a location fix yet. Hacky. Works.
            print(".", end="")

