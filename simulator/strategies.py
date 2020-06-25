import random
import numpy as np

from bet import Bet
import utils

class __Strategies:

	def default(self, balance: int, rates: np.ndarray, weights: np.ndarray) -> Bet:
		'''
		Always bets on the horse with the highest probability to win and compensates
		the lower probabilities by reducing the amount to bet:
			# ...
			sigma = horse_weight / max_horse_weight
			amount = amount * sigma
			# ...

		'''

		firstRate = rates[0]
		firstWeight = weights[0]

		sigma = firstWeight / utils.MAX_FIRST_HORSE_WEIGHT
		betAmmount = int(balance * utils.PERCENAGE_FOR_BET * sigma)

		return Bet(0, betAmmount)

	def default_no_compensation(self, balance: int, rates: np.ndarray, weights: np.ndarray) -> Bet:
		'''
		Same as default, but it does not compensate a lower probability.
		'''

		firstRate = rates[0]
		firstWeight = weights[0]

		betAmmount = int(balance * utils.PERCENAGE_FOR_BET)

		return Bet(0, betAmmount)

	def other(self, balance: int, rates: np.ndarray, weights: np.ndarray) -> Bet:
		'''
		Randomly bets to the lower probability (but higher reward) horse.
		Fallbacks to default.
		'''

		lastHorseWeight = weights[-1]
		lastHorseMaxWeight = utils.MAX_HORSE_WEIGHTS[-1]

		sigma = lastHorseWeight / lastHorseMaxWeight
		betAmmount = int(balance * utils.PERCENAGE_FOR_BET * sigma)

		if random.random() < lastHorseMaxWeight:
			return Bet(5, betAmmount)

		return self.default(balance, rates, weights)

	def __iter__(self):
		return (
			getattr(self, name)
			for name in dir(self)
			if not name.startswith('_')
		)

	def __getitem__(self, index):
		if type(index) != int:
			raise ValueError('index must be int')

		return list(iter(self))[index]

	def __len__(self):
		return len(list(iter(self)))


Strategies = __Strategies()
