import itertools
import bisect
import random

#--------------------
# ダミー確率
class DummmyWeightArms:
    def __init__(self, segment):
        self.name = segment["name"]
        values = [ (x['name'], x["dummy"]['weight'], x["dummy"]['bernoulli']) for x in segment["arms"] ]
        self.n, self.w, self.b = zip(*values)
        self.cumdist = list(itertools.accumulate(self.w))

    def draw(self):
        # 重み付き確率
        x = random.random() * self.cumdist[-1]
        a = bisect.bisect(self.cumdist, x)
        # ベルヌーイ試行
        if random.random() > self.b[a]:
            reward = 0.0
        else:
            reward = 1.0

        return (self.name, self.n[a], reward)

