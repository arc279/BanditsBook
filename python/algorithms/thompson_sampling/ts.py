import random


class ThompsonSampling():

    def __init__(self, counts_alpha, counts_beta, values):
        self.counts_alpha = counts_alpha
        self.counts_beta = counts_beta
        self.alpha = 1
        self.beta = 1
        self.values = values

    def initialize(self, n_arms):
        self.counts_alpha = [0 for col in range(n_arms)]
        self.counts_beta = [0 for col in range(n_arms)]
        self.values = [0.0 for col in range(n_arms)]

    def select_arm(self):
        theta = [(arm, random.betavariate(self.counts_alpha[arm] + self.alpha,
                                          self.counts_beta[arm] + self.beta)) 
                              for arm in range(len(self.counts_alpha))]
        theta = sorted(theta, key=lambda x: x[1])
        return theta[-1][0]

    def update(self, chosen_arm, reward):
        if reward == 1:
            self.counts_alpha[chosen_arm] += 1
        else:
            self.counts_beta[chosen_arm] += 1

        n = float(self.counts_alpha[chosen_arm]) + self.counts_beta[chosen_arm]
        self.values[chosen_arm] = (n - 1) / n * self.values[chosen_arm] + 1 / n * reward
