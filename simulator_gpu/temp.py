#!/usr/bin/env python3
import numpy as np
from timeit import default_timer as timer
from numba import cuda, jit, cuda
from numba.cuda.random import init_xoroshiro128p_states, create_xoroshiro128p_states, xoroshiro128p_uniform_float32, xoroshiro128p_dtype
# from collections import Counter

import struct
import random
import math
import time
import os

gpu = cuda.get_current_device()


runs = 100
iterations = 10000000

total_size = runs * iterations

@cuda.jit
def gpu_generate_data(random_states, array):
	ranges =(
		(1, 5),
		(1, 5),
		(6, 15),
		(6, 15),
		(16, 30),
		(16, 30)
	)

	y = cuda.grid(1)

	if y < array.shape[0]:
		for x in range(0, array.shape[1], 2):
			_min, _max = ranges[x]

			r_value = xoroshiro128p_uniform_float32(random_states, y)
			a = math.floor(_min + r_value * (_max - _min))

			r_value = xoroshiro128p_uniform_float32(random_states, y)
			b = math.floor(_min + r_value * (_max - _min))

			# if b < a:
			# 	a, b = b, a

			array[y, x] = a
			array[y, x + 1] = b

@cuda.jit('void(float64[:, :])')
def gpu_transform_rates_to_weights(array):

	row = cuda.grid(1)

	if row < array.shape[0]:
		total = 0.0

		for i in range(array.shape[1]):
			array[row, i] = (1 / (array[row, i] + 1))
			total += array[row, i]

		for i in range(array.shape[1]):
			array[row, i] /= total

def execute_kernel(function, *arrays, shape):

	if type(shape) is int:
		shape = tuple([shape])

	dimmension = len(shape)

	if dimmension > 3:
		print('Max shape is 3')
		return

	threadsperblock = tuple([int(gpu.MAX_THREADS_PER_BLOCK ** (1 / dimmension))] * dimmension)
	blockspergrid = tuple(map(
		lambda t: max(t[0] // t[1], 1),
		zip(shape, threadsperblock)
	))

	function[blockspergrid, threadsperblock](*arrays)


start = timer()
rates = np.empty((iterations, 6), dtype='float64')
data_allocation_time = timer() - start
print(f'Data allocation took {data_allocation_time:f} seconds')

start = timer()
random_states = create_xoroshiro128p_states(rates.shape[0], time.time_ns())
random_state_generation_time = timer() - start
print(f'Random states allocation took {random_state_generation_time:f} seconds')

gpu_generation_time = 0
rates_copy_time = 0
gpu_transform_time = 0

rates_means = []
weights_means = []

for run in range(runs):
	start = timer()
	execute_kernel(gpu_generate_data, random_states, rates, shape = rates.shape[0])
	gpu_generation_time += timer() - start

	rates_means.append(rates.mean(0))

	start = timer()
	weights = np.copy(rates)
	rates_copy_time += timer() - start

	start = timer()
	execute_kernel(gpu_transform_rates_to_weights, weights, shape = weights.shape[0])
	gpu_transform_time += timer() - start

	weights_means.append(weights.mean(0))


print(np.asarray(rates_means).mean(0))
print(np.asarray(weights_means).mean(0))

print(f'Data gpu generation took {gpu_generation_time:f} seconds')
print(f'Data copy took {rates_copy_time:f} seconds')
print(f'Data gpu transform took {gpu_transform_time:f} seconds')


total_time = sum([
	data_allocation_time,
	random_state_generation_time,
	gpu_generation_time,
	rates_copy_time,
	gpu_transform_time,
])

print(f'total time: {total_time}')
