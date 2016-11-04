import random
import yaml
from classification import BanditClassification

#--------------------
# demo
segments = yaml.load(open("classification/segments.yml").read())
s = { x["name"]:BanditClassification(x) for x in segments }

from pprint import pprint
income = s["income"]
pprint(income.arms)

samples = """0-200	0,0,0,0,1,1,1,1,0,1,0,1,0
200-400	0,1,1,1,0,1,1,1,0,1,1,1,1
400-600	1,1,0,0,0,0,1,0,0,1,0,0,0
600-800	1,1,1,1,0,1,1,1,0,0,1,0,0
800-1000	0,0,0,1,0,1,1,1,0,0,1,0,0
over1000	1,0,0,0,0,0,0,0,1,0,0,0,0
"""

for l in samples.splitlines():
    arm_name, rewards = l.split("\t")
    for r in rewards.split(","):
        income.update(arm_name, int(r))

print("-"*50)
pprint(list(zip(income.arm_names, income.algo.values, income.algo.counts_alpha, income.algo.counts_beta)))

#>>>
#[{'label': '200万未満', 'name': '0-200'},
# {'label': '200万~400万', 'name': '200-400'},
# {'label': '400万~600万', 'name': '400-600'},
# {'label': '600万~800万', 'name': '600-800'},
# {'label': '800万~1000万', 'name': '800-1000'},
# {'label': '1000万以上', 'name': 'over1000'}]
#--------------------------------------------------
#[('0-200', 0.4615384615384615, 6, 7),
# ('200-400', 0.7692307692307692, 10, 3),
# ('400-600', 0.3076923076923077, 4, 9),
# ('600-800', 0.6153846153846154, 8, 5),
# ('800-1000', 0.3846153846153845, 5, 8),
# ('over1000', 0.15384615384615385, 2, 11)]

