# #算法课程，关于棋盘覆盖问题，采用分治法处理
# i=0 #填写L型方块的编号
# def chessboard(x, y, bx, by, size):
#     if size == 1:
#         return
#     s=size/2
#     global i
#     i += 1
#     if bx < x+s and by < y+s:
#         chessboard(x, y, bx, by, s)
#     else:
#         chess[int(x+s-1)][int(y+s-1)] = i
#         chessboard(x, y, x+s-1, y+s-1, s)
#
#     if bx < x+s and by >= y+s:
#         chessboard(x, y+s, bx, by, s)
#     else:
#         chess[int(x+s-1)][int(y+s)] = i
#         chessboard(x, y+s, x+s-1, y+s, s)
#
#     if bx >= x+s and by < y+s:
#         chessboard(x+s, y, bx, by, s)
#     else:
#         chess[int(x+s)][int(y+s-1)] = i
#         chessboard(x+s, y, x+s, y+s-1, s)
#
#     if bx >= x+s and by >= y+s:
#         chessboard(x+s, y+s, bx, by, s)
#     else:
#         chess[int(x+s)][int(y+s)] = i
#         chessboard(x+s, y+s, x+s, y+s, s)
#     return 0
# print("请输入棋盘的规格K（2^k*2^k）：")
# size=int(eval(input()))
# global chess
# chess = [[0 for n in range(0, size)]for m in range(0, size)]
# print("请输入特殊方块所在位置（须在棋盘内部，右上角为坐标原点）:")
# bx = int(eval(input()))
# by = int(eval(input()))
# bx = bx-1
# by = by-1
# chessboard(0, 0, bx, by, size)
# chess[bx][by] = -1
# print("排序完毕")
# for p in range(0, size):
#     for q in range(0, size):
#         print(chess[p][q], end=' ')
#     print()
#不知道为什么上面的跑起来跟下面的很不一样
import matplotlib.pyplot as plt

def chess(tr, tc, pr, pc, size):
    global mark
    global table
    if size == 1:
        return  # 递归终止条件
    mark += 1  # 表示直角骨牌号
    count = mark
    half = size // 2  # 当size不等于1时，棋盘格规模减半，变为4个
# 小棋盘格进行递归操作
# 左上角
    if (pr < tr + half) and (pc < tc + half):
        chess(tr, tc, pr, pc, half)
    else:
        table[tr + half - 1][tc + half - 1] = count
        chess(tr, tc, tr + half - 1, tc + half - 1, half)
# 将[tr+half-1,tc+half-1]作为小规模棋盘格的特殊点，进行递归
# 右上角
    if (pr < tr + half) and (pc >= tc + half):
        chess(tr, tc + half, pr, pc, half)
    else:
        table[tr + half - 1][tc + half] = count
        chess(tr, tc + half, tr + half - 1, tc + half, half)
# 将[tr+half-1,tc+half]作为小规模棋盘格的特殊点，进行递归
# 左下角
    if (pr >= tr + half) and (pc < tc + half):
        chess(tr + half, tc, pr, pc, half)
    else:
        table[tr + half][tc + half - 1] = count
        chess(tr + half, tc, tr + half, tc + half - 1, half)
# 将[tr+half,tc+half-1]作为小规模棋盘格的特殊点，进行递归
# 右下角
    if (pr >= tr + half) and (pc >= tc + half):
        chess(tr + half, tc + half, pr, pc, half)
    else:
        table[tr + half][tc + half] = count
        chess(tr + half, tc + half, tr + half, tc + half, half)
# 将[tr+half,tc+half]作为小规模棋盘格的特殊点，进行递归
# 输出矩阵
def show(table):
    n = len(table)
    for i in range(n):
        for j in range(n):
            print(table[i][j], end='	')
        print('')

def drawboard(canvas1,board,colors,startx=50,starty=50,cellwidth=50):
    width=2*startx+len(board)*cellwidth
    height=2*starty+len(board)*cellwidth
    canvas1.config(width=width,height=height)#布置画布
    for i  in range(len(board)):
        for j in range(len(board)):
            index = board[i][j]
            if index == 0:
                color = 'white'#特殊方格显示为白色
            else:
                color = colors[6*index]#为了间隔开颜色
            cellx = startx+i*50
        celly = starty+j*50
        canvas1.create_rectangle(cellx, celly, cellx+cellwidth, celly+cellwidth, fill=color, outline="black") #画方格
    canvas1.update()


def visualize(table):
    plt.imshow(table, cmap=plt.cm.jet, alpha=2.0)
    plt.colorbar()
    plt.show()


mark = 0
# n = 8  # 输入8*8的棋盘规格
print("请输入棋盘的规格K（2^k*2^k）：")
n = int(eval(input()))
size = 2**n
print("请输入特殊方块所在位置（须在棋盘内部，右上角为坐标原点）:")
bx = int(eval(input()))
by = int(eval(input()))
bx = bx-1
by = by-1
table = [[-1 for x in range(size)] for y in range(size)]  # -1代表特殊格子
chess(0, 0, bx, by, size)  # 特殊棋盘位置
show(table)
visualize(table)
