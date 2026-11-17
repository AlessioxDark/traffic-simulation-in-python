import sys
import random
import pygame


pygame.init()
LARGHEZZA = 1056
ALTEZZA = 672
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Traffic System")

orologio = pygame.time.Clock()
from field import create_field, grass_img,road_img,rotated_road,road_texture_img,genera_auto
from semaforo import traffic_controller, SEMAFORI_IMG
from veicolo import lista_auto
Running = True

SEMAFORI_POS = {
  "nord":(19*32,7*32),
  "nord_sx":(22*32,7*32),
  "sud":(13*32,13*32),
  "sud_sx":(10*32,13*32),
  "ovest":(13*32,7*32),
  "ovest_sx":(10*32,7*32),
  "est":(19*32,13*32),
  "est_sx":(22*32,13*32),
}

FIELD = create_field()
tick = 0
while Running:
  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      Running = False
  traffic_controller.aggiorna()  # Il controller calcola il tempo, cambia le fasi, ecc.
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
  # VISUALIZZAZIONE DELLE TRAIETTORIE
  
  for auto in lista_auto:  
    auto.aggiorna()

    schermo.blit(
        auto.img,
        (round(auto.x), round(auto.y))
    )
    
    
  if tick % (5*60) == 0:
    genera_auto()
  lista_auto[:] = [
    auto for auto in lista_auto
    if (
        -32 <= auto.x <= LARGHEZZA
        and -32 <= auto.y <= ALTEZZA
    )
]
    
  for semaforo_name,semaforo in traffic_controller.semafori.items():   
      schermo.blit(SEMAFORI_IMG[semaforo.color], SEMAFORI_POS[semaforo_name])
    

  tick+=1
  # Aggiorna il display limitando a 60 FPS
  pygame.display.flip()
  orologio.tick(60)

pygame.quit()
sys.exit()