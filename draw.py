from pickle import load
import pygame
import re
from urllib.request import urlretrieve
from getpass import getuser
from os import remove
import pyautogui
from pynput.keyboard import Listener
import threading
# from random_utils.funcs import crash
import numpy as np
import ctypes
pyautogui.PAUSE = 0


next_col = False

def crash():
    ctypes.pointer(ctypes.c_char.from_address(5))[0]


def check_key(key):
    global next_col
    if hasattr(key, "_name_"):
        next_col = key._name_ == "right"
    elif hasattr(key, "char"):
        if key.char == "q":
            crash()


def monitor_keys():
    with Listener(on_press=check_key) as l:
        l.join()


def compare_colors(c1, c2):
    return abs(sum(np.array(c1) - np.array(c2)))


def get_best_color(colors, color):
    diffs = [(compare_colors(c, color), c) for c in colors.values()]
    return min(diffs, key=lambda x: x[0])[1]


threading.Thread(target=monitor_keys).start()


data = load(open("screen_info.skribbl_draw", "rb"))
colors = data["colors"]
rect = data["rect"]

pattern = re.compile(r"https?://")
path = input("Link or path: ")
if re.search(pattern, path):
    img_path = f"/home/{getuser()}/temp_skribbl"
    urlretrieve(path, img_path)
    res = tuple(map(int, input("Resolution (WxH): ").split("x")))  # Duplicated so that urlretrieve can check url before getting resolution... saves time
    image = pygame.transform.scale(pygame.image.load(img_path), res)
    remove(img_path)
else:
    res = tuple(map(int, input("Resolution (WxH): ").split("x")))  # Duplicated so that urlretrieve can check url before getting resolution... saves time
    image = pygame.transform.scale(pygame.image.load(path), res)


for pos, color in colors.items():
    pyautogui.click(pos)
    for x in range(res[0]):
        for y in range(res[1]):
            if color == get_best_color(colors, image.get_at((x, y))[:3]):
                pyautogui.click(np.interp(x, (0, res[0]), (rect[0], rect[0] + rect[2])), np.interp(y, (0, res[1]), (rect[1], rect[1] + rect[3])))

            if next_col:
                break
        if next_col:
            break
    
    next_col = False

crash()
