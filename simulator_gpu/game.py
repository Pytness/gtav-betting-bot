#!/usr/bin/env python3

import numpy as np
from collections import namedtuple

import utils
from bet import Bet
from strategies import Strategies
from constants import *

from numba import jit, types, typed
from numba.experimental import jitclass

class NotEnoughMoney(Exception):
	pass

@jitclass([
	('__balance', 'float64'),
        # ('__strategy', types.float64[:]())
])

class GameState:
	# @jit(types.void(types.float64, types.float64[:]()))
	def __init__(self, balance: float, strategy):
		self.__balance: float = balance
		self.__strategy = strategy

	# @jit(types.float64())
	def getBalance(self) -> int:
		return self.__balance

	@jit(types.float64[:]())
	def __strategy():
		pass

	@jit(types.void())
	def __placeBet(self, bet: Bet, rates, weights):

		# winner = ut

		if winner == bet.index:
			prize = bet.amount * rates[bet.index]
			self.__balance += prize
		else:
			self.__balance -= bet.amount

	# @jit
	def nextStep(self):
		if self.__balance <= MIN_BET:
			raise NotEnoughMoney()

		rates = utils.generateRandomRates()
		weights = utils.getWeightsFromRates(rates)

		bet = self.__strategy(self.__balance, rates, weights)
		self.__placeBet(bet, rates, weights)
