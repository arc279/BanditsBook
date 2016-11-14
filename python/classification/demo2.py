import sys
import random
import yaml
import itertools
import bisect
import numpy as np
import datetime, pytz

from classification.classifier import BanditClassifier
from pprint import pprint

random.seed(1)

# 試行回数
n = int(sys.argv[1]) if len(sys.argv) == 2 else 10000

#--------------------
# ダミー確率
class DummmyWeightArms:
    class DummmyWeightArm:
        def __init__(self, segment):
            self.name = segment["name"]
            self.weight = segment["dummy"]["weight"]

            values = [ (x['name'], x["dummy"]['weight'], x["dummy"]['bernoulli']) for x in segment["arms"] ]
            self.n, self.w, self.b = zip(*values)
            self.cumdist = list(itertools.accumulate(self.w))

        def select_arm(self):
            # 重み付き確率
            x = random.random() * self.cumdist[-1]
            a = bisect.bisect(self.cumdist, x)
            return (self.name, self.n[a], self.b[a])

    def __init__(self, segments):
        self.w = [ self.DummmyWeightArm(x) for x in segments ]
        a, n = zip(*[ (d.weight, d.name) for d in self.w ])
        self.seg_weights = np.array(a) / sum(a)
        self.seg_names = n

    def draw(self):
        a = [ n.select_arm() for n in self.w ]

        r = sum([ x[2] * self.seg_weights[i] for i, x in enumerate(a) ])
        if random.random() > r:
            reward = 0.0
        else:
            reward = 1.0

        return reward, a

    def sample_each_line(self, seg, n):
        tz = pytz.timezone("Asia/Tokyo")
        for i in range(n):
            now = datetime.datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S%z')
            reward, arms = w.draw()

            for seg_name, arm_name, p in arms:
                segment = s[seg_name]
                segment.update(arm_name, reward)
                print("\t".join([str(i), now, str(reward), seg_name, arm_name]))

    def sample_one_line(self, seg, n):
        tz = pytz.timezone("Asia/Tokyo")
        for i in range(n):
            now = datetime.datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S%z')
            reward, arms = w.draw()

            arm_names = []
            for seg_name, arm_name, p in arms:
                segment = s[seg_name]
                segment.update(arm_name, reward)
                arm_names.append(arm_name)

            print("\t".join([str(i), now, str(reward)] + arm_names))


# demo
#--------------------
# セグメント
segments = yaml.load(open("classification/segments.yml").read())
s = { x["name"]:BanditClassifier(x) for x in segments }
print("事前分布", file=sys.stderr)
pprint(segments, stream=sys.stderr)

#--------------------
# ダミー確率
w = DummmyWeightArms(segments)
#w.sample_one_line(s, n)
w.sample_each_line(s, n)

#--------------------
# 結果表示
print("-"*50, file=sys.stderr)
print("事後分布", file=sys.stderr)
seg_weights = dict(zip(w.seg_names, w.seg_weights))
for n, x in s.items():
    var = x.arm_weight()
    mean = x.arm_mean()
    pprint((n, ("var", var), ("mean", mean), ("weight", seg_weights[n]),
        list(zip(x.arm_names, x.algo.values, x.algo.counts_alpha, x.algo.counts_beta))), stream=sys.stderr)

