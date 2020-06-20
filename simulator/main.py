#!/usr/bin/env python3

import random
import time
import sys
import argparse

from numba import jit, cuda
import numpy as np

from datetime import timedelta
import time

from multiprocessing import Pool

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

def generateRandomRates():
	rates = np.asarray([random.randint(*rate_range) for rate_range in HORSE_RATE_RANGES])
	rates.sort()

	return rates

# def getRewardFromRates(rates):
# 	return [(1 / (rate + 1)) for rate in rates]

def getWeightsFromRates(rates):
	rates = [(1 / (rate + 1))  for rate in rates]
	total = sum(rates)

	return [(rate / total) for rate in rates]

def getBetAmmount(balance):
	bet = int(balance * PERCENAGE_FOR_BET)

	return bet

def getWinnerHorse(rates):
	population = list(range(len(rates)))
	weights = getWeightsFromRates(rates)

	return random.choices(population, weights)[0]

MAX_FIRST_HORSE_WEIGHT = getWeightsFromRates([1, 5, 15, 15, 30, 30])[0]

def play_run(balance = 1000 , iterations = 1):
	for i in range(iterations):

		if balance <= 0:
			# print(f'You run out of money in {i} iterations')
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

	args = parser.parse_args(sys.argv[1:])


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

	print(f'Time: {elapsed_time}')
	print(f'Time per run: {elapsed_time / args.runs}')


	expected_time = timedelta(seconds=args.iterations * SECONDS_PER_RUN)

	average_balance = int(total_balance / args.runs)
	average_benefits = average_balance - args.balance

	average_balance_per_hour = int(average_balance / (expected_time.total_seconds() / 3600))

	print('Average results:')
	print(f'\tBalance  :  {average_balance:*>+,}')
	print(f'\tBenefits :  {average_benefits:*>+,}')
	print(f'\tTime     :  {expected_time}')
	print(f'\t$ / Hour :  {average_balance_per_hour:*>+,}')
	print(f'\tFail %   :  {total_fails / args.runs * 100 :.2f}')
