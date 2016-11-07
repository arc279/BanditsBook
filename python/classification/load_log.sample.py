import sys
import yaml
from classifier import BanditClassifier
from pprint import pprint

# セグメント
segments = yaml.load(open("classification/segments.yml").read())
s = { x["name"]:BanditClassifier(x) for x in segments }

if __name__ == '__main__':
    fp = sys.stdin
    for l in fp:
        time, seg_name, arm_name, reward = l.rstrip().split("\t")
        segment = s[seg_name]
        segment.update(arm_name, float(reward))

    #--------------------
    # 結果表示
    print("-"*50, file=sys.stderr)
    for n, x in s.items():
        pprint((n, list(zip(x.arm_names, x.algo.values, x.algo.counts_alpha, x.algo.counts_beta))), stream=sys.stderr)

