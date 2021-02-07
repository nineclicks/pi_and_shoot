from touch import touch
from preview import Preview
from buttons import press_menu_button, press_shutter_button

import picamera
from time import time

menu_open = False

@touch
def screen_touch(x, y):
    pass

@press_menu_button
def menu_button():
    global menu_open
    menu_open = not menu_open

    if menu_open:
        preview.stop()

    else:
        preview.start()

@press_shutter_button
def shutter_button():
    preview.snap('out/{}.jpg'.format(str(int(time()*1000))))

preview = Preview((480*6, 320*6), 2)
preview.start()
