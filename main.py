import re

from module.user import User
from module.generator import Generator

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

    while True:
        while not authenticated:
            row = input()
            # 只要求空格分隔，没有指定空格数目，也没有说明可以使用其余空白符隔开
            row = re.split(' +', row)
            if len(row) == 2:
                user = userSet.get(row[0])
                if user is not None:
                    usertype = user.Authenticate(row[0], row[1])
                    authenticated = usertype is not None
            if authenticated:
                print('当前选择为%s出题' % usertype)
            else:
                print('请输入正确的用户名、密码：')

        num = input('准备生成%s数学题目，请输入生成题目数量（输入-1将退出当前用户，重新登录）：' % usertype)
        while True:
            try:
                num = int(num)
            except Exception as e:
                num = input('请输入10-30以内的整数（包含10和30），输入-1将退出当前用户，重新登录：')
            else:
                break

        def getLevel(school):
            if school == '小学':
                return 0
            elif school == '中学':
                return 1
            elif school == '高中':
                return 2

        level = getLevel(usertype)

        for i in range(1, num + 1):
            print(Generator.generate(level))
