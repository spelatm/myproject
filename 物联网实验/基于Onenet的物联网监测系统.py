import paho.mqtt.client as mqtt
from urllib.parse import quote
import time
import json
import random
import base64
import hmac
from tkinter import *
import threading
from tkintertable import TableCanvas
import tkinter.scrolledtext as scrolledtext



# HOST = "mqttstls.heclouds.com"    # 加密地址
# PORT = "8883"                     # 加密端口
HOST = "mqtts.heclouds.com"         # 未加密地址
PORT = "1883"                       # 未加密端口
PRO_ID = "506576"                   # 产品ID
DEV_ID = "929284376"                # 设备ID
DEV_NAME = "sensor_1"            # 设备名称
DEV_KEY = "Dzdw13NP6RiuFTfkcxcFIOToUUDMG/W5BLhtSpp0nCQ="        # 设备Key
ACCESS_KET = "r8Fdzk6nVsIRuVif14bBQx9AGQ2GulVnaHyVYjnF9xU"     # 产品AccessKey
sui = False
switch = True
count = 0  # 报文计数

# 用于生成Token的函数
def token(_pid, dname, access_key):
    version = '2018-10-31'
    # res = 'mqs/%s' % id           # 通过MQ_ID访问
    # res = 'products/%s' % id      # 通过产品ID访问产品API
    res = 'products/%s/devices/%s' % (_pid, dname)  # 通过MQTTS产品id和设备名称访问
    # 用户自定义token过期时间
    et = str(int(time.time()) + 3600000)
    # 签名方法，支持md5、sha1、sha256
    method = 'md5'
    # 对access_key进行decode
    key = base64.b64decode(access_key)
    # print(key)
    # 计算sign
    org = et + '\n' + method + '\n' + res + '\n' + version
    # print(org)
    sign_b = hmac.new(key=key, msg=org.encode(), digestmod=method)
    sign = base64.b64encode(sign_b.digest()).decode()
    # print(sign)
    # value 部分进行url编码，method/res/version值较为简单无需编码
    sign = quote(sign, safe='')
    res = quote(res, safe='')
    # token参数拼接
    token = 'version=%s&res=%s&et=%s&method=%s&sign=%s' % (version, res, et, method, sign)
    return token

# 定义了带时间戳的输出格式
def ts_print(*args):
    t = time.strftime("[%Y-%m-%d %H:%M:%S")
    ms = str(time.time()).split('.')[1][:3]
    t += ms + ']:'
    print(t, *args)

# 当MQTT代理响应客户端连接请求时触发
def on_connect(client, userdata, flags, rc):
    ts_print("<<<<CONNACK")
    ts_print("connected with result code: " + mqtt.connack_string(rc), rc)
    client.subscribe(topic=topic_cmd, qos=1)        # 订阅由OneNET平台下发的命令
    client.subscribe(topic=topic_dp, qos=1)         # 订阅上传数据的响应结果

# 当接收到MQTT代理发布的消息时触发
def on_message(client, userdata, msg):
    ts_print('on_message')
    ts_print("Topic: " + str(msg.topic))
    ts_print("Payload: " + str(msg.payload))
    # LED_Control(str(msg.payload))
    if topic_cmds in msg.topic:                     # 命令响应的主题
        responseTopic = str(msg.topic).replace("request","response",1)
        # print(responseTopic)
        client.publish(responseTopic,'OK',qos = 1)  # 发布命令响应

# 当客户端调用publish()发布一条消息至MQTT代理后被调用
def on_publish(client, userdata, mid):
    ts_print("Puback:mid: " + str(mid))
    ts_print("Puback:userdata: " + str(userdata))

# 当MQTT代理响应订阅请求时被调用
def on_subscribe(client, obj, mid, granted_qos):
    ts_print("Subscribed: message:" + str(obj))
    ts_print("Subscribed: mid: " + str(mid) + "  qos:" + str(granted_qos))

# 当客户端与代理服务器断开连接时触发
def on_disconnect(client):
    ts_print('DISCONNECTED')

# 发布到服务器的数据内容
def data1(ds_id, value1, value2, value3, value4, value5, value6):
    message = {
        "id": int(ds_id),
        "dp": {
            "temperature": [{      # 距离传感器采集的数据
                "v": value1
            }],
            "humidity": [{        # Python产生的随机数
                "v": value2
            }],
            "CO2": [{  # 距离传感器采集的数据
                "v": value3
            }],
            "PM2_5": [{  # 距离传感器采集的数据
                "v": value4
            }],
            "PM100": [{  # 距离传感器采集的数据
                "v": value5
            }],
            "PH": [{  # 距离传感器采集的数据
                "v": value6
            }],
        }
    }
    # print(message)
    message = json.dumps(message).encode('ascii')
    return message


def data2(ds_id,value):
    message = {
        "id": int(ds_id),
        "dp": {
            "temperature": [{      # 距离传感器采集的数据
                "v": value
            }],
            "humidity": [{        # Python产生的随机数
                "v": random.random()
            }],
            "CO2": [{  # 距离传感器采集的数据
                "v": random.uniform(0, 100)
            }],
            "PM2_5": [{  # 距离传感器采集的数据
                "v": random.randint(0, 1000)
            }],
            "PM100": [{  # 距离传感器采集的数据
                "v": random.randint(0, 1000)
            }],
            "PH": [{  # 距离传感器采集的数据
                "v": random.uniform(0, 12)
            }],
        }
    }
    # print(message)
    message = json.dumps(message).encode('ascii')
    return message

def publishmessage_attime(topic_publish,count,client): # 模拟数据并上传
    # global switch
    def run():
        global count
        if sui:
            while switch:
                client.publish(topic=topic_publish, payload=data2(count, random.uniform(0, 100)), qos=1)
                print("-------------------------------------------------------------------------------")
                print("定时上传数据发送成功")
                count += 1
                time.sleep(3)
                if not switch:
                    break
    thread = threading.Thread(target=run)
    thread.start()


def choose_to_publish(topic_publish,client, value1, value2, value3, value4, value5, value6):# 选择好数据并上传
    if sui:
        global count
        client.publish(topic=topic_publish, payload=data1(count, value1, value2, value3, value4, value5, value6), qos=1)
        print("-------------------------------------------------------------------------------")
        print("指定上传数据发送成功")
        count += 1
        return 0


def connect_to_onenet(): # 连接到Onenet
    global sui
    client.connect(HOST, int(PORT), keepalive=1200)
    # connect_to_onenet()
    client.loop_start()
    sui = True

    print("连接成功")

def stop_connect_onenet(client): # 断开连接
    global sui
    client.disconnect()
    client.loop_stop()
    sui = False
    print("断开连接")

def exit_out():# 退出
    exit()


def switch_off():
    global switch
    switch = False
    print("-------------------------------------------------------------------------------")
    print("关闭定时发送数据")

def switch_on():
    global switch
    switch = True
    publishmessage_attime(topic_publish,count, client)

def refreshText():
    global count
    ll = ['断开', '连接']
    text1.delete(0.0, END)
    text1.insert(INSERT, count)
    text1.update()
    if sui == True:
        text2.delete(0.0, END)
        text2.insert(INSERT, ll[1])
        text2.update()
    else:
        text2.delete(0.0, END)
        text2.insert(INSERT, ll[0])
        text2.update()
    root.after(1000, refreshText)

if __name__ == '__main__':
    # 按照OneENT要求的格式，配置数据发布和订阅的主题
    topic_dp = '$sys/%s/%s/dp/post/json/+' % (PRO_ID, DEV_NAME)   # 设备上报数据主题
    topic_cmd = '$sys/%s/%s/cmd/#' % (PRO_ID, DEV_NAME)           # 设备接受命令主题
    topic_cmds = '$sys/%s/%s/cmd/request/' % (PRO_ID, DEV_NAME)   # 设备接受命令主题
    topic_publish = '$sys/%s/%s/dp/post/json' % (PRO_ID, DEV_NAME)
    # 配置MQTT连接信息
    client_id = DEV_NAME
    username = PRO_ID
    password = token(PRO_ID, DEV_NAME, DEV_KEY)
    print('username:' + username)
    print('password:' + password)
    client = mqtt.Client(client_id=client_id, clean_session=True, protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.username_pw_set(username=username, password=password)
    # client.tls_set(ca_certs='MQTTS-certificate.pem')              # 加密方式需要使用鉴权证书
    # client.tls_insecure_set(True) #关验证
    # client.connect(HOST, int(PORT), keepalive=1200)
    # # connect_to_onenet()
    # client.loop_start()
    # print("连接成功")

    root = Tk()
    root.title('传感器仿真终端')
    root.geometry('640x540')  # 这里的乘号不是 * ，而是小写英文字母 x



    # 6文本框用来输入数据
    inp1 = Entry(root)# temperature
    inp1.place(relx=0.3, rely=0.2, relwidth=0.3, relheight=0.05)
    inp2 = Entry(root)# humidity
    inp2.place(relx=0.3, rely=0.3, relwidth=0.3, relheight=0.05)
    inp3 = Entry(root)# PH
    inp3.place(relx=0.3, rely=0.4, relwidth=0.3, relheight=0.05)
    inp4 = Entry(root)# CO2
    inp4.place(relx=0.3, rely=0.5, relwidth=0.3, relheight=0.05)
    inp5 = Entry(root)# PM2_5
    inp5.place(relx=0.3, rely=0.6, relwidth=0.3, relheight=0.05)
    inp6 = Entry(root)# PM100
    inp6.place(relx=0.3, rely=0.7, relwidth=0.3, relheight=0.05)

    lb1 = Label(root, text='temperature')
    lb1.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.05)
    lb2 = Label(root, text='humidity')
    lb2.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.05)
    lb3 = Label(root, text='PH')
    lb3.place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.05)
    lb4 = Label(root, text='CO2')
    lb4.place(relx=0.1, rely=0.5, relwidth=0.2, relheight=0.05)
    lb5 = Label(root, text='PM2_5')
    lb5.place(relx=0.1, rely=0.6, relwidth=0.2, relheight=0.05)
    lb6 = Label(root, text='PM100')
    lb6.place(relx=0.1, rely=0.7, relwidth=0.2, relheight=0.05)


    # client = connect_to_onenet()
    # stop_connect_onenet(client)
    btn1 = Button(root, text='连接', command=lambda: connect_to_onenet())
    btn1.place(relx=0, rely=0.1, relwidth=0.15, relheight=0.1)
    btn2 = Button(root, text='断开', command=lambda: stop_connect_onenet(client))
    btn2.place(relx=0.15, rely=0.1, relwidth=0.15, relheight=0.1)

    btn3 = Button(root, text='上传', command=lambda: choose_to_publish(topic_publish ,client, inp1.get(),
                                                                     inp2.get(), inp3.get(), inp4.get(), inp5.get(),
                                                                     inp6.get()))
    btn3.place(relx=0.3, rely=0.1, relwidth=0.15, relheight=0.1)
    btn4 = Button(root, text='定时上传', command=lambda: switch_on())
    btn4.place(relx=0.45, rely=0.1, relwidth=0.15, relheight=0.1)
    btn5 = Button(root, text='关闭定时上传', command=lambda: switch_off())
    btn5.place(relx=0.6, rely=0.1, relwidth=0.15, relheight=0.1)
    btn6 = Button(root, text='退出', command=lambda: exit_out())
    btn6.place(relx=0.75, rely=0.1, relwidth=0.15, relheight=0.1)



    lb7 = Label(root, text='上传报文数')
    lb7.place(relx=0, rely=0.8, relwidth=0.1, relheight=0.03)
    text1 = Text(root, width=15, height=1)
    text1.place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.03)

    lb8 = Label(root, text='当前状态')
    lb8.place(relx=0.5, rely=0.8, relwidth=0.1, relheight=0.03)
    text2 = Text(root, width=15, height=1)
    text2.place(relx=0.6, rely=0.8, relwidth=0.1, relheight=0.03)
    # text1.grid(row=0, column=1, padx=10, pady=10)

    root.after(1000, refreshText)
    # txt = Text(root)
    # txt.place(rely=0.6, relheight=0.4)
    root.mainloop()

