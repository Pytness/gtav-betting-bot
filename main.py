from PIL import ImageGrab
from PIL import ImageOps
from PIL import ImageFilter

import pyautogui
pyautogui.FAILSAFE = False

import keyboard

import pytesseract
import directinput
import horserace

import math
import random
import time


import logging
logging.basicConfig(
	filename = 'autobet.log',
	level = logging.DEBUG,
	format = '%(asctime)-4s %(levelname)-8s %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)

def main():

	lastKnownBalance = 10000

	while True:
		# Press event button
		logging.debug('Pressing event button')

		horserace.startUniqueEvent()
		time.sleep(0.5)

		horse_rates = horserace.getHorseRates()
		logging.debug('Horse rates: %s' % horse_rates)

		firstHorseRate = min(horse_rates)

		first_horse_index = horse_rates.index(firstHorseRate)
		del horse_rates[first_horse_index]

		secondHorseRate = min(horse_rates)

		horserace.selectHorse(first_horse_index)
		time.sleep(0.5)

		try:
			currentBalance = horserace.getCurrentBalance()
			lastKnownBalance = currentBalance
		except:
			currentBalance = lastKnownBalance

		logging.debug('Current balance: %s' % currentBalance)


		# add more weight to the second horse rate
		secondHorseRate *= 2

		total_rate = firstHorseRate + secondHorseRate
		sigma = (secondHorseRate / total_rate) ** 2

		logging.debug('Sigma: %s' % sigma)

		betAmmount = int(horserace.getBetAmmount(currentBalance) * sigma)

		if betAmmount > horserace.MAX_BET:
			betAmmount = horserace.MAX_BET

		logging.debug('Current bet: %s' % betAmmount)

		horserace.raiseBet(betAmmount, sleep=0.1)
		horserace.bet()

		time.sleep(horserace.RACE_TIME)

		directinput.SendKey(directinput.KEY_ESCAPE)

		# input()

if __name__ == '__main__':
	keyboard.add_hotkey('up', main)
	keyboard.wait('esc')
