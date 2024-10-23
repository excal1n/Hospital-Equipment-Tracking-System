# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 19:59:18 2022

@author: pietr
"""

# python3.6


import random
from math import sqrt
import matplotlib.pyplot as plt

from paho.mqtt import client as mqtt_client

x = ''
y = ''
r1 = 0
r2 = 0
r3 = 0
U = 20
Vx = 20
Vy = 20 
plotar = ''    
payload = [0,0,0]
coordenadas = "coordenadas.txt"

class Ponto:
    def __init__(self,x:float=0,y:float=0) -> None:
        self._x = x
        self._y = y

    @property
    def x(self)->float:
        return self._x
    @x.setter
    def x(self,x:float)->float:
        self._x = x

    @property
    def y(self)->float:
        return self._y
    @y.setter
    def y(self,y:float)->None:
        self._y = y
    
    def distancia(self,ponto)->float:
        return sqrt((self.x - ponto.x)**2 + (self.y - ponto.y)**2)
    
    def __repr__(self) -> str:
        return f"P({self.x},{self.y})"
    
# /////////////////////////////////////////////////////////////////////////////////////
broker = 'broker.emqx.io'
port = 1883
topic1 = "esp1"
topic2 = "esp2"
topic3 = "esp3"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'bledemo'


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

plt.ion()

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(topic1)
            client.subscribe(topic2)
            client.subscribe(topic3)
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if (msg.topic == topic1):
            payload[0] = int(f"{msg.payload.decode()}")
            # print(payload)  
            calcula(payload)
        if (msg.topic == topic2):
            payload[1] = int(f"{msg.payload.decode()}")
            # print(payload)
            calcula(payload)
        if (msg.topic == topic3):
            payload[2] = int(f"{msg.payload.decode()}")
            # print(payload)
            calcula(payload)
    client.on_message = on_message
 
    
def escreve_txt_grafico(plotar):
    with open(coordenadas,'w') as fw:
        fw.write(plotar)
    print("gravado")
    pullData = open(coordenadas,"r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    plt.cla()
    plt.clf()
    ax1.clear()
    plota_pontos_ancora(pontos)
    plt.axis([0,100, 0,100])
    plt.plot(xar, yar,"o")
    plt.show()

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    
# /////////////////////////////////////////////////////////////////////////////////////

def calcula(payload):
    
    r1 = payload[0]*(-1)
    r2 = payload[1]*(-1)
    r3 = payload[2]*(-1)
    
    print(r1,r2,r3)      
      
    V = sqrt(Vx**2 + Vy**2) #Reta aresta ponto 0,0
      
    xi = int(((r1**2) - (r2**2) + (U**2))/(2*U))
    yi = int(((r1**2) - (r3**2) + (V**2) - (2*Vx*xi))/(2*Vy))
    
    x = str(xi)
    y = str(yi)
    
    plotar = (x+','+y)
    
    print(plotar)
    
    escreve_txt_grafico(plotar)

def plota_ponto(p:Ponto,cor:str):
    circulo = plt.Circle((p.x,p.y),2.9,fill=True,color=cor)
    ax = plt.gca()
    ax.add_patch(circulo)

def plota_pontos_ancora(pontos):
    for ponto in pontos:
        plota_ponto(ponto,'r')
        
if __name__ == '__main__':
    
    p1 = Ponto(0,0) #x1,y1 Ponto1 = (0,0)
    p2 = Ponto(100,0) #x2,y2 Ponto2 = (Vx,Vy)
    p3 = Ponto(100,100) #x3,y3 Ponto3 = (U,0)
        
    pontos = [p1,p2,p3]
    
    run()