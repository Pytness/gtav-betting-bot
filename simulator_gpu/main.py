#!/usr/bin/env python3

import random
import time
import sys
import argparse
import numpy as np
from multiprocessing import Pool
from datetime import timedelta
import time
import inspect

import utils
import game
from strategies import Strategies


def play_run(balance, iterations, strategy):

	gameState = game.GameState(balance, strategy)

	for i in range(iterations):
		try:
			gameState.nextStep()
		except game.NotEnoughMoney as e:
			return 0

	return gameState.getBalance()

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
	pass

if __name__ == '__main__':

	parser = argparse.ArgumentParser(
		formatter_class=CustomFormatter
	)

	parser.add_argument('-t', '--test', action='store_true',
		help='Do a test\n')

	parser.add_argument('-b', '--balance', type=int, default=1000,
		help='Starting balance for each run\n')

	parser.add_argument('-r', '--runs', type=int, default=1,
		help='Number of runs to simulate\n')

	parser.add_argument('-i', '--iterations', type=int, default=100,
		help='Number of iteration per run to do\n')

	parser.add_argument('-s', '--strategy', type=int, default=0,
		choices=range(len(Strategies)),
		help='\n'.join([
			f'[{i}] {f.__name__}:\n{inspect.cleandoc(f.__doc__)}\n'
			for i, f in enumerate(Strategies)
		]) + '\n')

	args = parser.parse_args(sys.argv[1:])

	if args.test == True:
		rates = utils.generateRandomRates()
		print(rates.tolist())

		weights = utils.getWeightsFromRates(rates)
		print(weights.tolist())

		exit()

	total_balance = 0

	def target(x):
		return play_run(args.balance, args.iterations, Strategies[args.strategy])

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


	print('Simulation average:')

	expected_time = timedelta(seconds=args.iterations * utils.SECONDS_PER_RUN)

	average_balance = int(total_balance / args.runs)
	average_benefits = average_balance - args.balance

	average_balance_per_hour = int(average_balance / (expected_time.total_seconds() / 3600))

	print('Simulation average:')
	print(f'\tStrategy        :  {Strategies[args.strategy].__name__}')
	print(f'\tBalance         :  $ {average_balance:*>+,}')
	print(f'\tBenefits        :  $ {average_benefits:*>+,}')
	print(f'\tBenefits / Hour :  $ {average_balance_per_hour:*>+,}\n')
	print(f'\tFailed          :  {total_fails / args.runs * 100 :.4f}% ({total_fails} / {args.runs}) \n')
	print(f'\tTime            :  {expected_time}')
