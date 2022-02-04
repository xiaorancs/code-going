# coding: utf-8
# Author: xiaoran

class Calculator(object):
    def __init__(self):
        self.priori_op = {
            '+': {'+':-1, '-':-1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1},
            '-': {'+':-1, '-':-1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1},
            '*': {'+':1, '-':1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1},
            '/': {'+':1, '-':1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1},
            '√': {'+':1, '-':1, '*':1, '/':1, '√':-1, '(':1, ')':-1},
            '(': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':0},
            ')': {'+':-1, '-':-1, '*':-1, '/':-1, '√':-1, '(':0, ')':-1},
        }

    # 格式化输入的计算表达式: 1.去除空格; 2.'-'号补0占位
    def format_input(self, ori_input):
        input = ori_input.replace(" ", "")
        sub_input = input.split("-")
        # print(sub_input)
        for i in range(1, len(sub_input)):
            # print("hah", i-1, sub_input[i-1])
            if sub_input[i-1] == "" or (not self.is_digit(sub_input[i-1][-1]) and sub_input[i-1][-1] not in ('!', ')')) :
                sub_input[i-1] += "0"
        return "-".join(sub_input)
    
    def is_digit(self, c):
        if c in "0123456789.e":
            return True
        return False

    def get_ans(self, op, a, b):
        ans = 0
        if op == '+':
            ans = a + b
        elif op == '-':
            ans = a - b
        elif op == '*':
            ans = a * b
        elif op == '/':
            ans = a / b
        return ans

    def solver(self, input):
        # print("input", input)
        input = self.format_input(input)
        print("input", input)
        stack_num = []
        stack_op = []
        num_str = ""
        for c in input:
            if c in self.priori_op.keys():
                # print(c, stack_num, stack_op, num_str)
                if len(num_str) > 0:
                    num = int(num_str)
                    stack_num.append(num)
                    num_str = ""
                # 判断当前op和stack_op栈顶元素的优先级,当前op < 栈顶op
                while len(stack_op) > 0 and self.priori_op[c][stack_op[-1]] == -1:
                    top = stack_op[-1]
                    if top == '√':
                        num = stack_num.pop()
                        stack_num.append(num**0.5)
                        stack_op.pop()
                    else:
                        num1 = stack_num.pop()
                        num2 = stack_num.pop()
                        ans = self.get_ans(top, num2, num1)
                        stack_num.append(ans)
                        stack_op.pop()
                if c == ')' and stack_op[-1] == '(':
                    stack_op.pop()
                else:
                    stack_op.append(c)
            else:
                num_str = num_str + c
        if len(num_str) > 0:
            num = int(num_str)
            stack_num.append(num)
        # print(stack_op)
        # print(stack_num)
        while len(stack_op) > 0:
            if stack_op[-1] == '√':
                num = stack_num.pop()
                stack_num.append(num**0.5)
                stack_op.pop()
            else:
                num1 = stack_num.pop()
                num2 = stack_num.pop()
                op = stack_op.pop()
                # print(num1, num2, op)
                ans = self.get_ans(op, num2, num1)
                stack_num.append(ans)
        # print("output", stack_num)
        return stack_num[0]


def test_Calculator():
    input = "2+3*4"
    calculator = Calculator()
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "(2+3)*4"
    ans=calculator.solver(input=input)
    print("%s=%s" % (input, ans))


    input = "(2+3)*4+√9*(1/2+((1+1)*2))"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))
    input = "-2+(-3)*5"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))
    input = "(2-1*2+14/2)+√9"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "(2-1*2+14/2)+√9+(-2)"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))

    input = "(2-1*2+14/2)+√9+(-2)-2"
    ans = calculator.solver(input=input)
    print("%s=%s" % (input, ans))


if __name__ == "__main__":
    test_Calculator()