import os
import sys
import time
from PIL import ImageFont
from luma.core.render import canvas
from demo_opts import get_device
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT
from luma.core.virtual import viewport

from apds9960.const import *
from apds9960 import APDS9960
import RPi.GPIO as GPIO
import smbus

import threading
import datetime

device = None

lasttimeupdate = None
timeout = 5
checkdisplay = False

dirs = {
    APDS9960_DIR_NONE: "none",
    APDS9960_DIR_LEFT: "left",
    APDS9960_DIR_RIGHT: "right",
    APDS9960_DIR_UP: "up",
    APDS9960_DIR_DOWN: "down",
    APDS9960_DIR_NEAR: "near",
    APDS9960_DIR_FAR: "far",
}

def displaytimeout():
    global checkdisplay
    while(True):
        if  ( (  checkdisplay == True) and (((datetime.datetime.now() - lasttimeupdate).total_seconds()) > timeout)):
            print("Main    : Display off")
            DisplayOff()
            checkdisplay = False
		  
def intH(channel):
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Volter__28Goldfish_29.ttf'))
    font = ImageFont.truetype(font_path,35)
    #draw.text((0, 0), "Hello World", font=font, fill=255)
    dispay_message(font,6,'*')
	
def updateDisplay():
  global checkdisplay
  global lasttimeupdate
  lasttimeupdate = datetime.datetime.now()
  checkdisplay = True

def DisplayOff():
    global device
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Volter__28Goldfish_29.ttf'))
    font = ImageFont.truetype(font_path,35)
    #draw.text((0, 0), "Hello World", font=font, fill=255)
    #dispay_message(font,6,'')
    device.hide()

def scroll_message(font=None, speed=1,msg='Hello World'):
    global device
    x = device.width
    device.show()
    # First measure the text size
    with canvas(device) as draw:
        w, h = draw.textsize(msg, font)

    virtual = viewport(device, width=max(device.width, w + x + x), height=max(h, device.height))
    with canvas(virtual) as draw:
        draw.text((x, 20), msg, font=font, fill="white")

    i = 0
    while i < x + w:
        virtual.set_position((i, 0))
        i += speed
        time.sleep(0.025)
        updateDisplay()

def dispay_message(font=None, speed=1,msg='Hello World'):
    global device
    device.show()
    with canvas(device) as draw:
        draw.text((0, 20), msg, font=font, fill="white")
        updateDisplay()

	
def main():
	global device
	device = get_device()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.IN)
	
	port = 1
	bus = smbus.SMBus(port)

	apds = APDS9960(bus)	
	GPIO.add_event_detect(7, GPIO.FALLING, callback = intH)
	apds.setProximityIntLowThreshold(50)
	apds.enableGestureSensor()
	#with canvas(device) as draw:
	font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Volter__28Goldfish_29.ttf'))
	font = ImageFont.truetype(font_path,35)
	#draw.text((0, 0), "Hello World", font=font, fill=255)
	dispay_message(font,6,'Start')
	t = threading.Thread(target=displaytimeout)
	t.start()
	while True:
		time.sleep(0.5)
		if apds.isGestureAvailable():
			motion = apds.readGesture()
			diris = dirs.get(motion, "unknown")
			dispay_message(font,6,diris)
            
	time.sleep(1)
	
	#msg = "Hi how are you, this should be long text"
	#show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT))
	#time.sleep(1)

	

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
		



