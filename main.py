import datetime
import os
import re

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
            curTime = datetime.datetime.now()
            dirPath = '%s/data/%s' % (os.getcwd(), user.getUsername())
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            try:
                with open('%s/%s.txt' % (dirPath, curTime.strftime('%Y-%m-%d-%H-%M-%S')), 'w', encoding='utf-8') as f:
                    for i in range(1, num + 1):
                        f.write('%s: %s\n\n' % (i, Generator.generate(level)))
            except Exception as e:
                print('生成出错！')
                print(e)
            else:
                print('生成成功！')
