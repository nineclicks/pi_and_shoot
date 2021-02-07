from gpiozero import LED, Button

button_params = {
        'bounce_time': 0.01,
        }

shutter_button = Button(21, **button_params)
menu_button = Button(20, **button_params)

def press_menu_button(fn):
    menu_button.when_pressed = fn
    return fn

def press_shutter_button(fn):
    shutter_button.when_pressed = fn
    return fn
