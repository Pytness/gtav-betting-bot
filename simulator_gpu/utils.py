#!/usr/bin/env python3

from collections import namedtuple
import numpy as np
import random

from numba import jit, types, typed

from constants import *


@jit(types.int8(types.float64[:], types.float64[:]))
def rand_choice_nb(arr, prob):
	return arr[np.searchsorted(np.cumsum(prob), np.random.random(), side="right")]

@jit(types.float64[:]())
def generateRandomRates() -> np.ndarray:
	rates: np.ndarray = np.asarray([
		np.random.randint(row[0], row[1] + 1)
		for row in HORSE_RATE_RANGES
	], dtype=np.float64)

	rates.sort()

	return rates

@jit(types.float64[:](types.float64[:]))
def getWeightsFromRates(rates: np.ndarray) -> np.ndarray:
	weights: np.ndarray = np.asarray([
		(1 / (rate + 1))
		for rate in rates
	], dtype=np.float64)

	return weights / weights.sum()

@jit(types.float64(types.float64))
def getBetAmmount(balance: types.float64):
	return balance * PERCENAGE_FOR_BET

@jit(types.int8(types.float64[:]))
def getWinnerHorse(rates: np.ndarray) -> int:
	weights = getWeightsFromRates(rates)

	population = np.asarray(
		[float(i) for i in range(rates.size)],
		dtype=np.float64
	)

	return rand_choice_nb(population, weights)



MAX_FIRST_HORSE_WEIGHT = getWeightsFromRates(np.asarray([1, 5, 15, 15, 30, 30], dtype=np.float64))[0]
MAX_HORSE_WEIGHTS = tuple([
	getWeightsFromRates(np.asarray([1, 5, 15, 15, 30, 30], dtype=np.float64))[0],
	getWeightsFromRates(np.asarray([5, 5, 15, 15, 30, 30], dtype=np.float64))[1],
	getWeightsFromRates(np.asarray([5, 5, 6, 15, 30, 30], dtype=np.float64))[2],
	getWeightsFromRates(np.asarray([5, 5, 15, 15, 30, 30], dtype=np.float64))[3],
	getWeightsFromRates(np.asarray([5, 5, 15, 15, 16, 30], dtype=np.float64))[4],
	getWeightsFromRates(np.asarray([5, 5, 15, 15, 30, 30], dtype=np.float64))[5],
])

# print(MAX_FIRST_HORSE_WEIGHT)
