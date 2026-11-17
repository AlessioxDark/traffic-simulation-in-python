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

GRUPPI_SEMAFORI = {
    "OVEST": (692, 204, "nord", "nord_sx"),
    "NORD": (384, 204, "ovest", "ovest_sx"),
    "EST": (384, 456, "sud", "sud_sx"),
    "SUD": (692, 456, "est", "est_sx"),
}

GAP_SEMAFORI = 6

font_direzioni = pygame.font.SysFont(
    "Arial", 18, bold=True
)

# Dimensioni delle immagini dei semafori
SEMAFORO_W, SEMAFORO_H = next(
    iter(SEMAFORI_IMG.values())
).get_size()

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
    
  # VISUALIZZAZIONE DEI QUATTRO GRUPPI SEMAFORICI

  for direzione, dati in GRUPPI_SEMAFORI.items():

      centro_x, y, nome_normale, nome_sx = dati

      # Recuperiamo i due semafori
      sem_normale = traffic_controller.semafori[nome_normale]
      sem_sx = traffic_controller.semafori[nome_sx]

      img_normale = SEMAFORI_IMG[sem_normale.color]
      img_sx = SEMAFORI_IMG[sem_sx.color]

      # Calcoliamo la larghezza complessiva della coppia
      larghezza_totale = SEMAFORO_W * 2 + GAP_SEMAFORI

      # Posizionamento affiancato e centrato
      x_inizio = centro_x - larghezza_totale // 2

      # Semaforo normale
      schermo.blit(
          img_normale,
          (x_inizio, y)
      )

      # Semaforo svolta a sinistra
      schermo.blit(
          img_sx,
          (x_inizio + SEMAFORO_W + GAP_SEMAFORI, y)
      )

      # Nome della direzione
      testo = font_direzioni.render(
          direzione,
          True,
          (255, 255, 255)
      )

      testo_rect = testo.get_rect(
          midbottom=(centro_x, y - 6)
      )

      # Sfondo per rendere leggibile la scritta
      sfondo = testo_rect.inflate(10, 6)

      pygame.draw.rect(
          schermo,
          (35, 35, 35),
          sfondo,
          border_radius=4
      )

      schermo.blit(testo, testo_rect)

  tick+=1
  # Aggiorna il display limitando a 60 FPS
  pygame.display.flip()
  orologio.tick(60)

pygame.quit()
sys.exit()