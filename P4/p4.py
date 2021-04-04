import numpy as np
import math

'''
Todo: 
1. Part 1 in P4.
2. Euclidean distance (currently are all manhattan in my code below)
3. Complete linkage distance
4. Total distortion
5. Output all required information in correct format

PS: Currently, I choose 
	n = num of all distinct countries, and
	m = 3 (latitude, longitude, total deaths until Jun27, 
		  i.e., 1st, 2nd, last number for each country as parameters).
	Also, for countries that have several rows, I average the latitude, longitude and sum up the deaths.

	You may need to change some of that based on your part 1 results.

'''



# For 'South Korea', and "Bonaire Sint Eustatius and Saba" (line 145 and 257), I removed the ',' in name manually
with open('time_series_covid19_deaths_global.csv') as f:
    data = list(f)[1:]
with open('time_series_covid19_deaths_US.csv') as f:
    data_us = list(f)[1:]


d_dict = {}
for d in data:
    l = d.strip('\n').split(',')
    c = l[1]  # country
    if c in d_dict:
        d_dict[c][0].append(float(l[2]))
        d_dict[c][1].append(float(l[3]))
        d_dict[c][2].append(float(l[-1]))
    else:
        d_dict[c] = [[float(l[2])], [float(l[3])], [float(l[-1])]]
d_dict = {k:np.array([sum(v[0])/len(v[0]), sum(v[1])/len(v[1]), sum(v[2])]) for k,v in d_dict.items()}
countries = sorted([c for c in d_dict.keys()])
#for c in countries:
#    print(*d_dict[c], sep= ',')

time_series_list = []
for d in data:
    l = d.strip('\n').split(',')
    lst = []
    if l[1] == 'Canada':
        del(l[:4])
        for i in range(len(l)):
            l[i] = float(l[i])
        if time_series_list:
            for i in range(len(time_series_list)):
                time_series_list[i] += l[i]
        else:
            time_series_list = l
time_series_list_us = []
for d in data:
    l = d.strip('\n').split(',')
    lst = []
    if l[1] == 'US':
        del(l[:4])
        for i in range(len(l)):
            l[i] = float(l[i])
        if time_series_list_us:
            for i in range(len(time_series_list_us)):
                time_series_list_us[i] += l[i]
        else:
            time_series_list_us = l

#print(time_series_list)   
#print(time_series_list_us) 

time_series_list_difference = time_series_list
time_series_list_difference_us = time_series_list_us   
for i in reversed(range(1,len(time_series_list_difference))):
    time_series_list_difference[i] -= time_series_list_difference[i-1]
del(time_series_list_difference[0])
for i in reversed(range(1,len(time_series_list_difference_us))):
    time_series_list_difference_us[i] -= time_series_list_difference_us[i-1]
del(time_series_list_difference_us[0])
#print(time_series_list_difference)
#print(time_series_list_difference_us)

def manhattan(a,b):
    return sum(abs(a[i]-b[i]) for i in range(len(a)))

def euclidean(a, b):
    return math.sqrt(sum((a[i]-b[i])**2 for i in range(len(a))))

def sum_sqared_dist(a,b):
    return sum((a[i]-b[i])**2 for i in range(len(a)))


 # single linkage distance
def sld(cluster1, cluster2): 
    res = float('inf')
    # c1, c2 each is a country in the corresponding cluster
    for c1 in cluster1:
        for c2 in cluster2:
            dist = euclidean(d_dict[c1], d_dict[c2])
            if dist < res:
                res = dist
    return res

#complete linkage distance
def cld(cluster1, cluster2):
    res = -1
    for c1 in cluster1:
        for c2 in cluster2:
            dist = euclidean(d_dict[c1], d_dict[c2])
            if dist > res:
                res = dist
    return res

k = 8


# hierarchical clustering (sld, 'manhattan')
n = len(d_dict)
clusters = [{d} for d in d_dict.keys()]
for _ in range(n-k):
    dist = float('inf')
    best_pair = (None, None)
    for i in range(len(clusters)-1):
        for j in range(i+1, len(clusters)):
            if cld(clusters[i], clusters[j]) < dist:
                dist = cld(clusters[i], clusters[j])
                best_pair = (i,j)
    new_clu = clusters[best_pair[0]] | clusters[best_pair[1]]
    clusters = [clusters[i] for i in range(len(clusters)) if i not in best_pair]
    clusters.append(new_clu)
print(clusters)
q5 = ""
#for i in range(len(clusters)):
#    for item in clusters[i]:
#        q5 += str(i) + ","
for country in countries:
    for cluster in clusters:
        if country in cluster:
            q5 += str(clusters.index(cluster)) + ","
print(q5)
for cluster in clusters:
    print(*center(cluster), sep=',')

## k-means (manhattan)
import copy
def center(cluster):
    return np.average([d_dict[c] for c in cluster], axis=0)
init_num = np.random.choice(len(countries) - 1, k)
clusters = [{countries[i]} for i in init_num]
while True:
    new_clusters = [set() for _ in range(k)]
    centers = [center(cluster) for cluster in clusters]
    for c in countries:
        clu_ind = np.argmin([euclidean(d_dict[c], centers[i]) for i in range(k)])
        new_clusters[clu_ind].add(c)
    if all(new_clusters[i] == clusters[i] for i in range(k)):
        break
    else:
        clusters = copy.deepcopy(new_clusters)

q7 = ""
#for i in range(len(clusters)):
#    for item in clusters[i]:
#        q5 += str(i) + ","
for country in countries:
    for cluster in clusters:
        if country in cluster:
            q7 += str(clusters.index(cluster)) + ","
print(q7)
for cluster in clusters:
    print(*center(cluster), sep=',')
def distortion(cluster):
    cent = center(cluster)
    dis = 0
    for c in cluster:
        dis += sum_sqared_dist(cent, d_dict[c])
    return dis
total_distortion = 0
for cluster in clusters:
    total_distortion += distortion(cluster)
print(total_distortion)
