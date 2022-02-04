# coding: utf-8

import sys

class Node(object):
    def __init__(self, v):
        self.v = v
        self.adj = []

class Digraph(object):
    def __init__(self, V, input_list=None):
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.input_list = input_list
        if input_list:
            self.construct_digraph(input_list)

    # input_list = [(start_v, [v_1, v_2, ..., v_n]),]
    def construct_digraph(self, input_list=None):
        if not input_list:
            input_list = self.input_list
        for start_v, end_v_list in input_list:
            for end_v in end_v_list:
                self.add_edge(start_v, end_v)

    def add_edge(self, start_v, end_v):
        self.adj[start_v].append(end_v)
    
    # 得到v的邻居
    def get_adj(self, v):
        return self.adj[v]

    # 从v开始进行bfs, 并记录v的所有经过的路径
    def bfs(self, s):
        # 节点是否访问
        visited = [False for i in range(self.V)]
        # 从s到v的路径
        path_from_s = [-1 for i in range(self.V)]
        # 从s到v的距离
        dist_from_s = [sys.maxsize for i in range(self.V)]

        queue = []
        queue.append(s)
        visited[s] = True
        dist_from_s[s] = 0
        while len(queue) > 0:
            v = queue[0]
            queue.remove(v)
            for w in self.get_adj(v):
                if not visited[w]:
                    path_from_s[w] = v
                    dist_from_s[w] = dist_from_s[v] + 1
                    visited[w] = True
                    queue.append(w)
        return path_from_s, dist_from_s, visited

    def bfs_sets(self, s_sets):
        # 节点是否访问
        visited = [False for i in range(self.V)]
        # 从s到v的路径
        path_from_s = [-1 for i in range(self.V)]
        # 从s到v的距离
        dist_from_s = [sys.maxsize for i in range(self.V)]
        queue = []
        for s in s_sets:
            queue.append(s)
            visited[s] = True
            dist_from_s[s] = 0
        while len(queue) > 0:
            v = queue[0]
            queue.remove(v)
            for w in self.get_adj(v):
                if not visited[w]:
                    path_from_s[w] = v
                    dist_from_s[w] = min(dist_from_s[w], dist_from_s[v] + 1)
                    visited[w] = True
                    queue.append(w)
        return path_from_s, dist_from_s, visited

class ShortestCommonAncestor(object):
    # constructor takes a rooted DAG as argument
    def __init__(self, digraph):
        self.digraph = digraph

    def _ancestor_util(self, v, w, use_set=False):
        if not use_set:
            path_from_v, dist_from_v, visited_v = self.digraph.bfs(v)
            path_from_w, dist_from_w, visited_w = self.digraph.bfs(w)
        else:
            path_from_v, dist_from_v, visited_v = self.digraph.bfs_sets(v)
            path_from_w, dist_from_w, visited_w = self.digraph.bfs_sets(w)
        shortest_dist = float("inf")
        shortest_ancestor = -1
        for i in range(self.digraph.V):
            # 能够从v到达i, 而且能够从w到达i
            if visited_v[i] and visited_w[i] and dist_from_v[i] + dist_from_w[i] < shortest_dist:
                shortest_dist = dist_from_v[i] + dist_from_w[i]
                shortest_ancestor = i
        return shortest_dist, shortest_ancestor

    # length of shortest ancestral path between v and w
    def length(self, v, w):
        shortest_dist, _ = self._ancestor_util(v, w)
        return shortest_dist

    # a shortest common ancestor of vertices v and w
    def ancestor(self, v, w):
        _, shortest_ancestor = self._ancestor_util(v, w)
        return shortest_ancestor

    # length of shortest ancestral path of vertex subsets A and B
    def length_subset(self, subsetA, subsetB):
        shortest_dist, _ = self._ancestor_util(subsetA, subsetB, use_set=True)
        return shortest_dist

    # a shortest common ancestor of vertex subsets A and B
    def ancestor_subset(self, subsetA, subsetB):
        _, shortest_ancestor = self._ancestor_util(subsetA, subsetB, use_set=True)
        return shortest_ancestor


class WorkNet(object):
    # constructor takes the name of the two input files
    def __init__(self, synsets_file, hypernyms_file):
        print(synsets_file, hypernyms_file)
        self.synsets_file = synsets_file
        self.hypernyms_file = hypernyms_file
        self.nouns_2_id_map = {}
        self.id_2_nouns_map = {}
        self.hypernyms_input = []
        self.shortest_common_ancestor =None
        self.V = 0

    def read_synsets_file(self, synsets_file=None):
        if not synsets_file:
            synsets_file = self.synsets_file
        with open(synsets_file, 'r') as f:
            for line in f.readlines():
                line_split = line.strip().split(",")
                id, nouns_set = line_split[:2]
                nouns_set = nouns_set.split(" ")
                self.id_2_nouns_map[int(id)] = line_split[1]
                if "Airedale" in nouns_set:
                    print(line)
                for nouns in nouns_set:
                    if nouns not in self.nouns_2_id_map.keys():
                        self.nouns_2_id_map[nouns] = [int(id)]
                    else:
                        self.nouns_2_id_map[nouns].append(int(id))
                self.V += 1
        print(len(self.nouns_2_id_map))
        return self.nouns_2_id_map

    def read_hypernyms_file(self, hypernyms_file=None):
        v = 0
        e = 0
        if not hypernyms_file:
            hypernyms_file = self.hypernyms_file
        with open(hypernyms_file, "r") as f:
            for line in f.readlines():
                line_split = line.strip().split(",")
                id_v = int(line_split[0])
                id_ws = list(map(int, line_split[1:]))
                v += 1
                e += len(id_ws)
                self.hypernyms_input.append((id_v, id_ws))
        print(len(self.hypernyms_input), v, e)
        return self.hypernyms_input, v, e
    
    # 构造图
    def init_worknet(self):
        self.read_synsets_file()
        hypernyms_input, v, e = self.read_hypernyms_file()
        print("vvv", v, self.V)
        self.digraph = Digraph(self.V, hypernyms_input)
        self.shortest_common_ancestor = ShortestCommonAncestor(digraph=self.digraph)

    # all WordNet nouns
    def nouns(self):
        return list(self.nouns_2_id_map.keys())

    # is the word a WordNet noun?
    def is_noun(self, word):
        if word in self.nouns_2_id_map.keys():
            return True
        return False

    # a synset (second field of synsets.txt) that is a shortest common ancestor
    # of noun1 and noun2 (defined below)
    def sca(self, noun1, noun2):
        if not self.is_noun(noun1) or not self.is_noun(noun2):
            return -1
        id_noun1 = self.nouns_2_id_map[noun1]
        id_noun2 = self.nouns_2_id_map[noun2]
        ancestor_id = self.shortest_common_ancestor.ancestor_subset(id_noun1, id_noun2)
        ancestor = self.id_2_nouns_map[ancestor_id]
        print("ancestor", id_noun1, id_noun2, ancestor_id, ancestor)
        return ancestor_id, ancestor

    # distance between noun1 and noun2 (defined below)
    def distance(self, noun1, noun2):
        if not self.is_noun(noun1) or not self.is_noun(noun2):
            return -1
        id_noun1 = self.nouns_2_id_map[noun1]
        id_noun2 = self.nouns_2_id_map[noun2]
        dist = self.shortest_common_ancestor.length_subset(id_noun1, id_noun2)
        # print("distance", id_noun1, id_noun2, dist)
        return dist


class Outcast(object):
   # constructor takes a WordNet object
   def __init__(self, word_net):
       self.word_net = word_net

   # given an array of WordNet nouns, return an outcast
   def outcast(self, nouns):
        best_noun = None
        max_dist = 0
        for i in range(len(nouns)):
            cur_dist = 0
            for j in range(len(nouns)):
                dist = self.word_net.distance(nouns[i], nouns[j])
                cur_dist = cur_dist + dist
                # print("outcast i:%d, noun_i:%s, noun_j:%s, dist:%d" % (i, nouns[i], nouns[j], cur_dist))
            print("outcast i:%d, noun_i:%s, dist:%d" % (i, nouns[i], cur_dist))
            if cur_dist > max_dist:
                max_dist = cur_dist
                best_noun = nouns[i]
        return best_noun, max_dist

def test_spa():
    v = 12
    input_list = [[6, [3]], [7, [3]], [3, [1]], [4, [1]], [5, [1]], [8, [5]], 
                [9, [5]], [10, [9]], [11, [9]], [1, [0]], [2, [0]]]
    digraph = Digraph(v, input_list)
    print(digraph.get_adj(1))
    sca = ShortestCommonAncestor(digraph=digraph)
    print(sca._ancestor_util(3, 10))
    print(sca._ancestor_util(8, 11))
    print(sca._ancestor_util(6, 2))

def test_digraph():
    work_net = WorkNet(synsets_file="synsets.txt", hypernyms_file="hypernyms.txt")
    work_net.read_synsets_file()
    input_list, v, e = work_net.read_hypernyms_file()

    digraph = Digraph(v, input_list)
    print(digraph.get_adj(816))
    sca = ShortestCommonAncestor(digraph=digraph)
    print(sca._ancestor_util(3, 3))

    print(sca._ancestor_util([3,10], [3, 6], use_set=True))


def test_all():
    work_net = WorkNet(synsets_file="synsets.txt", hypernyms_file="hypernyms.txt")
    work_net.init_worknet()

    work_net.sca("Airedale", "Airedale_terrier")
    print("apple_potato_dist", work_net.distance("apple", "potato"))
    print("apple_apple_sca", work_net.sca("apple", "apple"))
    print("apple_apple_dist", work_net.distance("apple", "apple"))

    outcast = Outcast(word_net=work_net)
    nouns = ["horse", "zebra", "cat", "bear", "table"]
    print(outcast.outcast(nouns=nouns))
    nouns = ["water", "soda", "bed", "orange_juice", "milk", 'apple_juice', "tea", "coffee"]
    print(outcast.outcast(nouns=nouns))
    nouns = ["apple", "pear", "peach", "banana", "lime", "lemon", "blueberry", "strawberry", 'mango', "watermelon", "potato"]
    print(outcast.outcast(nouns=nouns))

if __name__ == "__main__":
    test_all()