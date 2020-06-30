# Simulator

```usage: main.py [-h] [-t] [-b BALANCE] [-r RUNS] [-i ITERATIONS] [-s {0,1,2}]

optional arguments:
  -h, --help            show this help message and exit
  -t, --test            Do a test
                         (default: False)
  -b BALANCE, --balance BALANCE
                        Starting balance for each run
                         (default: 1000)
  -r RUNS, --runs RUNS  Number of runs to simulate
                         (default: 1)
  -i ITERATIONS, --iterations ITERATIONS
                        Number of iteration per run to do
                         (default: 100)
  -s {0,1,2}, --strategy {0,1,2}
                        [0] default:
                        Always bets on the horse with the highest probability to win and compensates
                        the lower probabilities by reducing the amount to bet:
                                # ...
                                sigma = horse_weight / max_horse_weight
                                amount = amount * sigma
                                # ...

                        [1] default_no_compensation:
                        Same as default, but it does not compensate a lower probability.

                        [2] other:
                        Randomly bets to the lower probability (but higher reward) horse.
                        Fallbacks to default.

                         (default: 0)```
