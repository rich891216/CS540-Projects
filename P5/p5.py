import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
# %matplotlib inline
import copy
import math
import heapq

'''
The below script is based on a 55 * 57 maze. 
Todo:
	1. Plot the maze and solution in the required format.
	2. Implement DFS algorithm. (I've given you the BFS below)
	3. Implement A* with Euclidean distance. (I've given you the one with Manhattan distance)

'''



width, height = 57, 58
X, Y = 14, 2

solution = mpimg.imread('solution.png')
ori_img = mpimg.imread('richard.png')
img = ori_img[:,:,0]
solution = solution[:,:,0]
class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.succ = ''
        self.action = ''  # which action the parent takes to get this cell
cells = [[Cell(i,j) for j in range(width)] for i in range(height)]


 
maze_w = 57
maze_h = 58
 
wall = 2
hall = 14
 
#img[y][x]
#....x
#.
#y
 
x = 0
y = 0
 
output = ""
 
try:
    while True:
        while True:
            if img[y][x] == 0:
                output += "+"
            else:
                output += " "
 
            x += wall
 
            if x >= (wall+hall)*maze_w + wall:
                output += "\n"
                break
 
            if img[y][x] == 0:
                output += "--"
            else:
                output += "  "
 
            x += hall
       
        y += wall
        x = 0
 
        if y >= (wall+hall)*maze_h + wall:
            break
       
        while True:
            if img[y][x] == 0:
                output += "|  "
            else:
                output += "   "
 
            x += wall + hall
 
            if x >= (wall+hall)*maze_w + wall:
                output += "\n"
                break
 
        y += hall
        x = 0
 
       
        if y >= (wall+hall)*maze_h + wall:
            break
except Exception as e:
    print(output)
    raise e
 
print(output)



for i in range(height):
    succ = []
    for j in range(width):
        s = ''
        c1, c2 = i * 16 + 8, j * 16 + 8
        if img[c1-8, c2] == 1: s += 'U'
        if img[c1+8, c2] == 1: s += 'D'
        if img[c1, c2-8] == 1: s += 'L'
        if img[c1, c2+8] == 1: s += 'R'
        cells[i][j].succ = s
        succ.append(s)
    print(*succ, sep=',')
# 2    


cells[0][28].succ = cells[0][28].succ.replace('U', '')
cells[54][28].succ = cells[54][28].succ.replace('D', '')

# bfs
visited = set()
s1 = {(0,28)}
s2 = set()
while (56,28) not in visited:
    for a in s1:
        visited.add(a)
        i, j = a[0], a[1]
        succ = cells[i][j].succ
        if 'U' in succ and (i-1,j) not in (s1 | s2 | visited): 
            s2.add((i-1,j))
            cells[i-1][j].action = 'U'
        if 'D' in succ and (i+1,j) not in (s1 | s2 | visited): 
            s2.add((i+1,j))
            cells[i+1][j].action = 'D'
        if 'L' in succ and (i,j-1) not in (s1 | s2 | visited): 
            s2.add((i,j-1))
            cells[i][j-1].action = 'L'
        if 'R' in succ and (i,j+1) not in (s1 | s2 | visited): 
            s2.add((i,j+1))
            cells[i][j+1].action = 'R'     
    s1 = s2
    s2 = set()
    
cur = (56,28)
s = ''
seq = []
while cur != (0,28):
    seq.append(cur)
    i, j = cur[0], cur[1]
    t = cells[i][j].action
    s += t
    if t == 'U': cur = (i+1, j)
    if t == 'D': cur = (i-1, j)
    if t == 'L': cur = (i, j+1)
    if t == 'R': cur = (i, j-1)
action = s[::-1]
seq = seq[::-1]
print(action)
# 3 
q5 = ""
for i in range(height):
    for j in range(width):
        if (i,j) in visited:
            q5 += "1,"
        else:
            q5 += "0,"
    q5 += "\n"
print(q5)

#dfs
visited = set()
cur = (0,28)
s1 = []
s2 = set()
while (56,28) not in visited:
    visited.add(cur)
    i,j = cur[0], cur[1]
    succ = cells[i][j].succ
    if 'U' in succ and (i-1, j) not in visited:
        visited.add(cur)
        s1.append(cur)
        cur = (i-1, j)
        continue
    if 'D' in succ and (i+1, j) not in (visited):
        visited.add(cur)
        s1.append(cur)
        cur = (i+1, j)
        continue
    if 'L' in succ and (i, j-1) not in visited:
        visited.add(cur)
        s1.append(cur)
        cur = (i, j-1)
        continue
    if 'R' in succ and (i, j+1) not in visited:
        visited.add(cur)
        s1.append(cur)
        cur = (i, j+1)
        continue
    else:
        cur = s1[-1]
        s1.pop(-1)

q6 = ""
for i in range(height):
    for j in range(width):
        if (i,j) in visited:
            q6 += "1,"
        else:
            q6 += "0,"
    q6 += "\n"
print("Q6: ", q6)


## Part2
man = {(i,j): abs(i-56) + abs(j-28) for j in range(width) for i in range(height)}
q7 = ""
for i in range(height):
    for j in range(width):
        q7 += str(man[(i,j)])+","
    q7 += "\n"
#print(q7)
euc = {(i,j): math.sqrt((i-54)**2 + (j-28)**2 ) for j in range(width) for i in range(height)}

# manhattan   use man
g = {(i,j): float('inf') for j in range(width) for i in range(height)}
g[(0,28)] = 0

queue = [(0,28)]
visited = set()

while queue and (56,28) not in visited:
    queue.sort(key=lambda x: g[x] + euc[x])
    point = queue.pop(0)
    if point not in visited:
        visited.add(point)
        i, j = point[0], point[1]
        succ = cells[i][j].succ
        if 'U' in succ and (i-1,j) not in visited:
            if (i-1,j) not in queue: queue += [(i-1,j)]
            g[(i-1,j)] = min(g[(i-1,j)], g[(i,j)]+1)
        if 'D' in succ and (i+1,j) not in visited:
            if (i+1,j) not in queue: queue += [(i+1,j)]
            g[(i+1,j)] = min(g[(i+1,j)], g[(i,j)]+1)
        if 'L' in succ and (i,j-1) not in visited:
            if (i,j-1) not in queue: queue += [(i,j-1)]
            g[(i,j-1)] = min(g[(i,j-1)], g[(i,j)]+1)
        if 'R' in succ and (i,j+1) not in visited:
            if (i,j+1) not in queue: queue += [(i,j+1)]
            g[(i,j+1)] = min(g[(i,j+1)], g[(i,j)]+1)     
q8 = ""
for i in range(height):
    for j in range(width):
        if (i,j) in visited:
            q8 += "1,"
        else:
            q8 += "0,"
    q8 += "\n"
print(q8)