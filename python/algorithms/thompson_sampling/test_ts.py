import os
import sys
import random
import datetime
from core import *
import means
import ts
from algorithms import output_log

random.seed(1)

base_dir = os.getenv("BASE_DIR")
num_sims = int(os.getenv("NUM_SIMS"))
horizon = int(os.getenv("HORIZON"))
n_arms = [ int(i) for i in os.getenv("N_ARMS").split(",") ]

mean_type = os.getenv("MEAN_TYPE")
mean_proc = means.Types[mean_type]

now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
save_format = "%s.%dx%d.%s" % (mean_type, horizon, num_sims, now)
output_arms_file = os.path.join(base_dir, "%s.arms.tsv" % save_format)
output_sims_file = os.path.join(base_dir, "%s.sims.tsv" % save_format)

print(now, file=sys.stderr)
print("arms: %s" % n_arms, file=sys.stderr)
print("means: %s" % mean_type, file=sys.stderr)
print("Sim: %d * Times: %d" % (num_sims, horizon), file=sys.stderr)
print(save_format)

try:
    fp1 = open(output_sims_file, "w")
    fp2 = open(output_arms_file, "w")

    for n_arm in n_arms:
        means = mean_proc(n_arm)
        best_arm = ind_max(means)
        arms = list(map(lambda mu: BernoulliArm(mu), means))

        algo = ts.ThompsonSampling([], [], [])
        algo.initialize(n_arm)

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

                output_log.sim(fp1,
                    n_arm=n_arm,
                    best_arm=best_arm,
                    sim=sim,
                    times=t,
                    chosen_arm=chosen_arm,
                    reward=reward,
                    cumulative_reward=cumulative_reward,
                )

        for i, m in enumerate(means):
            output_log.arm(fp2,
                n_arm=n_arm,
                best_arm=best_arm,
                arm_idx=i,
                arm_mean=m,
                value=algo.values[i],
                alpha=algo.counts_alpha[i],
                beta=algo.counts_beta[i],
            )

except Exception as e:
    print(e, file=sys.stderr)
    sys.exit(1)
finally:
    [ fp.close() for fp in [fp1, fp2] if fp is not None ]
