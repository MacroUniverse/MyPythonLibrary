#!/usr/bin/python3
print('欢迎使用 my_module.py')

def plus1(num):
    return num + 1

num = 3.5
num2 = plus1(num)


if __name__ == '__main__':
    # 脚本模式下运行的命令
    print('正在被作为脚本执行,  __name__ 的值为 __main__')
else:
    # 作为模块导入时运行的命令
    print('正在被作为模块导入, __name__ 的值为', __name__)
