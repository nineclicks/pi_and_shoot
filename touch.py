from evdev import InputDevice, categorize, ecodes
import json
import threading
dev = InputDevice('/dev/input/event0')

#print(dev)

lastx = 0
lasty = 0

width = 480
height = 320

minx = 9e9
miny = 9e9
maxx = -9e9
maxy = -9e9

touch_fn = lambda: None

def save_calibration():
    cal = {
            'minx': minx,
            'miny': miny,
            'maxx': maxx,
            'maxy': maxy,
            }
    with open('display_calibration.json', 'w') as fp:
        json.dump(cal, fp, indent=2)

def load_calibration():
    global minx, miny, maxx, maxy

    try:
        with open('display_calibration.json', 'r') as fp:
            cal = json.load(fp)

        minx = cal['minx']
        miny = cal['miny']
        maxx = cal['maxx']
        maxy = cal['maxy']
    except FileNotFoundError as _:
        pass

def screen_press(x, y):
    global minx, miny, maxx, maxy

    minx = min(minx, x)
    miny = min(miny, y)
    maxx = max(maxx, x)
    maxy = max(maxy, y)

    save_calibration()

    try:
        px_x = int(width * (x - minx) / (maxx - minx))
        px_y = int( height * (y - miny) / (maxy - miny))

        touch_fn(px_x, px_y)
    except:
        pass

def touch(fn):
    global touch_fn
    touch_fn = fn
    touch_thread.start()
    return fn

def touch_loop():
    for event in dev.read_loop():
        if event.type == ecodes.ABS_RX and event.code == 0 and event.type == 3:
            lasty = event.value
        elif event.type == ecodes.ABS_RX and event.code == 1 and event.type == 3:
            lastx = event.value
        elif event.type == ecodes.EV_KEY and event.value == 0:
            screen_press(lastx, lasty)

load_calibration()
touch_thread = threading.Thread(target=touch_loop)
