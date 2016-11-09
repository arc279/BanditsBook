
def sim(
    fp,
    n_arm,
    best_arm,
    sim,
    times,
    chosen_arm,
    reward,
    cumulative_reward
):
    fp.write("\t".join([str(x) for x in [
        n_arm,
        best_arm,
        sim,
        times,
        chosen_arm,
        reward,
        cumulative_reward,
    ]]))
    fp.write("\n")
    
def arm(
    fp,
    n_arm,
    best_arm,
    arm_idx,
    arm_mean,
    value,
    alpha,
    beta,
):
    fp.write("\t".join([str(x) for x in [
        n_arm,
        best_arm,
        arm_idx,
        arm_mean,
        value,
        alpha,
        beta,
    ]]))
    fp.write("\n")
