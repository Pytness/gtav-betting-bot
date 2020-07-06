#!/usr/bin/env python3

import random
import string
from PIL import Image, ImageFont, ImageDraw
from collections import namedtuple

FOLDER = 'training-data'

LANG = 'eng'
FONTNAME = 'pricedown'

IMAGE_COUNT = 30

LINE_WIDTH = 40
LINE_COUNT = 20

MARGIN = 20

Box = namedtuple('Box', ['symbol', 'left', 'bottom', 'right', 'top', 'page'])

font = ImageFont.truetype("./pricedown.ttf", 42)

population = ''.join([
	# string.ascii_letters,
	string.digits,
	'/'
	# string.punctuation,

])

def generate_image():
	global population

	text = '\n'.join([
		''.join(random.choices(population, k=LINE_WIDTH))
		for i in range(LINE_COUNT)
	])

	text_width, text_height = font.getsize_multiline(text)

	image = Image.new('RGB', (text_width + MARGIN * 2, text_height + MARGIN * 2), "white")

	IMAGE_WIDTH, IMAGE_HEIGHT = image.size
	xy = (MARGIN, MARGIN)

	draw = ImageDraw.Draw(image)
	draw.text(xy, text, 'black', font)

	boxes = []

	for line_number, line in enumerate(text.split('\n')):

		line_margin = line_number * (font.font.ascent + (font.font.descent // 2))

		for i, char in enumerate(line):
			bottom_1 = font.getsize(line[i])[1]
			right, bottom_2 = font.getsize(line[:i+1])

			bottom = bottom_1 if bottom_1 < bottom_2 else bottom_2
			width, height = font.getmask(char).size

			right += xy[0]
			bottom += xy[1] + line_margin

			top = bottom - height
			left = right - width

			boxes.append(Box(char,
				left, top,
				right, bottom,
				0
			))

			# draw.rectangle((left, top, right, bottom), None, "#f00")

	return (image, boxes)


for i in range(IMAGE_COUNT):
	image, boxes = generate_image()

	image.save(f'{FOLDER}/{LANG}.{FONTNAME}.exp{i}.png')
	# image.show()


	with open(f'{FOLDER}/{LANG}.{FONTNAME}.exp{i}.box', 'w') as boxfile:
		for box in boxes:
			box = ' '.join(map(str, list(box)))
			boxfile.write(box + '\n')
