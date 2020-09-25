from random import randint
from random import shuffle


class Generator:
    opset = ['+', '-', '*', '/', '²', '√', 'sin', 'cos', 'tan']

    @staticmethod
    def generate(level):
        """
        docstring
        """
        generated = False
        while not generated:
            # 生成操作数序列以及二元运算符序列
            length = randint(1 if level == 0 else 0, 4)
            op2arr = [Generator.opset[randint(0, 3)] for i in range(length)]
            numarr = [randint(1, 100) for i in range(length + 1)]

            # 生成二元运算符的位置
            remain = 1
            position = []
            for i in range(length):
                position.append(randint(0, remain))
                remain += 1 - position[i]
            if remain > 1:
                position[-1] += remain - 1

            # 生成一元运算符序列
            op1arr = []
            if level == 1:
                op1arr.append(Generator.opset[randint(4, 5)])
            elif level == 2:
                op1arr.append(Generator.opset[randint(6, 8)])
            if level != 0:
                for i in range(randint(0, level)):
                    op1arr.append(Generator.opset[randint(4, 5 if level == 1 else 8)])
                shuffle(op1arr)

            # 生成后缀表达式
            expression = numarr.copy()
            offset = 2
            index = 0
            for i in range(length):
                for j in range(position[i]):
                    expression.insert(i + j + offset, op2arr[index])
                    index += 1
                offset += position[i]
            for op in op1arr:
                expression.insert(randint(1, len(expression)), op)

            # 返回生成的结果
            return expression


    @staticmethod
    def calculate(expression):
        """
        docstring
        """
        pass
