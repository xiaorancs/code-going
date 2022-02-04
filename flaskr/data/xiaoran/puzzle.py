# coding: utf-8

import random
import numpy as np
import copy
from heapq import heappop, heappush
from queue import Queue

class Board(object):
    def __init__(self, data, height=0, use_func='manhattan', next=None, prev=None):
        # self.n = n
        # self.random_list = [i for i in range(n*n)]
        # self.target_board = list(np.array(data).reshape(n, n))
        # random.shuffle(self.random_list)
        # self.board_data = list(np.array(data).reshape(n, n))
        # if isinstance(data, list) and len(data) == n:
        #     self.board_data = data
        self.board_data = data
        self.n = len(data)
        self.height = height
        self.random_list = [i for i in range(self.n * self.n)]
        self.random_list.remove(0)
        self.random_list.append(0)
        self.target_board = np.array(self.random_list).reshape(self.n, self.n)
        self.use_func = use_func
        self.next = next
        self.prev = prev

    # tile at (row, col) or 0 if blank
    def get(self, row, col):
        return self.board_data[row][col]

    # board size n
    def size(self):
        return self.n
    
    # 从val值，得到起在八数码中的正确的问题。
    def get_xy_from_value(self, val):
        idx = (val - 1) // self.n
        idy = (val - 1) - (idx * self.n)
        return idx, idy

    # number of tiles out of place
    def hamming(self):
        dist = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.board_data[i][j] != self.target_board[i][j] and self.target_board[i][j] != 0:
                    dist += 1
        # dist = self.n * self.n - np.sum(self.board_data == self.target_board)
        return dist

    # sum of Manhattan distances between current board and target board
    def manhattan(self):
        dist = 0
        for i in range(self.n):
            for j in range(self.n):
                val = self.board_data[i][j]
                idx, idy = self.get_xy_from_value(val)
                dist += abs(idx - i) + abs(idy - j)
        return dist
    
    # 启发式的得分 source 
    def get_score(self):
        if self.use_func == 'hamming':
            return self.height + self.hamming()
        return self.height + self.manhattan()

    # is this board the target board?
    def is_target(self):
        return np.sum(self.board_data == self.target_board) == self.n * self.n

    # does this board equal y?
    def equals(self, y):
        return self.board_data == y.board_data

    # 得到0的位置
    def get_zero_xy(self):
        idx = 0
        idy = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.board_data[i][j] == 0:
                    idx = i
                    idy = j
        return idx, idy

    # all neighboring boards
    def neighbors(self):
        all_neighbors = []
        idx, idy = self.get_zero_xy()
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        for i in range(4):
            cur_x = idx + dx[i]
            cur_y = idy + dy[i]
            if cur_x < 0 or cur_x >= self.n or cur_y < 0 or cur_y >= self.n:
                continue
            cur_board = copy.deepcopy(self.board_data)
            t = cur_board[cur_x][cur_y]
            cur_board[cur_x][cur_y] = cur_board[idx][idy]
            cur_board[idx][idy] = t
            all_neighbors.append(np.array(cur_board))
        return all_neighbors

    # is this board solvable?
    def is_solvable(self):
        return np.sum(self.board_data == self.target_board) == self.n * self.n

    def to_string(self):
        return "_".join(map(str, list(np.array(self.board_data).reshape(self.n*self.n))))

    def hash_code(self):
        hash_value = 0
        for i in range(self.n):
            for j in range(self.n):
                hash_value = hash_value * 10 + self.board_data[i][j]
        return hash_value
    
    # 定义比较方式
    def __cmp__(self, other):
        if self.get_score() > other.get_score():
            return -1
        elif self.get_score() == other.get_score():
            return 0
        else:
            return 1

    # 定义优先级的比较方式
    def __lt__(self, other):
        if self.get_score() < other.get_score():
            return True
        else:
            return False


class Solver(object):
    def __init__(self, board, use_algo="astar"):
        self.board = board
        self.ans_board = None
        self.iter = 100000
        # use_algo in ["bfs", "astar"]
        self.use_algo = use_algo

    # find a solution to the initial board (using the A* algorithm)
    def solver(self):
        visit_set = set([])
        iter = self.iter
        queue = []
        queue = []
        cur_board = self.board
        init_score = cur_board.get_score()
        print(cur_board.board_data)
        ans_board = None
        if self.use_algo == 'bfs':
            queue.append(cur_board)
        else:
            heappush(queue, cur_board)
        while len(queue) > 0 and iter > 0:
            iter -= 1
            if self.use_algo == 'bfs':
                top_board = queue[0]
                queue.remove(top_board)
            else:
                top_board = heappop(queue)
            if top_board.hash_code() in visit_set:
                continue            
            visit_set.add(top_board.hash_code())
            # print("top_board", top_board.board_data)
            # print("get_score", top_board.get_score())
            # print("top_board", top_board.to_string())
            if top_board.is_solvable():
                ans_board = top_board
                self.ans_board = ans_board
                break
            top_board_neighbors = top_board.neighbors()
            for t_data in top_board_neighbors:
                t_board = Board(t_data, height=top_board.height + 1, prev=top_board)
                if t_board.hash_code() in visit_set and init_score > t_board.get_score():
                    continue
                if self.use_algo == 'bfs':
                    queue.append(t_board)
                else:
                    heappush(queue, t_board)
        return ans_board

    # min number of moves to solve initial board
    def moves(self):
        return self.ans_board.height

    # sequence of boards in a shortest solution
    def solution(self):
        ans_list = []
        cur_board = self.ans_board
        if cur_board != None:
            ans_list.append(cur_board.board_data)
        while cur_board != None and cur_board.prev != None:
            cur_board = cur_board.prev
            ans_list.append(cur_board.board_data)
        ans_list.reverse()
        return ans_list

if __name__ == "__main__":
    n = 4
    random_list = [i for i in range(n*n)]
    random_list.remove(0)
    random_list.append(0)
    random_list = [0, 1, 3, 4, 2, 5, 7, 8, 6]
  
    random_list = [2,9,3,5,8,11,12,7,15,4,0,13,6,1,10,14]
    random_list = [7,8,1,10,2,4,5,13,0,9,3,6,11,14,15,12]
    random_list = [1,0 , 3, 2]
    random_list = [1,3,5,7,2,6,8,0,4]

    random_list = [1,6,2,4,5,0,3,8,9,10,7,11,13,14,15,12]

    n = 5
    random_list = [6,7,5,10,15,3,2,8,0,4,1,12,20,13,9,11,16,19,14,24,21,17,22,18,23]
    # random.shuffle(random_list)
    board_data = np.array(random_list).reshape(n, n)
    board = Board(board_data)

    # print(board.board_data)
    # print(board.neighbors())
    # print(board.target_board)
    # print(board.is_target())
    # print(board.is_solvable())

    solver = Solver(board)
    solver.solver()

    print(solver.moves())
    print(solver.solution())

