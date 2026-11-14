import sys
import pygame
pygame.init()
LARGHEZZA = 1056
ALTEZZA = 672

schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Traffic System")

orologio = pygame.time.Clock()
from field import create_field, lista_auto, grass_img,road_img,rotated_road,road_texture_img
from semaforo import semaforo_rosso,semaforo_verde,Semaforo,semaforo_giallo,GestoreTraffico
Running = True



semaforo_nord = Semaforo("RED",semaforo_rosso)
semaforo_sud = Semaforo("RED",semaforo_rosso)
semaforo_est = Semaforo("RED",semaforo_rosso)
semaforo_ovest = Semaforo("RED",semaforo_rosso)
gestore = GestoreTraffico(semaforo_nord,semaforo_sud,semaforo_est,semaforo_ovest)
INCROCIO_POSITIONS = [[14*32,9*32],[14*32,10*32],[19*32,11*32],[19*32,12*32],[17*32,8*32],[18*32,8*32],[15*32,13*32],[16*32,13*32]]
FIELD = create_field()
while Running:
  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      Running = False
  gestore.aggiorna()  # Il controller calcola il tempo, cambia le fasi, ecc.
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

    if [auto.x,auto.y] in INCROCIO_POSITIONS:
      pass
    else:
      auto.move()
    
    
  
  schermo.blit(semaforo_sud.img,(13*32,13*32))
  schermo.blit(semaforo_est.img,(19*32,13*32))
  schermo.blit(semaforo_ovest.img,(13*32,7*32))
  schermo.blit(semaforo_nord.img,(19*32,7*32))

  # Aggiorna il display limitando a 60 FPS
  pygame.display.flip()
  orologio.tick(60)

pygame.quit()
sys.exit()