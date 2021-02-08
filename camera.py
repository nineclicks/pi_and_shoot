from touch import touch
from preview import Preview
from buttons import press_menu_button, press_shutter_button
from menu import Menu
import subprocess
from review import get_images, Review

import picamera
from time import time

menu_open = False
review_open = False
menu = Menu()

@touch
def screen_touch(x, y):
    if menu_open:
        menu.press(x, y)

    elif review_open:
        review.press(x, y)

@press_menu_button
def menu_button():
    global menu_open, review_open
    if review_open:
        review_open = False
        menu_open = False
    else:
        menu_open = not menu_open

    if menu_open:
        preview.stop()
        menu.render_menu()

    else:
        preview.start()

@press_shutter_button
def shutter_button():
    if menu_open or review_open:
        menu_button()

    else:
        preview.snap('out/{}.jpg'.format(str(int(time()*1000))))

def shut_down():
    print('shutting down')
    subprocess.run(['sudo', 'shutdown', 'now'])

def start_review():
    global menu_open, review_open, review
    menu_open = False
    review_open = True
    review = Review()

review = None


menu.items = [
        (lambda: 'Review\n({})'.format(len(get_images())), start_review),
        (lambda: 'Shutdown', shut_down),
        ]

preview = Preview((480*6, 320*6), 2)
preview.start()
