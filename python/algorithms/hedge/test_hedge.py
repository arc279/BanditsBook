exec(open("core.py").read())

import os
import sys
import random

output_dir = "/Users/automagi/workspace/R/hedge_results"

num_sims = int(os.getenv("NUM_SIMS"))
horizon = int(os.getenv("HORIZON"))
n_arms = int(os.getenv("N_ARMS"))

random.seed(1)
#means = [0.1, 0.1, 0.1, 0.1, 0.9]
#random.shuffle(means)
if True:
  means = [random.random() for x in range(n_arms)]
else:
  means = [0.2 for x in range(n_arms)]
  means[-1] = 0.9 # 最後の腕が一番良い

best_arm = ind_max(means)
output_file = os.path.join(output_dir, "%dx%d_%dx%d.tsv" % (n_arms, best_arm, horizon, num_sims))

arms = list(map(lambda mu: BernoulliArm(mu), means))
print("Num of arms: %d" % n_arms, file=sys.stderr)
print("Best arm is %d" % best_arm, file=sys.stderr)
print("Sim: %d * Times: %d" % (num_sims, horizon), file=sys.stderr)
print(best_arm)

with open(output_file, "w") as f:
  for eta in [.5, .8, .9, 1, 2]:
    algo = Hedge(eta, [], [])
    algo.initialize(n_arms)

    for sim in range(num_sims):
      cumulative_reward = 0
      sim = sim + 1
      algo.initialize(len(arms))
      
      for t in range(horizon):
        t = t + 1
        
        chosen_arm = algo.select_arm()
        reward = arms[chosen_arm].draw()
        cumulative_reward += reward
        algo.update(chosen_arm, reward)

        f.write("\t".join([str(x) for x in [
          eta,
          sim,
          t,
          chosen_arm,
          reward,
          cumulative_reward,
        ]]))  
        f.write("\n")

