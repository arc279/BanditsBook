import numpy as np
from algorithms.thompson_sampling import ts

"""ThompsonSamplingを用いたセグメント分類"""
class BanditClassifier():
    def __init__(self, segment):
        self.name = segment["name"]
        self.label = segment["label"]
        self.arms = segment["arms"]
        self.arm_names = [ x["name"] for x in self.arms ]

        self.algo = ts.ThompsonSampling([], [], [])
        self.algo.initialize(len(self.arms))

    def update(self, arm_name, reward):
        try:
            select_arm = self.arm_names.index(arm_name)
            self.algo.update(select_arm, reward)
        except ValueError as e:
            # TODO:
            print(e)

    """事後分布"""
    def posterior_distribution(self):
        return list(zip(self.arm_names, self.algo.values))

    def arm_weight(self):
        return np.std(self.algo.values)

    def arm_mean(self):
        return np.mean(self.algo.values)

