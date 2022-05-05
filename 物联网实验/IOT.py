import qrcode
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
import os
import uuid

# img = qrcode.make('hello qrcode !')
# img.save('test.png')
def show_pic(f1,file):

    # img_open = Image.open(file)
    # global img_png
    # img_png = ImageTk.PhotoImage(img_open)
    # label_img = tk.Label(root, image=img_png, anchor='center',)
    # label_img.place(x=20, y=20)
    # label_img.pack()
    global photo
    global img
    img = Image.open(file)  # 打开图片
    photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
    imglabel = tk.Label(f1, image=photo)
    imglabel.grid(row=5, column=2)


def getQRcode(root, strs, name, insert_image):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    # 添加数据
    qr.add_data(strs)
    # 填充数据
    qr.make(fit=True)
    # 生成图片
    img = qr.make_image(fill_color="blue", back_color="white")
    img = img.convert("RGBA")  # RGBA
    # 添加logo
    icon = Image.open(insert_image).convert("RGBA")
    # 获取图片的宽高
    img_w, img_h = img.size
    factor = 6
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    # 重新设置logo的尺寸
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    print(icon)
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    img.paste(icon, (w, h), icon)
    # 显示图片
    # plt.imshow(img)
    # plt.show()
    img.save(name)
    show_pic(root, name)
    return img


def open_file():
    global content
    global filename
    filename = filedialog.askopenfilename()
    infile = open(filename, 'r')
    # content = infile.read()
    file_path = os.path.dirname(filename)
    print(filename)
    return filename

def write_in(f1,filename):
    # n1 = entry1.get()
    n2 = entry2.get()
    n3 = entry3.get()
    n3 = n3 + '.png'
    # 增加学校场所的地点编码：
    pp = \
        {
     "1号门": "建筑类型：坐标建筑门0，坐标：000 ",
     "计算机学院": "建筑类型：教学楼，坐标：000N1W1S0E0 ",
     "电气学院": "建筑类型：教学楼，坐标：000N2W1S0E0 ",
     "化工学院": "建筑类型：教学楼，坐标：000N2W2S0E0 ",
     "研究生院": "建筑类型：教学楼，坐标：000N1W1S0E0 ",
     "艺术学院": "建筑类型：教学楼，坐标：000N3W1S0E0 ",
     "耒耜大厦": "建筑类型：教学楼，坐标：111111N0W0S2E1 ",
     "京江操场": "建筑类型：运动场所，坐标：111N0W0S1E1",
     "京江学院": "建筑类型：教学楼，坐标：111N1W0S0E1",
     "F区学生宿舍": "建筑类型：学生宿舍，坐标：111N2WOS0E1 ",
     "E区学生宿舍": "建筑类型：学生宿舍，坐标：111N0WOS0E1 ",
     "G区学生宿舍": "建筑类型：学生宿舍，坐标：111N0WOS0E2 ",
     "D区学生宿舍": "建筑类型：学生宿舍，坐标：111N0WOS0E3 ",
     "B区学生宿舍": "建筑类型：学生宿舍，坐标：333N1W0S0E1 ",
     "C区学生宿舍": "建筑类型：学生宿舍，坐标：333N0W1S0E0 ",
     "A区学生宿舍": "建筑类型：学生宿舍，坐标：333N0W0S0E1 ",
     "七食堂": "建筑类型：餐饮 ，坐标：111N2WOS0E2UP1",
     "六食堂": "建筑类型：餐饮，坐标：111N2WOS0E2 ",
     "五食堂": "建筑类型：餐饮，坐标：111N0WOS1E3UP ",
     "四食堂": "建筑类型：餐饮，坐标：111N0WOS0E3 ",
     "三食堂": "建筑类型：餐饮，坐标：333N0W0S1E1 ",
     "二食堂": "建筑类型：餐饮，坐标：333N0W0S1E2 ",
     "一食堂": "建筑类型：餐饮，坐标：222N1W0S0E3 ",
     "西山操场": "建筑类型：运动场所坐标建筑(333)，坐标：333 ",
     "东山操场": "建筑类型：运动场所，坐标：222N1W0S0E2 ",
     "汽车学院": "建筑类型：教学楼，坐标：333N0W0S1E0 ",
     "能动学院": "建筑类型：教学楼，坐标：333N0W0S2E0 ",
     "土木工程学院": "建筑类型：教学楼，坐标：333N0W1S1E0 ",
     "图书馆": "建筑类型：公共设备，坐标：000N3W0S0E0 ",
     "医学院": "建筑类型：教学楼坐标：，000N3W0S0E1 ",
     "药学院": "建筑类型：教学楼，坐标：000N1W0S0E1 ",
     "机械工程学院": "建筑类型：坐标：333N0W2S2E0 ",
     "讲堂群": "建筑类型：教学楼，坐标：333N0W1S2E0 ",
     "三山楼": "建筑类型：教学楼，坐标：333N0W1S3E0 ",
     "实习工厂": "建筑类型：教学楼，坐标：333N0W1S4E0 ",
     "计算中心": "建筑类型：精密公共设备，坐标：222N3W1S0E0 ",
     "三江楼": "建筑类型：教学楼，坐标：222N2W0S0E0 ",
     "环境学院": "建筑类型：教学楼，坐标：222N4W0S0E0 ",
     "外国语学院": "建筑类型：教学楼，坐标：222N3W0S0E0 ",
     "大礼堂": "建筑类型：公共设备，坐标：333N0W0S2E1 ",
     "新一区快递站点": "建筑类型：快递站点，坐标：333N2W0S0E1 ",
     "邮政快递站点": "建筑类型：快递站点，坐标：333N0W0S0E2 ",
     "体育馆": "建筑类型：运动场所，坐标：222N1W0S0E1 ",
     "会议中心": "建筑类型：公共设备，坐标：222N5W0S0E1 ",
     "校医院": "建筑类型：医院，坐标：222N5W0S0E1 ",
     "教职工生活区": "建筑类型：公共设备，坐标：222N1W0S0E4 ",
     "京江门": "建筑类型：坐标建筑（门1），坐标：111 ",
     "中门": "建筑类型：坐标建筑门（门2），坐标：222 ",

     }
    if n2 in pp.keys():
        n2 = n2 + pp[n2]
    else:
        n2 = n2 + ":" +"该地点未被录入"
    # print(n2)
    getQRcode(f1, n2, n3, filename)

# def get_name():
#     global n3
#     n3 = entry3.get()
#     return n3

if __name__ == '__main__':

    window = tk.Tk()
    window.title('二维码实验')
    ##窗口尺寸
    # window.geometry('400x400')
    content = ''

    file_path = ''
    filename = tk.StringVar()
    filename = ''

    # def process_file(content):
    #     print(content)


    window.geometry("598x500")

    mf = tk.Frame(window)

    mf.pack()
    f1 = tk.Frame(mf, width=600, height=250)

    f1.pack()
    f2 = tk.Frame(mf, width=600, height=250)
    f2.pack()


    label1 = tk.Label(f1, text="选择内嵌图片").grid(row=0, column=0, sticky='e')

    entry1 = tk.Entry(f1, width=50, textvariable=filename)
    entry1.grid(row=0, column=1, padx=2, pady=2, sticky='we', columnspan=25)

    label2 = tk.Label(f1, text="输入二维码信息：").grid(row=1, column=0, sticky='e')

    entry2 = tk.Entry(f1, width=50)
    entry2.grid(row=1, column=1, padx=2, pady=2, sticky='we', columnspan=25)


    label3 = tk.Label(f1, text="输入二维码名称：").grid(row=2, column=0, sticky='e')

    entry3 = tk.Entry(f1, width=50)
    entry3.grid(row=2, column=1, padx=2, pady=2, sticky='we', columnspan=25)

    button1 = tk.Button(f1, text="选择图片", command=lambda: open_file())
    button1.grid(row=0, column=27, sticky='ew', padx=8, pady=4)

    button2 = tk.Button(f1, text="生成二维码", command=lambda: write_in(f1,filename))
    button2.grid(row=2, column=27, sticky='ew', padx=8, pady=4)

    ##显示出来
    window.mainloop()
    # getQRcode("https://music.163.com/song?id=36990266&userid=112961323", '01.png', '1.jpg')

