# coding: utf-8
# Author: xiaoran

import os
import sys
import random
import numpy as np

class UnionFind(object):
    """union find
    Args:
        n(int): 初始化的参数
    """
    def __init__(self, n):
        self.n = n
        self.data = [i for i in range(n)]
        self.parent = [i for i in range(n)]
        self.weight = [1 for i in range(n)]

    def union(self, p, q):
        self.parent_q = self.find(q)
        self.parent_p = self.find(p)
        if self.parent_p == self.parent_q:
            return
        # 小数据堆往大数据堆进行合并
        if self.weight[self.parent_q] < self.weight[self.parent_p]:
            self.parent[self.parent_q] = self.parent_p
            self.weight[self.parent_p] += self.weight[self.parent_q]
        else:
            self.parent[self.parent_p] = self.parent_q
            self.weight[self.parent_q] += self.weight[self.parent_p]

    def find(self, p):
        while (p != self.parent[p]):
            p = self.parent[p]
        return p

class Percolation(object):
    """Percolation
    Args:
        n(int): 构造矩阵的大小，构造成 (n, n)
    """
    def __init__(self, n):
        self.n = n
        self.open_site_counts = 0
        self.data = [[0 for i in range(n)] for _ in range(n)]
        self.top_union_find = UnionFind(n * n + 2)
        self.start = n * n 
        self.end = n * n + 1
        self.percolation_data = []

    def is_open(self, row, col):
        return self.data[row][col] != 0
    
    def open(self, row, col):
        if self.data[row][col] != 0:
            return
        self.data[row][col] = 1
        index = row * self.n + col
        if row == 0:
            self.top_union_find.union(self.start, index)
        if row == self.n - 1:
            self.top_union_find.union(self.end, index)
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        for i in range(len(dx)):
            x = row + dx[i]
            y = col + dy[i]
            if x < 0 or x >= self.n or y < 0 or y >= self.n:
                continue
            index_t = x * self.n + y
            if self.data[x][y] != 0:
                self.top_union_find.union(index, index_t)
        self.open_site_counts += 1

    def number_of_open_sites(self):
        return self.open_site_counts
    
    def get_current_status(self):
        return self.data

    # 得到从上到下的连通集合的下标
    def get_percolate_sits(self):
        return self.percolation_data

    # 可视化系统，并将一组可以从上到下的渗透系统可视化
    def show_percolates(self):
        for i in range(self.n):
            for j in range(self.n):
                if i == 0:
                    if self.data[i][j] != 0:
                        self.percolation_data.append((i, j))
                        self.data[i][j] = 2
                else:
                    # 判断上一个是不是连通，并左右试探所有连通
                    dx = [-1]
                    dy = [0]
                    ok = False
                    for di in range(len(dx)):
                        x = i + dx[di]
                        y = j + dy[di]
                        if x < 0 or y < 0 or y >= self.n:
                            continue
                        if self.data[x][y] == 2:
                            ok = True
                    if self.data[i][j] != 0 and ok:
                        k = j
                        while k < self.n and self.data[i][k] != 0:
                            self.percolation_data.append((i, k))
                            self.data[i][k] = 2
                            if i-1 > 0 and self.data[i-1][k] == 1:
                                self.data[i-1][k] = 2
                            k += 1
                        k = j-1
                        while k >= 0 and self.data[i][k] != 0:
                            self.percolation_data.append((i, k))
                            self.data[i][k] = 2
                            if i-1 > 0 and self.data[i-1][k] == 1:
                                self.data[i-1][k] = 2
                            k -= 1                        
    
    def percolates(self):
        percolation_status = self.top_union_find.find(self.start) == self.top_union_find.find(self.end)
        # 如果已经是渗透状态，得到当前一个渗透的状态
        if percolation_status:
            self.show_percolates()
        return percolation_status
    
    # 每次随机打开一个格子，直到系统联通; 返回打开的格子个数
    def run(self):
        while not self.percolates():
            x = random.randint(0, self.n-1)
            y = random.randint(0, self.n-1)
            self.open(x, y)
        return self.number_of_open_sites()


class PercolationStats(object):
    def __init__(self, n, t):
        self.n = n 
        self.t = t
        self.number_site_threshold = []

    # sample mean of percolation threshold
    def mean(self):
        return np.mean(np.array(self.number_site_threshold))

    # sample standard deviation of percolation threshold
    def stddev(self):
        return np.std(np.array(self.number_site_threshold))

    # low endpoint of 95% confidence interval
    def confidenceLow(self):
        return self.mean() - 1.96 * self.stddev() / np.sqrt(self.t)

    # high endpoint of 95% confidence interval
    def confidenceHigh(self):
        return self.mean() + 1.96 * self.stddev() / np.sqrt(self.t)

    def run(self):
        percolation_status = None
        for _ in range(self.t):
            percolation = Percolation(self.n)
            percolation.run()
            # while not percolation.percolates():
            #     x = random.randint(0, self.n-1)
            #     y = random.randint(0, self.n-1)
            #     percolation.open(x, y)
            percolation_status = percolation.get_current_status()
            self.number_site_threshold.append(percolation.number_of_open_sites() * 1.0 / (self.n * self.n))
        print("mean():", self.mean())
        print("stddev():", self.stddev())
        print("confidenceLow():", self.confidenceLow())
        print("confidenceHigh():", self.confidenceHigh())
        return self.mean(), self.stddev(), self.confidenceLow(), self.confidenceHigh(), percolation_status

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


def test_PercolationStats():
    n = 10
    t = 20
    percolation_stats = PercolationStats(n, t)
    mean, stddev, confidenceLow, confidenceHigh, random_percolation_status = percolation_stats.run()
    print("mean:%.3f, stddev:%.3f, confidenceLow:%.3f, confidenceHigh:%.3f" % (mean, stddev, confidenceLow, confidenceHigh))
    print("random_percolation_status", random_percolation_status)

if __name__ == "__main__":
    test_Percolation()
    test_PercolationStats()