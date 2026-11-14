from veicolo import carica_auto
import pygame
import random
from veicolo import Car

COLONNE = 33  # 1056 / 32 = 33
RIGHE = 21  # 672 / 32 = 21
FIELD = [[0 for _ in range(COLONNE)] for _ in range(RIGHE)]
lista_auto = []
blue_car,green_car,gray_car,black_car = carica_auto()
CARS = (blue_car,green_car,gray_car,black_car)

grass_img = pygame.image.load(
      r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\grass.png"
  ).convert()
road_img = pygame.image.load(
      r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\road.png"
  ).convert()
road_texture_img = pygame.image.load(
      r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\road_texture.png"
  ).convert()
rotated_road = pygame.transform.rotate(road_img,90)

def create_field():
  global FIELD,CARS,lista_auto
  for i in range(len(FIELD)):
    if i>=9 and i <=12:
      continue
    FIELD[i][15] = 1
    FIELD[i][16] = 1
    FIELD[i][17] = 1
    FIELD[i][18] = 1

  for j in range(len(FIELD[0])):
    for i in range(9,13):
      if j>=15 and j<=18:
        continue
      FIELD[i][j] = 2


  for j in range(15,19):
    for i in range(9,13):
      FIELD[i][j] = 3


  for riga in [0,20]:
    if riga == 0:
      for colonna in range(17,19):
        x = colonna * 32
        y = riga * 32
        img_casuale = random.choice(CARS)
        car = Car(x,y,(0,1),1,img_casuale)
        lista_auto.append(car)
    else:
      for colonna in range(15,17):
        x = colonna * 32
        y = riga * 32
        img_casuale = random.choice(CARS)
        car = Car(x,y,(0,-1),1,img_casuale)
        lista_auto.append(car)

  for riga in range(9,11):
        x = 0
        y = riga * 32
        img_casuale = random.choice(CARS)
        car = Car(x,y,(1,0),1,pygame.transform.rotate(img_casuale,90))
        lista_auto.append(car)
   
  for riga in range(11,13):
        x = 32 * 32
        y = riga * 32
        img_casuale = random.choice(CARS)
        car = Car(x,y,(-1,0),1,pygame.transform.rotate(img_casuale,90))
        lista_auto.append(car)
   

 

  return FIELD