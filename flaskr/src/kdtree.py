# coding: utf-8
import matplotlib.pyplot as plt
import copy
import time
import matplotlib
matplotlib.use('Agg')

class Point2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # x-coordinate 
    def x(self):
        return self.x

    # y-coordinate 
    def y(self):
        return self.y

    # square of Euclidean distance between two points 
    def distance_squared_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    # does this point equal that object? 
    def equals(self, target):
        return self.x == target.x and self.y == target.y

class RectHV(object):
    # construct the rectangle [xmin, xmax] x [ymin, ymax] 
    def __init__(self, xmin=0.0, ymin=0.0, xmax=1.0, ymax=1.0):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax


    # does this rectangle contain the point p (either inside or on boundary)? 
    def contains(self, p):
        return p.x >= self.xmin and p.x <= self.xmax and p.y >= self.ymin and p.y <= self.ymax

    # does this rectangle intersect that rectangle (at one or more points)? 
    # https://blog.csdn.net/szfhy/article/details/49740191/
    def intersects(self, other):
        zx = abs(self.xmin + self.xmax - other.xmin - other.xmax)
        x = abs(self.xmin - self.xmax) + abs(other.xmin - other.xmax)
        zy = abs(self.ymin + self.ymax - other.ymin - other.ymax)
        y = abs(self.ymin - self.ymax) + abs(other.ymin - other.ymax)
        return zx <= x and zy <= y
        return self.xmax >= other.xmin and self.ymax >= other.ymin and other.xmax >= self.xmin and other.ymax >= self.ymin

    # square of Euclidean distance from point p to closest point in rectangle 
    def distance_squared_to_point(self, p):
        up = abs(self.xmax - p.x)
        down = abs(self.xmin - p.x)
        left = abs(self.ymin - p.y)
        right = abs(self.ymax - p.y)
        if self.contains(p):
            return 0.0
        return min([up, down, left, right])

    # does this rectangle equal that object?     
    def equals(self, that):
        return self.xmin == that.xmin and self.xmax == that.xmax and self.ymin == that.ymin and self.ymax == that.ymax

class TreeNode(object):
    def __init__(self, point, rect, pivot_x=True):
        self.point = point
        self.rect = rect
        self.left = None
        self.right = None
        self.pivot_x = pivot_x

class KdTree(object):
    def __init__(self, file_name, k=10000):
        self.size = 0
        self.root = None
        self.xmin = 0.0
        self.ymin = 0.0
        self.xmax = 1.0
        self.ymax = 1.0
        self.file_name = file_name
        self.input_list_points = []
        self.ans = []
        self.k = k

    def create_dataset(self):
        input_list_points = []
        with open(self.file_name, "r") as f:
            for line in f.readlines():
                x, y = line.strip().split(" ")
                input_list_points.append(Point2D(x=float(x), y=float(y)))
        return input_list_points

    # construct kd tree
    def construct_kdtree(self):
        input_list_points = self.create_dataset()
        self.input_list_points = input_list_points[:self.k]
        for point in input_list_points[:self.k]:
            self.insert(point)

    def insert(self, point):
        if self.root is None:
            self.root = TreeNode(point=point, rect=RectHV(self.xmin, self.ymin, self.xmax, self.ymax), pivot_x=True)
        else:
            self.insert_util(self.root, point, RectHV())

    def insert_util(self, root, point, rect):
        if root is None:
            return
        # 节点已经存在返回
        if point.equals(root.point):
            return 
        
        # 根据当前使用的维度, 递归左右子树
        if root.pivot_x:
            if point.x < root.point.x:
                rect_temp = RectHV(rect.xmin, rect.ymin, root.point.x, rect.ymax)
                if root.left:
                    self.insert_util(root.left, point, rect_temp)
                else:
                    root.left = TreeNode(point, rect_temp, not root.pivot_x)
                    self.size += 1
            else:
                rect_temp = RectHV(root.point.x, rect.ymin, rect.xmax, rect.ymax)
                if root.right:
                    self.insert_util(root.right, point, rect_temp)                
                else:
                    root.right = TreeNode(point, rect_temp, not root.pivot_x)
                    self.size += 1
        else:
            if point.y < root.point.y:
                rect_temp = RectHV(rect.xmin, rect.ymin, rect.xmax, root.point.y)
                if root.left:
                    self.insert_util(root.left, point, rect_temp)
                else:
                    root.left = TreeNode(point, rect_temp, not root.pivot_x)
                    self.size += 1
            else:
                rect_temp = RectHV(rect.xmin, root.point.y, root.point.x, rect.ymax)
                if root.right:
                    self.insert_util(root.right, point, rect_temp)                
                else:
                    root.right = TreeNode(point, rect_temp, not root.pivot_x)
                    self.size += 1

    def range(self, rect, use_kd=True):
        root = self.root
        ans = []
        if use_kd:
            ans = self.range_util(root, rect)
        else:
            ans = self.range_bf(rect)
        res = [(d.x, d.y) for d in ans]
        res.sort()
        return res

    # 这个函数有个bug，会丢数
    def range_util(self, root, rect):  
        if root is None:
            return []
        ans = []
        left_ans = []
        right_ans = []
        if rect.intersects(root.rect):
            if rect.contains(root.point):
                ans = ans + [root.point]
                # self.ans.append(root.point)
            left_ans = self.range_util(root.left, rect)
            right_ans = self.range_util(root.right, rect)
            ans = left_ans + right_ans + ans
        return ans
    
    def range_bf(self, rect):
        ans = []
        for p in self.input_list_points:
            if rect.contains(p):
                ans.append(p)
        return ans

    # a nearest neighbor of point p; null if the symbol table is empty 
    # kd树搜搜竟然比暴力还慢
    def nearest(self, point, use_kd=True):
        current_node = self.root
        min_dist = [None]
        target=[0]
        search_path=[]

        if use_kd:
            start_time = time.time()
            min_dist, target = self.search(current_node, point)
            print("kd_ans", time.time()-start_time, min_dist, target.x, target.y)
        else:    
            start_time = time.time()
            min_dist, target = self.search_bf(point)
            print("bf_ans", time.time()-start_time, min_dist, target.x, target.y)
        return min_dist, target
            
    def search(self, root, point):
        if not root:
            return float('inf'), Point2D(0, 0)
        next_root = root.left
        if root.pivot_x:
            if point.x < root.point.x:
                next_root = root.left
            else:
                next_root = root.right
        else:
            if point.y < root.point.y:
                next_root = root.left
            else:
                next_root = root.right
        min_dist, target = self.search(next_root, point)
        cur_dist = point.distance_squared_to(root.point)
        if cur_dist < min_dist:
            min_dist = cur_dist
            target = root.point
        # 判断是够在矩形中保存，如果是，则进行另一个子树搜索
        if root.rect.distance_squared_to_point(point) <= min_dist:
            next_node = root.right
            if root.pivot_x:
                if point.x < root.point.x:
                    next_node = root.right
                else:
                    next_node = root.left
            else:
                if point.y < root.point.y:
                    next_node = root.right
                else:
                    next_node = root.left
            min_dist_t, target_t = self.search(root.right, point)
            if min_dist_t < min_dist:
                min_dist = min_dist_t
                target = target_t
        return min_dist, target

    def search_bf(self, point):
        min_dist = float("inf")
        target = None
        for p in self.input_list_points:
            if p.distance_squared_to(point) < min_dist:
                min_dist = p.distance_squared_to(point)
                target = p
        return min_dist, target

    def plot_fig(self, list_points, xmin, ymin, xmax, ymax, file_name):
        x = [d[0] for d in list_points]
        y = [d[1] for d in list_points]
        plt.cla()
        plt.scatter(x, y)
        # plt.vlines(x, ymin, ymax)
        # plt.hlines(y, xmin, xmax)
        plt.vlines(xmin, ymin, ymax, colors='red')
        plt.vlines(xmax, ymin, ymax, colors='red')
        plt.hlines(ymin, xmin, xmax, colors='red')
        plt.hlines(ymax, xmin, xmax, colors='red')
        plt.savefig(file_name)

if __name__ == "__main__":
    kd_tree = KdTree("input1M.txt")
    kd_tree.construct_kdtree()
    print(kd_tree.size)
    point = Point2D(0.103495, 0.172551)
    min_dist, target = kd_tree.nearest(point)
    print(target.x, target.y)
    res = kd_tree.range(rect=RectHV(0.1, 0.1, 0.2, 0.2))
    print(res[:10])

    kd_tree.plot_fig(res, 0.1, 0.1, 0.2, 0.2, "test.jpg")