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

from PIL import ImageGrab
from pyautogui import position
from pickle import dump

input("Press enter when your cursor is at top left of drawing rect.")
x1, y1 = position()
input("Press enter when your cursor is at bottom right of drawing rect.")
x2, y2 = position()

rect = (x1, y1, x2 - x1, y2 - y1)
colors = {}

print("Taking screenshot for colors")
screen = ImageGrab.grab().convert("RGB")
print("Done")
for i in range(int(input("How many colors are available to draw with: "))):
    input(f"Color {i+1}. Enter when done.")
    pos = position()
    colors[pos] = screen.getpixel(pos)

dump({"colors": colors, "rect": rect}, open("screen_info.skribbl_draw", "wb"))
