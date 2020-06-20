from PIL import ImageGrab
from PIL import ImageOps
from PIL import ImageFilter

import pyautogui
pyautogui.FAILSAFE = False

import keyboard

import pytesseract
import directinput

import math
import random
import time

import logging

positions = {
	'horse_rates_text': (
		(240, 465, 320, 505),
		(240, 627, 320, 667),
		(240, 789, 320, 829),
		(240, 951, 320, 991),
		(240, 1113, 320, 1153),
		(240, 1275, 320, 1315)
	),

	'unique_event_button':(1605, 1145, 2240, 1270),
	'balance_text': (1327, 510, 2091, 589),
	'bet_button': (1295, 988, 2114, 1114),
	'up_bet_button': (2004, 654, 2051, 728),
	'winner_text': (1242, 668, 1306, 735)
}

MIN_BET = 100
MAX_BET = 10000

HORSE_RATE_RANGES = (
	(1, 5),
	(1, 5),
	(6, 15),
	(6, 15),
	(16, 30),
	(16, 30)
)

PERCENAGE_FOR_BET = 0.05

RACE_TIME = 35

def makeImageRedeable(image, applyLambda = True):

	fn = lambda x : x if x < 80 else 255

	image = ImageOps.invert(image.convert('L'))
	if applyLambda:
		image = image.point(fn)

	image = image.convert('RGB').resize((image.size[0] * 2, image.size[1] * 2))
	# .filter(ImageFilter.GaussianBlur(radius=3))
	# image = image.resize((image.size[0] // 2, image.size[1] // 2))

	return image

def getStringFromImage(img):
	return pytesseract.image_to_string(img, lang="eng", config='--psm 6')

def getHorseRates():
	images = [ ImageGrab.grab(pos) for pos in positions['horse_rates_text'] ]

	rates = []
	for i, img in enumerate(images):
			img = makeImageRedeable(img, False)
			img_str = getStringFromImage(img)

			try:
				rate = int(img_str.split('/')[0])
			except:
				logging.error('Error: read "%s", saving image to %s.png' % (img_str, i))
				img.save('%s.png' % i)
				rate = HORSE_RATE_RANGES[i][0]

			rates.append(rate)

	return rates

def getCurrentBalance():
	img =  ImageGrab.grab(positions['balance_text'])
	img = makeImageRedeable(img)
	text = getStringFromImage(img).split(' ')[-1]
	# print('Debug: %s' % text)
	img.save('balance.png')

	return int(text)

def getBetAmmount(balance):
	bet = int(balance * PERCENAGE_FOR_BET)

	return bet

def getAmmountOfClicksForBet(bet):
	r = 1

	if bet < 1000:
		r = (bet // 100) - 1
	else:
		r = 9 + ((bet - 1000) // 500)

	return r

def getRandomPointInBox(box):
	width = box[2] - box[0]
	height = box[3] - box[1]

	return (
		box[0] + int(random.random() * width),
		box[1] + int(random.random() * height)
	)

def getWinnerHorse():
	img =  ImageGrab.grab(positions['balance_text'])
	img = makeImageRedeable(img)
	text = getStringFromImage(img)

	return int(text)

def virtualClickOnBox(box, sleep=0.5):
	pyautogui.moveTo(*getRandomPointInBox(box), 0.2, pyautogui.easeOutQuad)
	time.sleep(sleep)
	directinput.SendKey(directinput.KEY_RETURN)


def startUniqueEvent():
	virtualClickOnBox(positions['unique_event_button'])

def selectHorse(horse_number=0, sleep=0.1):
	virtualClickOnBox(positions['horse_rates_text'][horse_number], sleep)


def raiseBet(betAmmount, sleep=0.1):
	virtualClickOnBox(positions['up_bet_button'], sleep)

	for i in range(getAmmountOfClicksForBet(betAmmount)):
		directinput.SendKey(directinput.KEY_RETURN)
		time.sleep(sleep)

def bet(sleep=0.1):
	virtualClickOnBox(positions['bet_button'], sleep)
