import board
import busio
import digitalio
import time

uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=30)
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
            print(f"Sats: {sats} Alt: {alt} Lat: {lat} Lon: {lon}")
            gpsfix = True
        else:
            print(data_string, end="")
