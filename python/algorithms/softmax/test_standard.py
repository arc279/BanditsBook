import os
import sys
import random
from core import *
import means

random.seed(1)

base_dir = os.getenv("BASE_DIR")
num_sims = int(os.getenv("NUM_SIMS"))
horizon = int(os.getenv("HORIZON"))
n_arms = int(os.getenv("N_ARMS"))

#temperatures = [0.1, 0.2, 0.3, 0.4, 0.5]
temperatures = [2**(i) for i in range(-5, 5)]

mean_type = os.getenv("MEAN_TYPE")
mean_proc = means.Types[mean_type]
means = mean_proc(n_arms)

best_arm = ind_max(means)
save_format = "%dx%d_%dx%d" % (n_arms, best_arm, horizon, num_sims)
output_sims_file = os.path.join(base_dir, "%s.sims.tsv" % save_format)
output_means_file = os.path.join(base_dir, "%s.means.tsv" % save_format)
output_result_file = os.path.join(base_dir, "%s.results.tsv" % save_format)

arms = list(map(lambda mu: BernoulliArm(mu), means))
print("means: %s" % mean_type, file=sys.stderr)
print("temperatures: %s" % temperatures, file=sys.stderr)
print("Num of arms: %d" % n_arms, file=sys.stderr)
print("Best arm is %d" % best_arm, file=sys.stderr)
print("Sim: %d * Times: %d" % (num_sims, horizon), file=sys.stderr)
print(best_arm)

with open(output_means_file, "w") as f:
  for m in means:
    print(str(m), file=f)

with open(output_sims_file, "w") as f:
  with open(output_result_file, "w") as f2:
    for temperature in temperatures:
      algo = Softmax(temperature, [], [])
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
            temperature,
            sim,
            t,
            chosen_arm,
            reward,
            cumulative_reward,
          ]]))  
          f.write("\n")

      for i, (x, y) in enumerate(zip(algo.values, algo.counts)):
        f2.write("\t".join([str(x) for x in [
          temperature,
          i,
          x,
          y,
        ]]))  
        f2.write("\n")

