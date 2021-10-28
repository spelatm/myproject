#算法课程，关于棋盘覆盖问题，采用分治法处理
i=0 #填写L型方块的编号
def chessboard(x, y, bx, by, size):
    if size == 1:
        return
    s=size/2
    global i
    i=i+1
    if bx < x+s and by < y+s:
        chessboard(x, y, bx, by, s)
    else:
        chess[int(x+s-1-1)][int(y+s-1-1)] = i
        chessboard(x, y, x+s-1, y+s-1, s)
    if bx < x+s and by >= y+s :
        chessboard(x, y+s, bx, by, s)
    else:
        chess[int(x+s-1-1)][int(y+s)] = i
        chessboard(x, y+s, x+s-1, y+s, s)
    if bx >= x+s and by < y+s :
        chessboard(x+s, y, bx, by, s)
    else:
        chess[int(x+s)][int(y+s-1-1)] = i
        chessboard(x+s, y, x+s, y+s-1, s)
    if bx >= x+s and by >= y+s:
        chessboard(x+s, y+s, bx, by, s)
    else:
        chess[int(x+s)][int(y+s)] = i
        chessboard(x+s, y+s, x+s, y+s, s)

print("请输入棋盘的规格K（2^k*2^k）：")
size=int(eval(input()))
global chess
chess = [[0 for n in range(0, size)]for m in range(0, size)]
print("请输入特殊方块所在位置（须在棋盘内部，右上角为坐标原点）:")
bx = int(eval(input()))
by = int(eval(input()))
chessboard(0, 0, bx, by, size)
chess[bx][by] = -1
print("排序完毕")
for p in range(0, size):
    for q in range(0, size):
        print(chess[p][q],end='')
    print()