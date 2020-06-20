#!/usr/bin/env python3

import random
import time
import sys
import argparse
import numpy as np
from multiprocessing import Pool
from datetime import timedelta
import time

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

PERCENAGE_FOR_BET = 0.1
SECONDS_PER_RUN = 45

def generateRandomRates() -> np.ndarray:
	rates = np.asarray([
		np.random.randint(row[0], row[1] + 1)
		for row in HORSE_RATE_RANGES
	])

	rates.sort()

	return rates

def getWeightsFromRates(rates: np.ndarray) -> np.ndarray:
	weights = np.asarray([(1 / (rate + 1))  for rate in rates])

	return weights / weights.sum()

def getBetAmmount(balance: int):
	return int(balance * PERCENAGE_FOR_BET)

def getWinnerHorse(rates: np.ndarray) -> int:
	weights = getWeightsFromRates(rates)
	return np.random.choice(rates.size, p=weights)

MAX_FIRST_HORSE_WEIGHT = getWeightsFromRates([1, 5, 15, 15, 30, 30])[0]

def play_run(balance = 1000 , iterations = 1):
	for i in range(iterations):

		if balance <= 0:
			return 0

		horseRates = generateRandomRates()
		firstHorseRate = horseRates[0]

		weightRates = getWeightsFromRates(horseRates)
		firstHorseWeight = weightRates[0]

		sigma = firstHorseWeight / MAX_FIRST_HORSE_WEIGHT
		betAmmount = int(balance * PERCENAGE_FOR_BET * sigma)

		if betAmmount < MIN_BET:
			betAmmount = MIN_BET
		elif betAmmount > MAX_BET:
			betAmmount = MAX_BET

		if getWinnerHorse(horseRates) == 0:
			prize = betAmmount * firstHorseRate
			balance += prize
		else:
			balance -= betAmmount

	return balance


if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('-b', '--balance', type=int, default=1000,
		help='Starting balance for each run')

	parser.add_argument('-r', '--runs', type=int, default=1,
		help='Number of runs to simulate')

	parser.add_argument('-i', '--iterations', type=int, default=100,
		help='Number of iteration per run to do')

	parser.add_argument('-t', '--test', action='store_true',
		help='Do a test')

	args = parser.parse_args(sys.argv[1:])

	if args.test == True:
		rates = generateRandomRates()
		print(rates.tolist())

		weights = getWeightsFromRates(rates)
		print(weights.tolist())

		exit()


	total_balance = 0

	def target(x):
		return play_run(args.balance, args.iterations)

	start = time.perf_counter()

	with Pool() as pool:
		results = pool.map(target, range(args.runs))

		total_fails = results.count(0)
		total_balance = sum(results)

	end = time.perf_counter()

	elapsed_time = timedelta(seconds=end - start)

	print('Execution:')
	print(f'\tTotal time   : {elapsed_time}')
	print(f'\tTime per run : {elapsed_time / args.runs}\n')


	expected_time = timedelta(seconds=args.iterations * SECONDS_PER_RUN)

	average_balance = int(total_balance / args.runs)
	average_benefits = average_balance - args.balance

	average_balance_per_hour = int(average_balance / (expected_time.total_seconds() / 3600))

	print('Simulation average:')
	print(f'\tBalance         :  $ {average_balance:*>+,}')
	print(f'\tBenefits        :  $ {average_benefits:*>+,}')
	print(f'\tBenefits / Hour :  $ {average_balance_per_hour:*>+,}\n')
	print(f'\tFailed          :  {total_fails / args.runs * 100 :.4f}%\n')
	print(f'\tTime            :  {expected_time}')
