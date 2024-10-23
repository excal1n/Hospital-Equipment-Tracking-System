import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

xar = 0
yar = 0
xar2 = 0
yar2 = 0

fig=plt.figure(figsize=(20,12))
gráfico=fig.add_subplot()

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

def plota_ponto(p:Ponto,cor:str):
    circulo = plt.Circle((p.x,p.y),2.9,fill=True,color=cor)
    ax = plt.gca()
    ax.add_patch(circulo)

def plota_pontos_ancora(pontos):
    for ponto in pontos:
        plota_ponto(ponto,'r')

def atualiza(i):
    pullData = open("coordenadas.txt","r").read()
    dataArray = pullData.split('\n')
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split('/')
            xar = int(x[0:2:1])
            yar = int(x[3:6:1])
            xar2 = int(y[0:2:1])
            yar2 = int(y[3:6:1])
    gráfico.clear()
    gráfico.set_xlim(0,100)
    gráfico.set_ylim(0,100)
    plota_pontos_ancora(pontos)
    gráfico.plot(xar,yar,"o")
    gráfico.plot(xar2,yar2,"o")

p1 = Ponto(0,0) #x1,y1 Ponto1 = (0,0)
p2 = Ponto(100,0) #x2,y2 Ponto2 = (Vx,Vy)
p3 = Ponto(100,100) #x3,y3 Ponto3 = (U,0)
        
pontos = [p1,p2,p3]

a=animation.FuncAnimation(fig, atualiza, interval=1)
plt.show()