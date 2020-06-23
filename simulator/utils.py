from collections import namedtuple
import numpy as np

from constants import *

def generateRandomRates() -> np.ndarray:
	rates: np.ndarray = np.asarray([
		np.random.randint(row[0], row[1] + 1)
		for row in HORSE_RATE_RANGES
	])

	rates.sort()

	return rates

def getWeightsFromRates(rates: np.ndarray) -> np.ndarray:
	weights: np.ndarray = np.asarray([(1 / (rate + 1))  for rate in rates])

	return weights / weights.sum()

def getBetAmmount(balance: int):
	return int(balance * PERCENAGE_FOR_BET)

def getWinnerHorse(rates: np.ndarray) -> int:
	weights = getWeightsFromRates(rates)
	return np.random.choice(rates.size, p=weights)

MAX_FIRST_HORSE_WEIGHT = getWeightsFromRates([1, 5, 15, 15, 30, 30])[0]
MAX_HORSE_WEIGHTS = tuple([
	getWeightsFromRates([1, 5, 15, 15, 30, 30])[0],
	getWeightsFromRates([5, 5, 15, 15, 30, 30])[1],
	getWeightsFromRates([5, 5, 6, 15, 30, 30])[2],
	getWeightsFromRates([5, 5, 15, 15, 30, 30])[3],
	getWeightsFromRates([5, 5, 15, 15, 16, 30])[4],
	getWeightsFromRates([5, 5, 15, 15, 30, 30])[5],
])
