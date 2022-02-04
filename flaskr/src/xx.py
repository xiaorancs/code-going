# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:22:26 2021

@author: ·L
"""
import sys
import random
#判断系统是否是渗透的
class Percolation(object):
    """Percolation
    Args:
        n(int): 构造矩阵的大小，构造成 (n, n)；0表示关闭，1表示打开
    """
    def __init__(self, n):
        self.n = n
        self.grids=[[0]*n for _ in range(n)]
        self.open_count=0
        self.start=None
        self.end=None
        
    
    # 判断系统中(row, col)是否是打开状态
    def is_open(self, row, col):
        return self.grids[row][col]!=0

    # 打开(row, col)这个格子，状态从0变成1  
    def open(self, row, col):
        if self.grids[row][col]==0:
            self.open_count+=1
        self.grids[row][col]=1
    
    # 返回打开的格子数
    def number_of_open_sites(self):
        return self.open_count
    
    # 返回当前系统的状态，是nxn的矩阵
    def get_current_status(self):
        return self.grids

    # 可视化系统，将满足从上到下系统的格子，进行显示，
    # 你需要将满足从第一行就连通的格子的状态，从1变成2
    def show_percolates(self):
        dxdy=[[-1,0],[0,-1],[1,0],[0,1]]
        queue=[]
        for i in range(self.n):
            if self.grids[0][i]==1:
                queue.append((0,i))
        while queue: #深度优先遍历
            i,j=queue.popleft()
            self.grids[i][j]=2
            for dx,dy in dxdy:
                if self.grids[i+dx][j+dx]==1:
                    queue.append((i,j))
    
    # 返回true or false，表示当前系统是否是渗透的
    def percolates(self):
        return self.connected(self.start,self.end)
    
    # 运行模拟实验，每次打开一个格子，直到系统联通; 返回打开的格子个数
    def run(self):
        while True:
            row,col=random.randint(0, self.n-1),random.randint(0, self.n-1)
            while self.grids[row][col]!=0:
                row,col=random.randint(0, self.n-1),random.randint(0, self.n-1)
            self.grids[row][col]=1
            self.open_count+=1
            #合并
            self.union()
            if self.connected(self.start,self.end):#连通
                break
        return self.open_count
    def union(self,p,q):
    def find(self,p):
        
    def connected(self,p,q):
        rootp=self.find(p)
        rootq=self.find(q)
        return rootp==rootq
        

#蒙特卡洛实验模拟
class PercolationStats(object):
    def __init__(self, n, t):
        self.n = n 
        self.t = t
        pass

    # sample mean of percolation threshold
    # 渗透系统的阈值
    def mean(self):
        return 0.0

    # sample standard deviation of percolation threshold
    # T次实验渗透系统阈值对应的标准差
    def stddev(self):
        return 0.0

    # low endpoint of 95% confidence interval
    # 95置信区间的下届
    def confidenceLow(self):
        return 0.0

    # high endpoint of 95% confidence interval
    # 95置信区间的上届
    def confidenceHigh(self):
        return 0.0
    
    # 系统会默认调用这个函数进行评测，这个函数必须实现
    # 进行t次模拟实验，需要返回5元组
    # <mean(渗透阈值), std(方差), low_conf(置信区间下界), high_conf(置信区间上界), precolation_status(T次实验中随机一个可视化的状态，需要将能够从上到下渗透的格子从1标记成2)>
    def run(self):
        mean, std, low_conf, high_conf, precolation_status
        return (mean, std, low_conf, high_conf, precolation_status)

def test_Percolation():
    n = 5
    percolation = Percolation(n)
    number_of_open_sites = percolation.run()
    percolation_status = percolation.get_current_status()
    print("number_of_open_sites:%d, p:%f" % (number_of_open_sites, number_of_open_sites / (n*n)))
    print("percolation_status", percolation_status)
    
    n = 8
    percolation = Percolation(n)
    number_of_open_sites = percolation.run()
    percolation_status = percolation.get_current_status()
    print("number_of_open_sites:%d, p:%f" % (number_of_open_sites, number_of_open_sites / (n*n)))
    print("percolation_status", percolation_status)
# n = 5 output:
# number_of_open_sites:16, p:0.640000
# percolation_status: 
#     [[2, 2, 2, 0, 2], 
#      [0, 0, 2, 2, 0], 
#      [2, 2, 2, 2, 2], 
#      [2, 0, 2, 2, 2], 
#      [0, 0, 0, 0, 2]]

# n = 8 output:
# number_of_open_sites:42, p:0.656250
# percolation_status: 
#     [[2, 2, 0, 0, 2, 0, 2, 2], 
#      [2, 2, 2, 2, 0, 0, 2, 0], 
#      [0, 0, 2, 2, 2, 2, 0, 0], 
#      [1, 0, 2, 0, 0, 2, 2, 0], 
#      [2, 2, 2, 0, 0, 2, 0, 1], 
#      [0, 2, 2, 2, 2, 0, 1, 1], 
#      [2, 2, 2, 2, 0, 1, 1, 1], 
#      [0, 0, 2, 2, 2, 2, 2, 2]]
def test_PercolationStats():
    n = 10
    t = 20
    percolation_stats = PercolationStats(n, t)
    mean, stddev, confidenceLow, confidenceHigh, random_percolation_status = percolation_stats.run()
    print("mean:%f, stddev:%f, confidenceLow:%f, confidenceHigh:%f" % (mean, stddev, confidenceLow, confidenceHigh))
    print("random_percolation_status", random_percolation_status)
# output(n=10, t=20):
# mean:0.593, stddev:0.055, confidenceLow:0.109, confidenceHigh:0.157
# random_percolation_status: 
#     [[0, 2, 2, 0, 2, 0, 2, 2, 0, 2], 
#      [0, 2, 2, 2, 2, 2, 2, 0, 2, 2], 
#      [0, 2, 2, 2, 2, 2, 2, 2, 2, 0], 
#      [2, 2, 0, 2, 2, 2, 2, 0, 2, 2], 
#      [0, 2, 2, 2, 2, 2, 0, 0, 2, 2], 
#      [1, 0, 0, 2, 2, 2, 0, 1, 0, 2], 
#      [0, 1, 1, 0, 2, 0, 1, 0, 2, 2], 
#      [0, 0, 0, 0, 2, 2, 2, 2, 0, 0], 
#      [0, 0, 1, 1, 0, 0, 2, 0, 0, 1], 
#      [0, 0, 1, 0, 1, 0, 2, 0, 1, 0]]   
if __name__ == "__main__":
    n = 20
    t = 20
    if len(sys.argv) == 3:
        n = int(sys.argv[1])
        t = int(sys.argv[2])
    percolation_stats = PercolationStats(n, t)
    percolation_stats.run()
    



