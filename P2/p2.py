import numpy as np
from math import log2
import copy

'''
This script is using all 9 features (2,3,...,10) to create a tree, which serves as a template.
Todo: you need to modify this by using the several specified features to create your own tree 
Todo: you need to do the pruning yourself
Todo: you need to get all the output including the test results.
Todo: you also need to generate the tree of such the format in the writeup: 'if (x3 <= 6) return 2 .......'
'''

with open('breast-cancer-wisconsin.data', 'r') as f:
    a = [l.strip('\n').split(',') for l in f if '?' not in l]


a = np.array(a).astype(int)   # training data
def count(data):
    a = sum((d[-1] == 2) * 1 for d in data)
    b = sum((d[-1] == 4) * 1 for d in data)
    return a, b
def entropy(data):
    count = len(data)
    p0 = sum(b[-1] == 2 for b in data) / count
    if p0 == 0 or p0 == 1: return 0
    p1 = 1 - p0
    return -p0 * log2(p0) - p1 * log2(p1)

ben, mal = count(a)
print(ben, mal, entropy(a))

def infogain(data, fea, threshold):  # x_fea <= threshold;  fea = 2,3,4,..., 10; threshold = 1,..., 9
    count = len(data)
    d1 = data[data[:, fea - 1] <= threshold]
    d2 = data[data[:, fea - 1] > threshold]
    if len(d1) == 0 or len(d2) == 0: return 0
    return entropy(data) - (len(d1) / count * entropy(d1) + len(d2) / count * entropy(d2))


def find_best_split(data):
    c = len(data)
    c0 = sum(b[-1] == 2 for b in data)
    if c0 == c: return (2, None)
    if c0 == 0: return (4, None)
    ig = [[infogain(data, fea, t) for t in range(1, 10)]for fea in range(2,11)]
    ig = np.array(ig)
    max_ig = max(max(i) for i in ig)
    if max_ig == 0:
        if c0 >= c - c0:
            return (2, None)
        else:
            return (4, None)
    ind = np.unravel_index(np.argmax(ig, axis=None), ig.shape)
    fea, threshold = ind[0] + 2, ind[1] + 1
    return (fea, threshold)


def split(data, node):
    fea, threshold = node.fea, node.threshold
    d1 = data[data[:,fea-1] <= threshold]
    d2 = data[data[:, fea-1] > threshold]
    return (d1,d2)


class Node:
    def __init__(self, fea, threshold):
        self.fea = fea
        self.threshold = threshold
        self.left = None
        self.right = None


for i in range (2, 11):
    ig = [[infogain(a, i, t) for t in range(1,10)]]
    ig = np.array(ig)
    print(i, ig)

# biggest information gains: 2,6; 3,2; 4,2; 5,3; 6,2; 7,2; 8,3; 9,2; 10,1
ig = [[infogain(a, 9, t) for t in range(1,10)]] #original ig = [[infogain(a, fea, t) for t in range(1,10)] for fea in range(2,11)]
ig = np.array(ig)
ind = np.unravel_index(np.argmax(ig, axis=None), ig.shape)
root1 = Node(9, ind[1] + 1)

root2 = Node(5,2)

root2.left = Node(3,3)
root2.right = Node(3,2)

root2.left.left = Node(6,3)
root2.left.right = Node(6,2)
root2.right.left = Node(6,3)
root2.right.right = Node(6,2)

root2.left.left.left = Node(10, 1)
root2.left.left.right = Node(10, 2)
root2.left.right.left = Node(10, 1)
root2.left.right.right = Node(10, 2)
root2.right.left.left = Node(10, 1)
root2.right.left.right = Node(10, 1)
root2.right.right.left = Node(10, 1)
root2.right.right.right = Node(10, 2)


root2.left.left.left.left = Node(9, 2)
root2.left.left.left.right = Node(9, 2)

root2.left.left.right.left = Node(9, 2)
root2.left.left.right.right = Node(9, 2)

root2.left.right.left.left = Node(9, 2)
root2.left.right.left.right = Node(9, 2)

root2.left.right.right.left = Node(9, 2)
root2.left.right.right.right = Node(9, 2)

root2.right.left.left.left = Node(9, 3)
root2.right.left.left.right = Node(9, 1)

root2.right.left.right.left = Node(9, 1)
root2.right.left.right.right = Node(9, 3)

root2.right.right.left.left = Node(9, 2)
root2.right.right.left.right = Node(9, 2)

root2.right.right.right.left = Node(9, 2)
root2.right.right.right.right = Node(9, 1)








print("root: ",root1.fea, root1.threshold)

def create_tree(data, node):
    d1,d2 = split(data, node)#splitting root. d1 = below threshold, d2 = above threshold
    if node.left != None:
        create_tree(d1, node.left)
    else: 
        #print(abs(count(d1)[0]-count(d1)[1]))
        #print(abs(count(d2)[0]-count(d2)[1]))
        print(count(d1)," -- ",count(d1)[0]-count(d1)[1])
        print(count(d2), " -- ", count(d2)[0]-count(d2)[1])
        return
    if node.right != None:
        create_tree(d2, node.right)
    else:
        #print(abs(count(d1)[0]-count(d1)[1]))
        #print(abs(count(d2)[0]-count(d2)[1]))
        print(count(d1), " -- ", count(d1)[0]-count(d1)[1])
        print(count(d2), " -- ", count(d2)[0]-count(d2)[1])
        return



    #d11, d12 = split(d01, node.left) #splitting one more for data below threshold d11 = 2, d12 = 4
    #d13, d14 = split(d02, node.right) # d13 = 
    return 



def create_stump(data, node):
    d1, d2 = split(data, node) #d1 = below threshold, d2 = above threshold
    print("d1: ", d1, "d2: ", d2)
    ben1, mal1 = count(d1)
    ben2, mal2 = count(d2)
    print("ben1: ", ben1, "mal1: ", mal1, "ben2: ", ben2, "mal2: ", mal2)


#create_stump(a, root1)

print(create_tree(a, root2))


with open('test.data', 'r') as f:
    t = [l.strip('\n').split(',') for l in f if '?' not in l]
t = np.array(t).astype(int)   # testing data


#print("t: ", t)


out = ""

print (out)

s1 = [root2]
s2 = []
while s1:
    s2 = copy.deepcopy(s1)
    s1 = []
    for n in s2:
        if n != 2 and n != 4:
            print(n.fea, n.threshold)
            if n.left != None: s1 += [n.left]
            if n.right != None: s1 += [n.right]
        else:
            print(n)

    print()

for data in t:
    if (data[4] <= 2):
        if (data[2] <= 3):
            if (data[5] <= 3):
                if (data[9] <= 1):
                    if(data[8] <= 2): out += "2,"
                    else: out += "2,"
                else:
                    if (data[8] <= 2): out += "2,"
                    else: out += "4,"
            else:
                if (data[9] <= 2):
                    if (data[8] <= 2): out += "2,"
                    else: out += "4,"
                else:
                    if (data[8] <= 2): out += "0,"
                    else: out += "4,"
              
        else:
            if (data[5] <= 2):
                if (data[9] <= 1):
                    if(data[8] <= 2): out += "4,"
                    else: out += "2,"
                else:
                    if (data[8] <= 2): out += "2(4),"
                    else: out += "0,"
            else:
                if (data[9] <= 2):
                    if (data[8] <= 2): out += "4,"
                    else: out += "4,"
                else:
                    if (data[8] <= 2): out += "4,"
                    else: out += "4,"
    else:
        if (data[2] <= 2):
            if (data[5] <= 3):
                if (data[9] <= 1):
                    if(data[8] <= 3): out += "2,"
                    else: out += "4,"
                else:
                    if (data[8] <= 1): out += "0,"
                    else: out += "0,"
            else:
                if (data[9] <= 1):
                    if (data[8] <= 1): out += "2,"
                    else: out += "2,"
                else:
                    if (data[8] <= 3): out += "0,"
                    else: out += "4,"      
        else:
            if (data[5] <= 2):
                if (data[9] <= 1):
                    if(data[8] <= 2): out += "4,"
                    else: out += "4,"
                else:
                    if (data[8] <= 2): out += "0,"
                    else: out += "4,"
            else:
                if (data[9] <= 2):
                    if (data[8] <= 2): out += "4,"
                    else: out += "4,"
                else:
                    if (data[8] <= 1): out += "4,"
                    else: out += "4,"
print(out)




