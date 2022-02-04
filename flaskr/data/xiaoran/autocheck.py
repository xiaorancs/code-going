# coding: utf-8
# 词典来自: https://github.com/mahavivo/english-wordlists/edit/master/CET4+6_edited.txt

import numpy as np

class AutoCheck(object):
    def __init__(self, word_file='words.txt'):
        self.word_file = word_file
        self.word_list = self.read_words(word_file=word_file)
        print(len(self.word_list))
    
    def read_words(self, word_file):
        word_list = []
        with open(word_file, 'r') as f:
            for word in f.readlines():
                word_list.append(word.strip())
        return word_list

    def jaccard_sim(self, str_a ,str_b):
        '''
        Jaccard相似性系数
        计算sa和sb的相似度 len（sa & sb）/ len（sa | sb）
        '''
        seta = set(str_a)
        setb = set(str_b)
        sa_sb = 1.0 * len(seta & setb) / len(seta | setb)
        return sa_sb

    def cos_sim(self, str_a, str_b):
        seta = set(str_a)
        setb = set(str_b)
        all_chars = seta | setb
        cnt_a = {}
        cnt_b = {}
        for c in str_a:
            if c not in cnt_a:
                cnt_a[c] = 0
            cnt_a[c] += 1

        for c in str_b:
            if c not in cnt_b:
                cnt_b[c] = 0
            cnt_b[c] += 1

        a = []
        b = []
        for c in all_chars:
            k = 0
            if c in cnt_a.keys():
                k = cnt_a[c]
            a.append(k)
            k = 0
            if c in cnt_b.keys():
                k = cnt_b[c]
            b.append(k)

        a = np.array(a)
        b = np.array(b)
        #return {"文本的余弦相似度:":np.sum(a*b) / (np.sqrt(np.sum(a ** 2)) * np.sqrt(np.sum(b ** 2)))}
        return np.sum(a*b) / (np.sqrt(np.sum(a ** 2)) * np.sqrt(np.sum(b ** 2)))

    def min_edit_distance(self, str_a, str_b):
        '''
        最小编辑距离，只有三种操作方式 替换、插入、删除
        '''
        lensum = float(len(str_a) + len(str_b))
        if len(str_a) > len(str_b): #得到最短长度的字符串
            str_a,str_b = str_b,str_a
        distances = range(len(str_a) + 1) #设置默认值
        for index2,char2 in enumerate(str_b): #str_b > str_a
            newDistances = [index2+1] #设置新的距离，用来标记
            for index1,char1 in enumerate(str_a):
                if char1 == char2: #如果相等，证明在下标index1出不用进行操作变换，最小距离跟前一个保持不变，
                    newDistances.append(distances[index1])
                else: #得到最小的变化数，
                    newDistances.append(1 + min((distances[index1],   #删除
                                                 distances[index1+1], #插入
                                                 newDistances[-1])))  #变换
            distances = newDistances #更新最小编辑距离
        mindist = distances[-1]
        ratio = (lensum - mindist)/lensum
        #return {'distance':mindist, 'ratio':ratio}
        return ratio

    # https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
    def levenshtein_distance(self, str1, str2, damerau=True):
        '''
        编辑距离——莱文斯坦距离,计算文本的相似度
        '''
        m = len(str1)
        n = len(str2)
        lensum = float(m + n)
        d = [ [0 for _ in range(n+1)] for _ in range(m+1)]           
        for i in range(m+1):
            d[i][0] = 0
        for j in range(n+1):
            d[0][j] = 0
        for i in range(1, m):
            for j in range(1, n):
                cost = 0
                if str1[i-1] == str2[j-1]:
                    cost = 0          
                else:
                    cost = 1
                d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+cost)        
                if damerau:  
                    if i > 1 and j > 1 and str1[i] == str2[j-1] and str1[i-1] == str2[j]:
                        d[i][j] = min(d[i][j], d[i-2][j-2]+1)

        ldist = d[-1][-1]
        ratio = (lensum - ldist) / lensum
        #return {'distance':ldist, 'ratio':ratio}
        return ratio


    # query值包含空格，使用空格分隔
    def auto_check(self, ori_query):
        # print(ori_query)
        query_list = ori_query.split(" ")
        hint_query = ""
        for i, query in enumerate(query_list):
            check_word = ""
            ratio = 0.0
            for word in self.word_list:
                if ratio < self.levenshtein_distance(query, word):
                    check_word = word
                    ratio = self.levenshtein_distance(query, word)
                # 如果相等，进一步判断cos_sim
                elif ratio == self.levenshtein_distance(query, word):
                    cos_sim_1 = self.cos_sim(query, word)
                    cos_sim_2 = self.cos_sim(query, check_word)
                    # print(query, check_word, word, cos_sim_1, cos_sim_2)
                    if cos_sim_1 > cos_sim_2:
                        check_word = word
            if i == 0:
                hint_query += check_word
            else:
                hint_query += " " + check_word
            # print(query, check_word, i)
        print("ori_query", ori_query)
        print("hint_query", hint_query)
        return hint_query


def test_AutoCheck():
    auto_check = AutoCheck(word_file="./static/autocheck/words.txt")

    # print(auto_check.cos_sim("chcek", "check"))
    # print(auto_check.cos_sim("chcek", "cheek"))
    # print(auto_check.min_edit_distance("chcek", "check"))
    # print(auto_check.min_edit_distance("chcek", "cheek"))

    query = "tests"
    auto_check.auto_check(ori_query=query)

if __name__ == "__main__":
    test_AutoCheck()