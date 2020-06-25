#!/usr/bin/env python3

import numpy as np
from collections import namedtuple

import utils
from bet import Bet
from strategies import Strategies


from constants import *


class NotEnoughMoney(Exception):
	pass

class GameState:
	def __init__(self, balance: int, strategy):
		self.__balance = balance
		self.__strategy = strategy

	def getBalance(self) -> int:
		return self.__balance

	def __placeBet(self, bet: Bet, rates, weights):

		winner = np.random.choice(rates.size, p=weights)

		if winner == bet.index:
			prize = bet.amount * rates[bet.index]
			self.__balance += prize
		else:
			self.__balance -= bet.amount

	def nextStep(self):
		if self.__balance <= MIN_BET:
			raise NotEnoughMoney()

		rates = utils.generateRandomRates()
		weights = utils.getWeightsFromRates(rates)

		bet = self.__strategy(self.__balance, rates, weights)
		self.__placeBet(bet, rates, weights)
