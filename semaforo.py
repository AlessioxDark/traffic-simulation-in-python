import pygame
class Semaforo:
    def __init__(self,color):
        self.color = color

    def change_color(self,color):
        self.color = color


semaforo_rosso = pygame.image.load(
    r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\red_light.png"
).convert_alpha()
semaforo_giallo = pygame.image.load(
    r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\yellow_light.png"
).convert_alpha()
semaforo_verde = pygame.image.load(
    r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\green_light.png"
).convert_alpha()