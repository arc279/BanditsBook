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
n_arms = [
#    5, 10, 25, 50, 100,
    5, 10, 20, 30, 40, 50
]

mean_type = os.getenv("MEAN_TYPE")
mean_proc = means.Types[mean_type]

save_format = "%dx%d" % (horizon, num_sims)
output_sims_file = os.path.join(base_dir, "%s.sims.tsv" % save_format)
output_means_file = os.path.join(base_dir, "%s.means.tsv" % save_format)
output_result_file = os.path.join(base_dir, "%s.results.tsv" % save_format)

print("means: %s" % mean_type, file=sys.stderr)
print("Sim: %d * Times: %d" % (num_sims, horizon), file=sys.stderr)

with open(output_sims_file, "w") as f, \
    open(output_result_file, "w") as f2, \
    open(output_means_file, "w") as f3:
    for n_arm in n_arms:
        means = mean_proc(n_arm)
        best_arm = ind_max(means)
        factor = "%d arms[best:%d]" % (n_arm, best_arm)
        arms = list(map(lambda mu: BernoulliArm(mu), means))

        algo = ts.ThompsonSampling([], [], [])
        algo.initialize(n_arm)

        for m in means:
            f3.write("\t".join([str(x) for x in [
                factor,
                m,
            ]]))
            f3.write("\n")

        for sim in range(num_sims):
            cumulative_reward = 0
            sim = sim + 1
            algo.initialize(n_arm)

            for t in range(horizon):
                t = t + 1

                chosen_arm = algo.select_arm()
                reward = arms[chosen_arm].draw()
                cumulative_reward += reward
                algo.update(chosen_arm, reward)

                f.write("\t".join([str(x) for x in [
                    factor,
                    sim,
                    t,
                    chosen_arm,
                    best_arm,
                    reward,
                    cumulative_reward,
                ]]))
                f.write("\n")

        for i, (v, a, b) in enumerate(zip(algo.values, algo.counts_alpha, algo.counts_beta)):
            f2.write("\t".join([str(x) for x in [
                factor,
                i,
                v,
                a,
                b,
            ]]))
            f2.write("\n")
