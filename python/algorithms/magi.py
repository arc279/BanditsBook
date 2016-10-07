import os
import sys
import random
from core import *
import means
from thompson_sampling.ts import *
from softmax import *


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

algos = {
    "ThompsonSampling": ThompsonSampling([], [], []),
    "Softmax(0.125)": Softmax(0.125, [], []),
    "Softmax(0.25)": Softmax(0.25, [], []),
    "Softmax(0.5)": Softmax(0.5, [], []),
    "AnnealingSoftmax": AnnealingSoftmax([], []),
    "UCB1": UCB1([], []),
}

with open(output_means_file, "w") as f:
    for m in means:
        print(str(m), file=f)

with open(output_sims_file, "w") as f:
    for name, algo in algos.items():
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
                    name,
                    sim,
                    t,
                    chosen_arm,
                    reward,
                    cumulative_reward,
                ]]))
                f.write("\n")
