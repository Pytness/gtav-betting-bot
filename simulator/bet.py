from collections import namedtuple
from constants import MIN_BET, MAX_BET

class Bet():
	@staticmethod
	def __correctBetAmmount(amount):
		if amount < MIN_BET:
			return MIN_BET
		elif amount > MAX_BET:
			return MAX_BET

		if amount < 1000:
			return (amount // 100) * 100
		else:
			return ((amount - 1000) // 500) * 500 + 1000

	def __new__(self, index, amount):
		__bet = namedtuple('Bet', ['index', 'amount'])

		if type(index) != int or type(amount) != int:
			raise ValueError('index and ammount must be int')

		amount = Bet.__correctBetAmmount(amount)

		return __bet(index, amount)
