import os
import sys
import random
from core import *
import means
import ts

random.seed(1)

base_dir = os.getenv("BASE_DIR")
num_sims = int(os.getenv("NUM_SIMS"))
horizon = int(os.getenv("HORIZON"))
n_arms = int(os.getenv("N_ARMS"))

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
print("Num of arms: %d" % n_arms, file=sys.stderr)
print("Best arm is %d" % best_arm, file=sys.stderr)
print("Sim: %d * Times: %d" % (num_sims, horizon), file=sys.stderr)
print(best_arm)

with open(output_means_file, "w") as f:
    for m in means:
        print(str(m), file=f)

algo = ts.ThompsonSampling([], [], [])

with open(output_sims_file, "w") as f:
    with open(output_result_file, "w") as f2:
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
                    sim,
                    t,
                    chosen_arm,
                    reward,
                    cumulative_reward,
                ]]))
                f.write("\n")

        for i, (v, a, b) in enumerate(zip(algo.values, algo.counts_alpha, algo.counts_beta)):
            f2.write("\t".join([str(x) for x in [
                i,
                v,
                a,
                b,
            ]]))
            f2.write("\n")
