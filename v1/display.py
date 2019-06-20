import os
import sys
import time
from PIL import ImageFont
from luma.core.render import canvas
from demo_opts import get_device
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT
from luma.core.virtual import viewport


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
	
	#with canvas(device) as draw:
	font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Volter__28Goldfish_29.ttf'))
	font = ImageFont.truetype(font_path,35)
	#draw.text((0, 0), "Hello World", font=font, fill=255)
	scroll_message(font,6,'Hassan , How are you ')
	time.sleep(1)
	
	#msg = "Hi how are you, this should be long text"
	#show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT))
	#time.sleep(1)

	

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
		


