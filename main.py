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
from percorsi import crea_percorso,PARTENZE

Running = True




LINEE_DI_ARRESTO = [[14*32,9*32],[14*32,10*32],[19*32,11*32],[19*32,12*32],[17*32,8*32],[18*32,8*32],[15*32,13*32],[16*32,13*32]]
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

  for provenienza in ("nord", "sud", "est", "ovest"):

    for corsia in ("destra", "sinistra"):

        manovre = (
            "dritto", "destra"
        ) if corsia == "destra" else (
            "dritto", "sinistra"
        )

        for manovra in manovre:

            punti, direzione = crea_percorso(
                provenienza,
                corsia,
                manovra
            )

            colore = {
                "dritto": (0, 255, 0),
                "destra": (255, 180, 0),
                "sinistra": (255, 0, 0)
            }[manovra]

            punti_disegno = [
                (round(x), round(y))
                for x, y in punti
            ]

            pygame.draw.lines(
                schermo,
                colore,
                False,
                punti_disegno,
                2
            )


  
  for auto in lista_auto:  
    auto.aggiorna()

    schermo.blit(
        auto.img,
        (round(auto.x), round(auto.y))
    )
    
    
  if tick % (10*60) == 0:
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