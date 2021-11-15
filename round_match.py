# 算法课程 设计比赛日程表
# 每个选手必须与其他n - 1个选手各比赛一次

from numpy import *

def plan(n, table):
    if n == 2:
        table[0, 0] = 1
        table[0, 1] = 2
        table[1, 0] = 2
        table[1, 1] = 1
        return

    if n % 2 == 1:
        t = int((n+1)/2)
        n += 1
    else:
        t = int(n/2)
    plan(t, table)
    if n % 4 == 0:
        for i in range(int(n/2)):
            for j in range(int(n/2)):
                value = table[i][j]
                table[i+t][j] = value + t
                table[i][j+t] = value + t
                table[i+t][j+t] = value
    else:
        for i in range(int(n/2)):
            for j in range(int(n/2)+1):
                value = table[i][j]
                if value > t:
                    table[i+t][j] = i + 1
                    table[i][j] = i + t + 1
                    c = i + t + 2
                    k = int(n/2) + 1
                    while k < n:
                        if c > n:
                            c -= t
                        table[i][k] = c
                        table[c-1][k] = i + 1
                        c += 1
                        k += 1
                else:
                    table[i+t][j] = value + t
    return table

def main():
    a = int(input("请输入进行循环赛的人数:"))
    if a % 2 == 0:
        b = zeros([a, a])
        plan(a, b)
    else:
        b = zeros([a+1, a+1])
        plan(a+1,b)
        for i in range(a+1):
            for j in range(a+1):
                if b[i][j] > a:
                    b[i][j] = 0
                if i == a:
                    b[i][j] = 0
    print(b)

if __name__ == '__main__':
    main()
