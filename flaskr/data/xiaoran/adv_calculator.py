# coding: utf-8
# Author: xiaoran

import math

class AdvCalculator(object):
    def __init__(self):
        self.priori_op = {
            '+': {'+':-1, '-':-1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1, '!':-1, '^':-1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            '-': {'+':-1, '-':-1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1, '!':-1, '^':-1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            '*': {'+':1, '-':1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1, '!':-1, '^':-1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            '/': {'+':1, '-':1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1, '!':-1, '^':-1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            '√': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':-1, '!':-1, '^':-1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            '(': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':0, '!':-1, '^':1, 'ln':1, 'log':1, 'sin':1, 'cos':1, 'tan':1, 'arcsin':1, 'arccos':1, 'arctan':1},
            ')': {'+':-1, '-':-1, '*':-1, '/':-1, '√':-1, '(':0, ')':-1, '!':-1, '^':-1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            '!': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':-1, '!':1, '^':1, 'ln':1, 'log':1, 'sin':1, 'cos':1, 'tan':1, 'arcsin':1, 'arccos':1, 'arctan':1},
            '^': {'+':1, '-':1, '*':1, '/':1, '√':-1, '(':1, ')':-1, '!':-1, '^':1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            'ln': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':-1, '!':-1, '^':1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            'log': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':-1, '!':-1, '^':1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            'sin': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':-1, '!':-1, '^':1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            'cos': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':-1, '!':-1, '^':1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            'tan': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':-1, '!':-1, '^':1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            'arcsin': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':-1, '!':-1, '^':1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            'arccos': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':-1, '!':-1, '^':1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
            'arctan': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':-1, '!':-1, '^':1, 'ln':-1, 'log':-1, 'sin':-1, 'cos':-1, 'tan':-1, 'arcsin':-1, 'arccos':-1, 'arctan':-1},
        }
        self.all_op = self.priori_op.keys()
        self.unary_op = ['√', '!', 'ln', 'log', 'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan']
        self.binary_op = ['+', '-', '*', '/', '^']

    # 格式化输入的计算表达式: 1.去除空格; 2.'-'号补0占位
    def format_input(self, ori_input):
        input = ori_input.replace(" ", "")
        sub_input = input.split("-")
        for i in range(1, len(sub_input)):
            if sub_input[i-1] == "" or (not self.is_digit(sub_input[i-1][-1]) and sub_input[i-1][-1] not in ('!', ')')):
                sub_input[i-1] += "0"
        return "-".join(sub_input)

    def get_ans_tow(self, op, a, b):
        ans = 0
        if op == '+':
            ans = a + b
        elif op == '-':
            ans = a - b
        elif op == '*':
            ans = a * b
        elif op == '/':
            ans = a / b;
        elif op == '^':
            ans = a ** b    
        return ans
    
    def angle2radian(self, num):
        return num / 180 * math.pi

    def radian2angle(self, num):
        return num / math.pi * 180

    def get_ans_one(self, op, num):
        ans = 0
        if op == '√':
            ans = num ** 0.5
        elif op == '!':
            num = int(num)
            s = 1
            for i in range(1, num+1):
                s = s * i
            ans = s
        elif op == 'ln':
            ans = math.log(num)   
        elif op == 'log':
            ans = math.log2(num)
        # 默认输入输出都是角度
        elif op == 'sin':
            # print(num, self.angle2radian(num))
            ans = math.sin(self.angle2radian(num))
        elif op == 'cos':
            ans = math.cos(self.angle2radian(num))
        elif op == 'tan':
            ans = math.tan(self.angle2radian(num))
        elif op == 'arcsin':
            ans = math.asin(num)
            ans = self.radian2angle(ans)
        elif op == 'arccos':
            ans = math.acos(num)
            ans = self.radian2angle(ans)
        elif op == 'arctan':
            ans = math.atan(num)
            ans = self.radian2angle(ans)
        return ans

    def is_digit(self, c):
        if c in "0123456789.e":
            return True
        return False

    def solver(self, input):
        input = self.format_input(input)
        # print("format_input", input)
        stack_num = []
        stack_op = []
        num_str = ""
        op_str = ""
        flag = 1
        for i, c in enumerate(input):
            if not self.is_digit(c):
                op_str += c
                if op_str in self.all_op:
                    if len(num_str) > 0:
                        if num_str == 'e':
                            num = math.e
                        else:
                            num = float(num_str)
                        # print("num_1", num)
                        stack_num.append(num)
                        num_str = ""
                    # 判断当前op和stack_op栈顶元素的优先级,当前op < 栈顶op
                    while len(stack_op) > 0 and self.priori_op[op_str][stack_op[-1]] == -1:
                        top = stack_op[-1]
                        if top in self.unary_op:
                            num = stack_num.pop()
                            ans = self.get_ans_one(top, num)
                            stack_num.append(ans)
                            stack_op.pop()
                        else:
                            num1 = stack_num.pop()
                            num2 = stack_num.pop()
                            ans = self.get_ans_tow(top, num2, num1)
                            stack_num.append(ans)
                            stack_op.pop()
                    if op_str == ')' and stack_op[-1] == '(':
                        stack_op.pop()
                    else:
                        stack_op.append(op_str)
                    op_str = ""
            else:
                num_str = num_str + c
        if len(num_str) > 0:
            if num_str == 'e':
                num = math.e
            else:
                num = float(num_str)
            stack_num.append(num)

        while len(stack_op) > 0:
            if stack_op[-1] in self.unary_op:
                num = stack_num.pop()
                ans = self.get_ans_one(stack_op[-1], num)
                stack_num.append(ans)
                stack_op.pop()
            else:
                num1 = stack_num.pop()
                num2 = stack_num.pop()
                op = stack_op.pop()
                ans = self.get_ans_tow(op, num2, num1)
                stack_num.append(ans)
        return stack_num[0]

def test_Calculator():
    input = "2+3*4"
    calculator = AdvCalculator()
    # ans = calculator.solver(input=input)
    # print('ans', ans)
    input = "(2+3)*4"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "(2+3)*4+√9*(1/2+((1+1)*2))"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "(2+3)*4+√9"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "sin(2^6+26)"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "2^6"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "2+arcsin(log(2.0))+5+2^(2)+(-log(2))"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "2^log(8)"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "2^(-1)"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "-2*3*2^(-1)+2^2^3+3!"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "8^1-5!+10"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "(5!-8^(1/2))*e"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "(2-1*2+14/2)+√9"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "4^(-1/2)"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "ln(e*e)"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "ln(e*e)-2"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

if __name__ == "__main__":
    test_Calculator()