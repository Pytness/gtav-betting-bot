#!/usr/bin/env python3

import random
import numpy as np
from numba import jit as _jit
import inspect

import utils


TYPE = 'Tuple((float64, float64))(float64, float64[:], float64[:])'

@_jit(TYPE)
def default(balance: float, rates: np.ndarray, weights: np.ndarray) -> tuple:
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

	return (0, betAmmount)

@_jit(TYPE)
def default_no_compensation(balance: float, rates: np.ndarray, weights: np.ndarray) -> tuple:
	'''
	Same as default, but it does not compensate a lower probability.
	'''

	firstRate = rates[0]
	firstWeight = weights[0]

	betAmmount = int(balance * utils.PERCENAGE_FOR_BET)

	return (0, betAmmount)

@_jit(TYPE)
def other(balance: float, rates: np.ndarray, weights: np.ndarray) -> tuple:
	'''
	Randomly bets to the lower probability (but higher reward) horse.
	Fallbacks to default.
	'''

	lastHorseWeight = weights[-1]
	lastHorseMaxWeight = 1 #utils.MAX_HORSE_WEIGHTS[-1]

	sigma = lastHorseWeight / lastHorseMaxWeight
	betAmmount = int(balance * utils.PERCENAGE_FOR_BET * sigma)

	if random.random() < lastHorseMaxWeight:
		return (5, betAmmount)

	return default(balance, rates, weights)

Strategies = [
	value
	for name, value in vars().items()
	if not name.startswith('_') and callable(value)
]

print(Strategies)
