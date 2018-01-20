#!/usr/bin/python3
from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt,QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QImage, QPixmap,QPen )
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout,
                             QLabel, QLineEdit, QPushButton)
import sys
import random

class  Polyminoid(QGraphicsItem):
  def __init__(self,x,y,genom):
    super().__init__()
    self.x = x
    self.y = y
    self.genom = genom
    self.die = False
    
  def boundingRect(self):
    return QRectF(0,0,10,10)
  
  def move (self):
    # случайное движение
    a = random.randint(0,3)
    if a == 0:
      self.y-=10
    elif a == 1:
      self.y+=10
    elif a == 2:
      self.x+=10
    elif a == 3:
      self.x-=10
    
    self.update()
    
  # отрисовка полиминойда
  def paint(self, painter, option, widget):
    new_x = self.x
    new_y = self.y
    save = 0
    polyoid = []
    for gen in self.genom:
      # нарисовать ячейку на востоке
      if gen == "e":
        new_x = new_x + 10
        painter.setPen(QPen(Qt.blue,2,Qt.SolidLine,Qt.RoundCap))
        painter.drawRect(new_x,new_y,10,10)
      # нарисовать ячейку на западе
      elif gen == "w":
        new_x = new_x - 10
        painter.setPen(QPen(Qt.green,2,Qt.SolidLine,Qt.RoundCap))
        painter.drawRect(new_x,new_y,10,10)
      # нарисовать ячейку на севере
      elif gen == "n":
        painter.setPen(QPen(Qt.yellow,2,Qt.SolidLine,Qt.RoundCap))
        new_y = new_y - 10
        painter.drawRect(new_x,new_y,10,10)
      # нарисовать ячейку на юге
      elif gen == "s":
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine,Qt.RoundCap))
        new_y = new_y + 10
        painter.drawRect(new_x,new_y,10,10)
      polyoid.append((new_x,new_y))
      # если полиминойд замкнут сам в себя то он умерает
      if polyoid.count((new_x,new_y)) > 1:
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine,Qt.RoundCap))
        painter.drawLine(new_x-10,new_y-10,new_x+10,new_y+10)
        painter.drawLine(new_x-10,new_y+10,new_x+10,new_y-10)
        self.die = True

  #функция мутации полиминойда
  def mutation (self):
    a = random.randint(0,30)
    if a == 0:
        c = None
        d = random.randint(1,len(self.genom))
        b = random.randint(0,3)
        if b == 0:
          c = "n"
        elif b == 1:
          c = "s"
        elif b == 2:
          c = "e"
        elif b == 3:
          c = "w"
        self.genom.insert(d,c)
  
  #функция скрещевания полиминойда
  def childPoly (self,poly,scene):
    for p in poly:
      #ищет полиминойда на своей клетке с такойже длинной генома как и у себя
      if p.x == self.x and p.y == self.y and len(p.genom) == len(self.genom)and p != self:
        x = 10*random.randint(-15,15)
        y = 10*random.randint(-15,15)
        child = Polyminoid(self.x+x,self.y+y,[])
        poly.append(child)
        scene.addItem(child)
        #случайное смешевание генома
        for g in range(len(self.genom)):
          a = random.randint(0,1)
          if a == 0:
            child.genom.append(self.genom[g])
          elif a == 1:
            child.genom.append(p.genom[g])
        print("New Child")
        print(child.genom)

class MainGameWindow (QMainWindow):
  # настройки визуальной части
  def __init__ (self):
    super().__init__()
    self.setWindowTitle("Polymino")
    self.resize(400,400)
    
    self.setStyleSheet("margin: 10px; padding:10px; border: 2px solid green; background-color: cyan;")
    
    self.view = QGraphicsView(self)
    self.view.setCacheMode(QGraphicsView.CacheBackground)
    
    #self.view.resize(400,300)
    self.setCentralWidget(self.view)

    self.scene = QGraphicsScene(self.view)
    self.view.setScene(self.scene)
    
    self.scene.setSceneRect(0, 0, 100, 100)

    self.polyminoids = []

class Time ():
  # процессор событий
  def __init__ (self,w):
    self.w = w
    self.tickn = 0
  def tick(self):
      print(len(self.w.polyminoids))
      # появление первых полиминойдов
      if self.tickn < 10:
        p = Polyminoid(30,30,["e"])
        self.w.polyminoids.append(p)
        self.w.scene.addItem(p)
        print ('New Poly')

      for p in self.w.polyminoids:
        # исполнение функций каждого полиминойда
        p.move()
        p.mutation()
        p.childPoly(self.w.polyminoids,self.w.scene)
        if p.die == True:
          print("Poly Die")
          self.w.polyminoids.remove(p)
          self.w.scene.removeItem(p)
      self.w.update()
      self.tickn+= 1
app = QApplication(sys.argv)
MyWindow = MainGameWindow()
time = Time(MyWindow)
timer = QTimer()
timer.timeout.connect(time.tick)
timer.start(1000)

MyWindow.show()
app.exec_()
