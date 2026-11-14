import sys
import pygame
pygame.init()
LARGHEZZA = 1056
ALTEZZA = 672

schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Traffic System")

orologio = pygame.time.Clock()
from field import create_field, lista_auto, grass_img,road_img,rotated_road,road_texture_img
from semaforo import semaforo_rosso
Running = True


FIELD = create_field()
while Running:
  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      Running = False

  for riga_idx, riga in enumerate(FIELD):
    for colonna_idx, valore in enumerate(riga):
            x = colonna_idx * 32
            y = riga_idx * 32
            if valore == 0:
              schermo.blit(grass_img, (x, y))
            elif valore == 1:
              schermo.blit(road_img, (x, y))
            elif valore == 2:
              schermo.blit(rotated_road, (x, y))
            elif valore == 3:
              schermo.blit(road_texture_img, (x, y))
            
  for auto in lista_auto:
    
    schermo.blit(auto.img, (auto.x, auto.y))
    
  
  schermo.blit(semaforo_rosso,(13*32,13*32))
  schermo.blit(semaforo_rosso,(19*32,13*32))
  schermo.blit(semaforo_rosso,(13*32,7*32))
  schermo.blit(semaforo_rosso,(19*32,7*32))

  # Aggiorna il display limitando a 60 FPS
  pygame.display.flip()
  orologio.tick(60)

pygame.quit()
sys.exit()