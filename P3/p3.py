from collections import Counter, OrderedDict
from itertools import product
import matplotlib.pyplot as plt
from random import choice

import numpy as np
import string
import sys
import re
from math import log2
import math


# in this piece of code, I leave out a bunch of thing for you to fill up modify.
# The current code may run into a ZeroDivisionError. Thus, you need to add Laplace first.
'''
Todo: 
1. Laplace smoothing
2. Naive Bayes prediction
3. All the output.

'''


with open('wallst.txt', encoding='utf-8') as f:
    data = f.read()

data = data.lower()
data = data.translate(str.maketrans('', '', string.punctuation))
data = re.sub('[^a-z]+', ' ', data)
data = ' '.join(data.split(' '))

allchar = ' ' + string.ascii_lowercase

unigram = Counter(data)
unigram_prob = {ch: round((unigram[ch]) / (len(data)), 4) for ch in allchar}
#print("unigram probability: ",unigram_prob)
uni_list = [unigram_prob[c] for c in allchar]

def ngram(n):
    # all possible n-grams
    d = dict.fromkeys([''.join(i) for i in product(allchar, repeat=n)],0)
    # update counts
    d.update(Counter([''.join(j) for j in zip(*[data[i:] for i in range(n)])]))
    return d

bigram = ngram(2)  # c(ab)
bigram_prob = {c: ((bigram[c]) / (unigram[c[0]])) for c in bigram}  # p(b|a)
bigram_prob_smoothed = {c: round(((bigram[c]+1) / (unigram[c[0]] + 27)), 4) for c in bigram}
print("bigram probability smoothed: ", bigram_prob_smoothed, len(bigram_prob_smoothed))

trigram = ngram(3)
trigram_prob = {c: (trigram[c]+1) / (bigram[c[:2]]+19683) for c in trigram}


def gen_bi(c):
    w = [bigram_prob_smoothed[c + i] for i in allchar]
    return choices(allchar, weights=w)[0]
    

def gen_tri(ab):
    w_tri = [trigram_prob[ab + i] for i in allchar]
    return choices(allchar, weights=w_tri)[0]   


def gen_sen(c, num):
    res = c + gen_bi(c)
    for i in range(num - 2):
        if bigram[res[-2:]] == 0:
            t = gen_bi(res[-1])
        else:
            t = gen_tri(res[-2:])
        res += t
    return res

sentences = []
for c in string.ascii_lowercase:
    example_sentence = gen_sen(c, 1000)
    sentences.append(example_sentence)
    print(example_sentence)
with open('script.txt', encoding='utf-8') as f:
    young = f.read() 

dict2 = Counter(young)
likeli = [dict2[c] / len(young) for c in allchar]
print(likeli)
post_young = [round(likeli[i] / (likeli[i] + uni_list[i]), 4) for i in range(27)]

post_hugh = [1 - post_young[i] for i in range(27)]
print(post_young)

def naive_bayes(sentence):
    #return maximum probability given the 2 scripts
    #a = sentence| my script
    #b= sentence| profs script
    #if a > b return 0 else return 1
    a = 0
    b = 0
    for char in allchar:
        a += log2(unigram_prob[char])
    for char in sentence:
        b += log2(post_young[allchar.index(char)])
    if a > b:
        return 0
    else:
        return 1
vals = []
for sentence in sentences:
    vals.append(naive_bayes(sentence))

if __name__ == "__main__":
    pass
print(vals)