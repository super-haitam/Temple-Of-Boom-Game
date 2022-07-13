from PIL import Image, ImageDraw
import numpy as np


def drawLine(draw, start, end):
	draw.line([start, end], fill="black", width=0)

w, h = 40*20, 30*20
img = Image.new("RGB", (w, h), color=(108, 81, 70))

draw = ImageDraw.Draw(img)

interval = w//20
for i in range(interval):
	drawLine(draw, (i*interval, 0), (i*interval, h))

img.save("background.jpg")
