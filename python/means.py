import random

# 一様ランダム
def random_means(n_arms):
  return [random.random() for x in range(n_arms)]

# 偏り
def deflected_means(n_arms, from_=0.1, to_=0.3, needle=0.9):
  means = [random.uniform(from_, to_) for x in range(n_arms)]
  means[0] = needle
  random.shuffle(means)
  return means

# 範囲内ランダム
def average_means(n_arms, from_=0.1, to_=0.3):
  return [random.uniform(from_, to_) for x in range(n_arms)]

Types = {
  "random": random_means,
  "deflected": deflected_means,
  "average": average_means,
}
