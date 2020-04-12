#!/usr/bin/env python3

# Author: Zhiwei Luo

from socket import *
import _pickle as pickle
import threading

class NetworkInterface:
    udpPort = 6666
    socketUdp = None
    isBufferFull = False
    contextMouse = None
    receiveBuffer = None
    receiveAddr = None
    broadcastAddr = None
    myIPAddr = None
    bufferList = []
    threadReceive = None

    def __init__(self, context=None):
        self.contextMouse = context

    def initSocket(self, port=udpPort):
        self.socketUdp = socket(AF_INET, SOCK_DGRAM)
        self.myIPAddr = gethostbyname(gethostname())
        network = self.myIPAddr.split('.')[0:3];network.append('255')
        self.broadcastAddr = '.'.join(network)
        self.socketUdp.bind(('', self.udpPort))
        self.setBroadcastEnable()

    def setBroadcastEnable(self):
        self.socketUdp.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def setBlocking(self, block):
        self.socketUdp.setBlocking(block)

    def setTimeout(self, seconds):
        self.socketUdp.settimeout(seconds)

    def retrieveData(self):
        if len(self.bufferList) > 0:
            recvData = {'data': pickle.loads(self.bufferList[0][0]), 'ip': self.bufferList[0][1]}
            self.bufferList = self.bufferList[1:]
            return recvData 
        else:
            return None

    def receiveDataThread(self):
        while True:
            str_data, addr = self.socketUdp.recvfrom(1000)
            self.bufferList.append((str_data, addr))

    def startReceiveThread(self):
        self.threadReceive = threading.Thread(name='receive', target=self.receiveDataThread)
        self.threadReceive.setDaemon(True)
        self.threadReceive.start()

    def sendStringData(self, str):
        try:
            self.socketUdp.sendto(pickle.dumps(str), (self.broadcastAddr, self.udpPort))
        except:
            print('Send Data Failed!')
