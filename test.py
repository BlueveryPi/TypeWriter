#!D:\anaconda3\envs\py39\pythonw.exe
import os
import threading

try:
    from pynput import keyboard
    import pygame
    import pystray
    from pystray import Menu, MenuItem
    from PIL import Image
except ModuleNotFoundError or ImportError:
    path=os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")+"/asset/requirments.txt"
    os.system(f'pip install -r {path}')

    from pynput import keyboard
    import pygame
    import pystray
    from pystray import Menu, MenuItem
    from PIL import Image

pygame.init()
pygame.mixer.init()

donepressed=[]

state = 0

def set_state(v):
    def inner(icon, item):
        global state
        state = v
    return inner

def get_state(v):
    def inner(item):
        return state == v
    return inner

def playsound():
    sound=pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")+"/asset/audio/sound.mp3")
    sound.set_volume(0.1)
    sound.play()

def on_press(key):
    if key not in donepressed and state == 0:
        donepressed.append(key)
        threading.Thread(target=playsound).start()

def on_release(key):
    try:
        donepressed.remove(key)
    except:
        pass



icon=Image.open(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")+"/asset/typewriter.png")
icon=pystray.Icon("TypeWriter", icon=icon,
    menu=Menu(
    MenuItem("On", set_state(0), checked=get_state(0), radio=True),
    MenuItem("Off", set_state(1), checked=get_state(1), radio=True))).run_detached()

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()