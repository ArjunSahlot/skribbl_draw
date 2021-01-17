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
    colors[pos] = screen.getpixel(pos)[:3]

dump({"colors": colors, "rect": rect}, open("screen_info.skribbl_draw", "wb"))