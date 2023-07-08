import os
import board
import time
import terminalio
import displayio
import busio
from adafruit_display_text import label
import adafruit_st7789

print("==============================")
print(os.uname())
print(adafruit_st7789.__name__ + " version: " + adafruit_st7789.__version__)

# Release any resources currently in use for the displays
displayio.release_displays()

# reference pins.c for this device for pin names
tft_cs = board.LCD_CS
tft_dc = board.LCD_DC
tft_rst = board.LCD_RST
spi_mosi = board.LCD_MOSI
spi_clk = board.LCD_CLK

spi = busio.SPI(spi_clk, MOSI=spi_mosi)

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst
)

# rowstart/colstart from the circuitpython board.c for this device
display = adafruit_st7789.ST7789(display_bus, width=135, height=240, rowstart=40, colstart=53)
display.rotation = 270

# Initialize the display
splash = displayio.Group()
display.show(splash)

# Fill the screen with blue (we'll use it as the border)
color_bitmap = displayio.Bitmap(240, 135, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x0000FF
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Black background inside the border
inner_bitmap = displayio.Bitmap(236, 131, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=2, y=2)
splash.append(inner_sprite)

# Blocks of text
text_group1 = displayio.Group(scale=3, x=15, y=15)
text1 = "Stick C Plus"
text_area1 = label.Label(terminalio.FONT, text=text1, color=0x00FF00)
text_group1.append(text_area1)  # Subgroup for text scaling

text_group2 = displayio.Group(scale=2, x=28, y=50)
text2 = "Hack The Planet"
text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF)
text_group2.append(text_area2)  # Subgroup for text scaling

text_group3 = displayio.Group(scale=2, x=7, y=80)
text3 = "CircuitPython "+os.uname().release
text_area3 = label.Label(terminalio.FONT, text=text3, color=0x00FF00)
text_group3.append(text_area3)  # Subgroup for text scaling

text_group4 = displayio.Group(scale=1, x=7, y=120)
text4 = "h-i-r.net | IG: @4x0nn | GitHub: n0xa"
text_area4 = label.Label(terminalio.FONT, text=text4, color=0xFF00FF)
text_group4.append(text_area4)  # Subgroup for text scaling

# Draw them on the display
splash.append(text_group1)
splash.append(text_group2)
splash.append(text_group3)
splash.append(text_group4)

while True:
    # infinite loop keeps it from bailing out to the console
    pass
