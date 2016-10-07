exec(open("core.py").read())

import random

random.seed(1)
means = [0.1, 0.1, 0.1, 0.1, 0.9]
n_arms = len(means)
random.shuffle(means)
arms = list(map(lambda mu: BernoulliArm(mu), means))
print("Best arm is " + str(ind_max(means)))

algo = UCB1([], [])
algo.initialize(n_arms)
results = test_algorithm(algo, arms, 5000, 250)

f = open("algorithms/ucb/ucb1_results.csv", "w")

for i in range(len(results[0])):
  f.write(",".join([str(results[j][i]) for j in range(len(results))]) + "\n")

f.close()
