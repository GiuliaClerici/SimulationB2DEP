import random
from scipy.stats import bernoulli
import scipy
from collections import OrderedDict
import numpy as np

#random.uniform(0,1))

a = {0: 0.1, 1: 0.9, 2: 0.8, 3: 0.3, 4: 0.4}
p = {k: v for k, v in sorted(a.items(), key=lambda item: item[1], reverse=True)}
print(p)
print(p.keys())

mean = 0.0
means = np.array([])
for i in range(5):
    #print(list(p.keys())[i])
    val = p[list(p.keys())[i]]
    #print("val: ", val)
    mean = ((mean * i) + val) / (i+1)
    #print("mean: ", mean)
    means = np.append(means, mean)

print(means)
#for i in p.keys():
#    print("i: ", i)
#    for l in p.keys():
#        if p[l] > p[i] and i != l:
#            print("p[l]", p[l])