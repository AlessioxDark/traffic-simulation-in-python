import pygame

from veicolo import genera_auto


COLONNE = 33  # 1056 / 32 = 33
RIGHE = 21  # 672 / 32 = 21
FIELD = [[0 for _ in range(COLONNE)] for _ in range(RIGHE)]

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
  global FIELD
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



 

  return FIELD