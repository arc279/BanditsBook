import sys
import random
import yaml
import itertools
import bisect
import numpy as np

from classification.classifier import BanditClassifier
from classification.dummy_weight import DummmyWeightArms
from pprint import pprint

random.seed(1)

# 試行回数
n = int(sys.argv[1]) if len(sys.argv) == 2 else 10000

# demo
#--------------------
# セグメント
segments = yaml.load(open("classification/segments.yml").read())
s = { x["name"]:BanditClassifier(x) for x in segments }

#--------------------
# ダミー確率
w = [ DummmyWeightArms(x) for x in segments ]
for x in w:
    pprint((x.name, list(zip(x.n, x.w, x.b))), stream=sys.stderr)

#--------------------
# 更新
import datetime, pytz
tz = pytz.timezone("Asia/Tokyo")
for i in range(n):
    pairs = []
    for a in w:
        seg_name, arm_name, reward = a.draw()
        segment = s[seg_name]
        segment.update(arm_name, reward)

        now = datetime.datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S%z')
        print("\t".join([str(i), now, seg_name, arm_name, str(reward)]))

#--------------------
# 結果表示
print("-"*50, file=sys.stderr)
for n, x in s.items():
    var = x.arm_weight()
    mean = x.arm_mean()
    pprint((n, ("var", var), ("mean", mean),
        list(zip(x.arm_names, x.algo.values, x.algo.counts_alpha, x.algo.counts_beta))), stream=sys.stderr)

