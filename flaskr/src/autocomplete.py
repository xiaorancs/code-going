# coding: utf-8

from heapq import heappop, heappush

class TreeNode(object):
    def __init__(self):
        self.child_node = {}
        self.is_leaf = False
        self.content = ""
        self.weight = 0
        self.count = 0

    def insert(self, word, weight):
        current = self
        for c in word:
            if c not in current.child_node:
                new_node = TreeNode()
                current.child_node[c] = new_node
            current = current.child_node[c]
        current.is_leaf = True
        current.content = word
        current.weight = weight
        self.count += 1

    def construct_tree(self, input_list):
        for word, weight in input_list:
            self.insert(word, weight)

    def search_prefix(self, prefix, desc=True):
        current = self
        for c in prefix:
            if c in current.child_node:
                current = current.child_node[c]
        # 得到这个前缀下所有单次
        ans = []
        queue = []
        queue.append(current)
        while len(queue) > 0:
            top = queue[0]
            if top.is_leaf:
                ans.append((top.content, top.weight))
            queue.remove(top)
            for c in top.child_node.keys():
                queue.append(top.child_node[c])
        if desc:
            ans = sorted(ans, key=lambda x: x[1], reverse=True)
        return ans

class Autocomplete(object):
    """Autocomplete
    
    input_list = [(str, weight), (str, weight)]
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.list_item = None
        self.tree = TreeNode()

    def create_input_items(self):
        list_item = []
        with open(self.file_name, "r") as f:
            for line in f.readlines():
                line_split = line.strip().split("\t")
                if len(line_split) == 1:
                    continue
                w, s = line_split
                w = int(w)
                list_item.append((s, w))
        self.list_item = list_item
        return list_item

    def create_dict_tree(self):
        list_item = self.create_input_items()
        print(len(list_item))
        self.tree.construct_tree(list_item)

    # Returns all terms that start with the given prefix, in descending order of weight.
    def all_atches(self, prefix):
        pass

    # Returns the number of terms that start with the given prefix.
    def number_of_matches(prefix):
        pass


if __name__ == "__main__":
    autocomplete = Autocomplete("/Users/xiaoran/Github/ranxue/cos226_web/flaskr/static/wiktionary.txt")
    autocomplete.create_dict_tree()
    ans = autocomplete.tree.search_prefix("the")
    print(ans)