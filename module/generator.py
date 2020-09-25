from random import randint
from random import shuffle


class Generator:
    opset = ['+', '-', '*', '/', '²', '√', 'sin', 'cos', 'tan']

    @staticmethod
    def generate(level):
        """
        根据 level 生成指定等级的算术题
        0：小学；1：初中；2：高中
        """
        generated = False
        while not generated:
            """
            生成操作数序列以及二元运算符序列
            """
            length = randint(0 if level else 1, 4)
            op2Arr = [Generator.opset[randint(0, 3)] for i in range(length)]
            numArr = [randint(1, 100) for i in range(length + 1)]

            """
            生成二元运算符的位置
            """
            remain = 1
            position = []
            for i in range(length):
                position.append(randint(0, remain))
                remain += 1 - position[i]
            if remain > 1:
                position[-1] += remain - 1

            """
            生成一元运算符序列
            """
            op1Arr = []
            if level:
                if level == 1:
                    op1Arr.append(Generator.opset[randint(4, 5)])
                elif level == 2:
                    op1Arr.append(Generator.opset[randint(6, 8)])
                for i in range(randint(0, level)):
                    op1Arr.append(Generator.opset[randint(4, 5 if level == 1 else 8)])
                shuffle(op1Arr)

            """
            生成后缀表达式
            """
            expression = numArr
            offset = 2
            index = 0
            for i in range(length):
                for j in range(position[i]):
                    expression.insert(i + j + offset, op2Arr[index])
                    index += 1
                offset += position[i]
            for op in op1Arr:
                expression.insert(randint(1, len(expression)), op)

            def getPriority(item):
                """
                返回运算符或操作数的优先级
                操作数：0
                一元运算符：1
                '*'、'/'：2
                '+'、'-'：3
                """
                if isinstance(item, int):
                    return 0
                elif item == '+' or item == '-':
                    return 3
                elif item == '*' or item == '/':
                    return 2
                else:
                    return 1

            """
            转换成中缀表达式
            """
            expStack = []
            priStack = []
            for e in expression:
                priority = getPriority(e)
                if priority == 0:
                    """
                    是一个操作数，直接入栈
                    """
                    expStack.append(e)
                    priStack.append(0)
                elif priority == 3:
                    """
                    是加/减运算，优先级最低，拼接后直接入栈
                    """
                    item2 = expStack.pop()
                    priStack.pop()
                    item1 = expStack.pop()
                    priStack.pop()
                    expStack.append('%s%s%s' % (item1, e, item2))
                    priStack.append(3)
                elif priority == 2:
                    """
                    是乘/除运算，如果有加/减运算需要加括号
                    """
                    item2 = expStack.pop()
                    prio2 = priStack.pop()
                    if prio2 > 2:
                        item2 = '(%s)' % item2
                    item1 = expStack.pop()
                    prio1 = priStack.pop()
                    if prio1 > 2:
                        item1 = '(%s)' % item1
                    expStack.append('%s%s%s' % (item1, e, item2))
                    priStack.append(2)
                elif priority == 1:
                    """
                    是一元运算，除了操作数都要加括号
                    """
                    item = expStack.pop()
                    prio = priStack.pop()
                    if prio:
                        item = '(%s)' % item
                    if e == '²':
                        expStack.append('%s%s' % (item, '²'))
                    else:
                        expStack.append('%s%s' % (e, item))
                    priStack.append(1)

            return expStack[0]
