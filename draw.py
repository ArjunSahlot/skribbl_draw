#
#  Scribble Draw
#  Automate drawing in skribbl.io
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from pickle import load
import pygame
import re
from urllib.request import urlretrieve
from getpass import getuser
from os import remove
import pyautogui
from pynput.keyboard import Listener
import threading
from random_utils.funcs import crash
import numpy as np
import sys
pyautogui.PAUSE = 0


next_col = False

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
    r = abs(c2[0] - c1[0])
    g = abs(c2[1] - c1[1])
    b = abs(c2[2] - c1[2])
    return r + g + b


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
    if sys.platform == "linux":
        img_path = f"/home/{getuser()}/temp_skribbl"
    elif sys.platform == "windows":
        img_path = f"C:/Users/{getuser()}/temp_skribbl"
    else:
        img_path = f"/Users/{getuser()}/temp_skribbl"

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
