import os
import re
from datetime import datetime

from module.generator import Generator
from module.user import User

userSet = {
    '张三1': User('小学', '张三1', '123'),
    '张三2': User('小学', '张三2', '123'),
    '张三3': User('小学', '张三3', '123'),
    '李四1': User('初中', '李四1', '123'),
    '李四2': User('初中', '李四2', '123'),
    '李四3': User('初中', '李四3', '123'),
    '王五1': User('高中', '王五1', '123'),
    '王五2': User('高中', '王五2', '123'),
    '王五3': User('高中', '王五3', '123')
}

probSet = {
    '张三1': [False, None],
    '张三2': [False, None],
    '张三3': [False, None],
    '李四1': [False, None],
    '李四2': [False, None],
    '李四3': [False, None],
    '王五1': [False, None],
    '王五2': [False, None],
    '王五3': [False, None]
}

basePath = '%s/data' % os.getcwd()


def initSet(username):
    dirPath = '%s/%s' % (basePath, username)
    probs = set()

    if os.path.exists(dirPath):
        files = os.listdir(dirPath)

        def filterRule(e):
            if not isinstance(e, str):
                return False
            if not os.path.isfile('%s/%s' % (dirPath, e)) or not e.endswith('.txt'):
                return False
            filename = os.path.splitext(os.path.basename(e))[0]
            try:
                datetime.strptime(filename, '%Y-%m-%d-%H-%M-%S')
            except Exception as e:
                return False
            else:
                return True

        files = list(filter(filterRule, files))
        for filename in files:
            with open('%s/%s' % (dirPath, filename), 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line != '':
                        probs.add(re.sub(r'^\d+:\s+', '', line))

    return probs


if __name__ == "__main__":
    authenticated = False
    usertype = None
    user = None

    while True:
        if not authenticated:
            row = input('请输入用户名、密码：')
        while not authenticated:
            """
            用户登录验证
            """
            # 只要求空格分隔，没有指定空格数目，也没有说明可以使用其余空白符隔开
            row = re.split(' +', row)
            if len(row) == 2:
                user = userSet.get(row[0])
                if user is not None:
                    usertype = user.authenticate(row[0], row[1])
                    authenticated = usertype is not None
            if authenticated:
                print('当前选择为%s出题' % usertype)
            else:
                row = input('请输入正确的用户名、密码：')

        """
        试题数量选择
        """
        ready = 0
        while True:
            if ready == 0:
                num = input('准备生成%s数学题目，请输入生成题目数量（10-30以内的整数，输入0切换出题类型，输入-1将退出当前用户，重新登录）：' % usertype)
            elif ready == -1:
                num = input('请输入10-30以内的整数（包含10和30），输入0切换出题类型，输入-1将退出当前用户，重新登录：')

            try:
                num = int(num)
            except Exception as e:
                ready = -1
            else:
                if num == -1:
                    authenticated = False
                    break
                if num == 0:
                    tmp = input('请输入“切换为小学/初中/高中”：')
                    while True:
                        if tmp == '切换为小学':
                            usertype = '小学'
                            break
                        elif tmp == '切换为初中':
                            usertype = '初中'
                            break
                        elif tmp == '切换为高中':
                            usertype = '高中'
                            break
                        else:
                            tmp = input('请输入小学、初中和高中三个选项中的一个：')
                    user.setType(usertype)
                    print('已成功切换为%s！' % usertype)
                    ready = 0
                elif num < 10 or num > 30:
                    ready = -1
                else:
                    break

        if authenticated:
            """
            生成并输出
            """

            def getLevel(school):
                if school == '小学':
                    return 0
                elif school == '初中':
                    return 1
                elif school == '高中':
                    return 2

            level = getLevel(usertype)
            curTime = datetime.now()
            dirPath = '%s/%s' % (basePath, user.getUsername())
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            try:
                """
                如果未初始化，则初始化试题集合
                """
                cell = probSet.get(user.getUsername())
                if not cell[0]:
                    cell[1] = initSet(user.getUsername())

                """
                生成试题并添加进集合
                """
                with open('%s/%s.txt' % (dirPath, curTime.strftime('%Y-%m-%d-%H-%M-%S')), 'w', encoding='utf-8') as f:
                    for i in range(1, num + 1):
                        while True:
                            prob = Generator.generate(level)
                            if prob not in cell[1]:
                                cell[1].add(prob)
                                f.write('%s: %s\n\n' % (i, prob))
                                break
                            else:
                                print('发现重复，准备重新生成：', prob)
            except Exception as e:
                print('生成出错！')
                print(e)
            else:
                print('生成成功！')
