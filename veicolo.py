import pygame




class Car:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
    
    def move(self,x,y):
        self.x = x
        self.y = y



def carica_auto():
  CAR_WIDTH = 32
  CAR_HEIGHT = 32

  # Ora queste righe partono solo quando chiami la funzione
  black_car = pygame.transform.scale(
      pygame.image.load(r"assets\black_car.png").convert_alpha(),
      (CAR_WIDTH, CAR_HEIGHT),
  )
  gray_car = pygame.transform.scale(
      pygame.image.load(r"assets\gray_car.png").convert_alpha(),
      (CAR_WIDTH, CAR_HEIGHT),
  )
  green_car = pygame.transform.scale(
      pygame.image.load(r"assets\green_car.png").convert_alpha(),
      (CAR_WIDTH, CAR_HEIGHT),
  )
  blue_car = pygame.transform.scale(
      pygame.image.load(r"assets\blue_car.png").convert_alpha(),
      (CAR_WIDTH, CAR_HEIGHT),
  )
    
  return black_car, gray_car, green_car, blue_car