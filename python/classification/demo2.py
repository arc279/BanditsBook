import sys
import random
import yaml
import itertools
import bisect
from classification import BanditClassification
from pprint import pprint

# 試行回数
n = int(sys.argv[1])

# demo
#--------------------
# セグメント
segments = yaml.load(open("classification/segments.yml").read())
s = { x["name"]:BanditClassification(x) for x in segments }

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

w = [ DummmyWeightArms(x) for x in segments ]
for x in w:
    pprint((x.name, list(zip(x.n, x.w, x.b))), stream=sys.stderr)

#--------------------
# 更新
for _ in range(n):
    a = random.choice(w)
    seg_name, arm_name, reward = a.draw()
    segment = s[seg_name]
    segment.update(arm_name, reward)

    # ダミーログ出力
    print("%s\t%s\t%d" % (seg_name, arm_name, reward), file=sys.stdout)

#--------------------
# 結果表示
print("-"*50, file=sys.stderr)
for n, x in s.items():
    pprint((n, list(zip(x.arm_names, x.algo.values, x.algo.counts_alpha, x.algo.counts_beta))), stream=sys.stderr)

# ダミーログ出力
#>>> stdout
#income	400-600	1
#age	over60	0
#income	800-1000	1
#gender	unknown	1
#income	600-800	1
#gender	female	0
#marriage	married	1
#gender	female	1
#age	0-19	1
#income	200-400	1
#gender	female	1
#income	0-200	0
#income	800-1000	1
#age	40-50	0
#marriage	unmarried	1
#gender	female	1
#income	200-400	1
#age	0-19	1
#income	600-800	1
#age	50-60	1
#
# ダミーログ集計結果
#>>> stderr
#('gender', [('male', 10, 0.3), ('female', 20, 0.6), ('unknown', 5, 0.2)])
#('marriage', [('married', 5, 0.4), ('unmarried', 3, 0.6), ('unknown', 2, 0.3)])
#('income',
# [('0-200', 2, 0.3),
#  ('200-400', 4, 0.5),
#  ('400-600', 8, 0.7),
#  ('600-800', 7, 0.7),
#  ('800-1000', 4, 0.8),
#  ('over1000', 2, 0.6),
#  ('unknown', 2, 0.4)])
#('age',
# [('0-19', 8, 0.7),
#  ('20-30', 2, 0.3),
#  ('30-40', 2, 0.4),
#  ('40-50', 4, 0.8),
#  ('50-60', 8, 0.4),
#  ('over60', 9, 0.3),
#  ('unknown', 2, 0.3)])
#--------------------------------------------------
#('marriage',
# [('married', 0.3989811212449666, 50045, 75387),
#  ('unmarried', 0.5972163026105486, 44839, 30241),
#  ('unknown', 0.3021358291336694, 15108, 34896)])
#('income',
# [('0-200', 0.3094836118064829, 5316, 11861),
#  ('200-400', 0.5033952146416757, 17273, 17040),
#  ('400-600', 0.7010309278350484, 48076, 20503),
#  ('600-800', 0.6982425131728142, 41875, 18097),
#  ('800-1000', 0.7972820912317087, 27633, 7026),
#  ('over1000', 0.5996493278784378, 10260, 6850),
#  ('unknown', 0.40454545454545116, 7031, 10349)])
#('age',
# [('0-19', 0.7019088035486609, 40192, 17069),
#  ('20-30', 0.3015458459800919, 4272, 9895),
#  ('30-40', 0.39374386309440224, 5614, 8644),
#  ('40-50', 0.7959347886929753, 22751, 5833),
#  ('50-60', 0.4021140105352792, 23130, 34391),
#  ('over60', 0.29813936063935403, 19100, 44964),
#  ('unknown', 0.3023566654941942, 4298, 9917)])
#('gender',
# [('male', 0.29823584288280414, 21419, 50400),
#  ('female', 0.6001500585508924, 85588, 57023),
#  ('unknown', 0.20260378834441303, 7252, 28542)])
