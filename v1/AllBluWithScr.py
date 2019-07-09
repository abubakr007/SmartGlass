import os
import sys
import time
from PIL import ImageFont
from luma.core.render import canvas
from demo_opts import get_device
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT
from luma.core.virtual import viewport

import glob
import time
from bluetooth import *

def scroll_message(font=None, speed=1,msg='Hello World'):
    device = get_device()
    x = device.width

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

	
def main():
	
	server_sock=BluetoothSocket( RFCOMM )
	server_sock.bind(("",PORT_ANY))
	server_sock.listen(1)
	
	port = server_sock.getsockname()[1]
	
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	advertise_service( server_sock, "AquaPiServer",
		service_id = uuid,service_classes = [ uuid, SERIAL_PORT_CLASS ],
		profiles = [ SERIAL_PORT_PROFILE ], 
		#protocols = [ OBEX_UUID ] 
		)
	font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Volter__28Goldfish_29.ttf'))
	font = ImageFont.truetype(font_path,35)
	#draw.text((0, 0), "Hello World", font=font, fill=255)
	while True:
		print ("Waiting for connection on RFCOMM channel %d" % port)

		client_sock, client_info = server_sock.accept()
		print ("Accepted connection from ", client_info)

		try:
			data = client_sock.recv(1024)
			if len(data) == 0: break
			print(type('string'))
			print(type(data))
			print(data[2:-2])
			print ("received [%s]" % data)
			scroll_message(font,6,data.decode("utf-8"))
			time.sleep(1)
			"""if data == 'temp':
				data = str(read_temp())+'!'
			elif data == 'lightOn':
				GPIO.output(17,False)
				data = 'light on!'
			elif data == 'lightOff':
				GPIO.output(17,True)
				data = 'light off!'
			else:
				data = 'WTF!' 
				client_sock.send(data)
			print "sending [%s]" % data
			"""
			data = "done"
			client_sock.send(data)
			print ("sending [%s]" % data)

		except IOError:
			pass

		except KeyboardInterrupt:

			print ("disconnected")

			client_sock.close()
			server_sock.close()
			print ("all done")

			break

	

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
		


