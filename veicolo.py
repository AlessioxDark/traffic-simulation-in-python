import math
from percorsi import crea_percorso
from percorsi import PARTENZE
import semaforo
import pygame
import random
from semaforo import traffic_controller

CAR_WIDTH = 32
CAR_HEIGHT = 32
DISTANZA_SICUREZZA = 40

lista_auto = []

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
CARS = (blue_car,green_car,gray_car,black_car)

class Car:

    def __init__(
        self, x, y, direction, velocity, img,
        semaforo, provenienza, corsia, manovra
    ):

        self.x = float(x)
        self.y = float(y)

        # Centro dell'automobile
        self.cx = self.x + CAR_WIDTH / 2
        self.cy = self.y + CAR_HEIGHT / 2

        self.dir = direction
        self.velocity = velocity

        self.original_img = img
        self.img = img
        self.last_angle = None

        self.provenienza = provenienza
        self.corsia = corsia
        self.manovra = manovra

        self.semaforo = semaforo
        self.ruota_immagine(*self.dir)

        # Linea di arresto
        self.stop_point = PARTENZE[
            (provenienza, corsia)
        ]

        # Traiettoria già scelta
        self.traiettoria, self.direzione_uscita = crea_percorso(
            provenienza,
            corsia,
            manovra
        )

        self.punto_corrente = 0

        self.stato = "AVVICINAMENTO"

    def aggiorna_posizione(self):

        self.x = self.cx - CAR_WIDTH / 2
        self.y = self.cy - CAR_HEIGHT / 2

    def ruota_immagine(self, dx, dy):

        # L'immagine originale è orientata verso il basso.
        angolo = round(math.degrees(math.atan2(dx, dy)))

        # Evita trasformazioni inutili.
        if angolo != self.last_angle:

            self.img = pygame.transform.rotate(
                self.original_img,
                angolo
            )

            self.last_angle = angolo

    def avvicinamento(self):
        dx, dy = self.dir

        # Distanza dalla linea di arresto
        distanza_stop = (
            (self.stop_point[0] - self.cx) * dx
            + (self.stop_point[1] - self.cy) * dy
        )

        distanza_stop = max(0, distanza_stop)

    # Velocità massima consentita
        passo = min(self.velocity, distanza_stop)

        # Controlliamo la macchina davanti
        distanza_auto = self.distanza_auto_davanti()
        
        if distanza_auto is not None:

            spazio_disponibile = (
                distanza_auto - DISTANZA_SICUREZZA
            )

            passo = min(
                passo,
                max(0, spazio_disponibile)
            )

        # Movimento
        self.cx += dx * passo
        self.cy += dy * passo

            # Verifichiamo se abbiamo raggiunto la linea
        if distanza_stop <= passo + 0.000001:

                self.cx, self.cy = self.stop_point

                self.stato = "ATTESA"

    def segui_traiettoria(self):

        spazio = self.velocity

        while spazio > 0 and self.punto_corrente < len(self.traiettoria) - 1:

            target = self.traiettoria[self.punto_corrente + 1]

            dx = target[0] - self.cx
            dy = target[1] - self.cy

            distanza = math.hypot(dx, dy)

            if distanza < 0.0001:

                self.punto_corrente += 1
                continue

            self.ruota_immagine(dx, dy)

            passo = min(spazio, distanza)

            self.cx += dx / distanza * passo
            self.cy += dy / distanza * passo

            spazio -= passo

            if passo >= distanza:
                self.punto_corrente += 1

        # La curva è terminata
        if self.punto_corrente >= len(self.traiettoria) - 1:

            self.cx, self.cy = self.traiettoria[-1]

            self.dir = self.direzione_uscita

            self.ruota_immagine(*self.dir)

            self.stato = "USCITA"


    def distanza_auto_davanti(self):

        dx, dy = self.dir
        distanza_minima = None

        for altra in lista_auto:

            if altra == self:
                continue

            if (altra.provenienza != self.provenienza
                    or altra.corsia != self.corsia):
                continue

            delta_x = altra.cx - self.cx
            delta_y = altra.cy - self.cy

            longitudinale = delta_x * dx + delta_y * dy

            laterale = -delta_x * dy + delta_y * dx

            if longitudinale > 0 and abs(laterale) < 20:

                if (distanza_minima is None
                        or longitudinale < distanza_minima):

                    distanza_minima = longitudinale

        return distanza_minima
    
    def aggiorna(self):
       
        if self.stato == "AVVICINAMENTO":
           
            self.avvicinamento()

        elif self.stato == "ATTESA":

            luce_richiesta = (
                "GREEN_LEFT"
                if self.manovra == "sinistra"
                else "GREEN"
            )

            if self.semaforo.color == luce_richiesta:

                self.stato = "ATTRAVERSAMENTO"

                self.segui_traiettoria()

        elif self.stato == "ATTRAVERSAMENTO":

            self.segui_traiettoria()

        elif self.stato == "USCITA":

            self.cx += self.dir[0] * self.velocity
            self.cy += self.dir[1] * self.velocity

            self.ruota_immagine(*self.dir)

        self.aggiorna_posizione()

def scegli_manovra(corsia):

    if corsia == "destra":
        return random.choice(["dritto", "destra"])

    else:
        return random.choice(["dritto", "sinistra"])


def aggiungi_auto(x, y, direction, img, provenienza, corsia):

    manovra = scegli_manovra(corsia)

    if manovra == "sinistra":
        nome_semaforo = provenienza + "_sx"
    else:
        nome_semaforo = provenienza

    semaforo = traffic_controller.semafori[nome_semaforo]

    car = Car(
        x, y,
        direction,
        1,
        img,
        semaforo,
        provenienza,
        corsia,
        manovra
    )

    lista_auto.append(car)

def genera_auto():

    # AUTO PROVENIENTI DA NORD
    for colonna in (15, 16):

        corsia = "destra" if colonna == 15 else "sinistra"

        img = random.choice(CARS)

        aggiungi_auto(
            colonna * 32, 0,
            (0, 1),
            img,
            "nord",
            corsia
        )

    # AUTO PROVENIENTI DA SUD
    for colonna in (17, 18):

        corsia = "sinistra" if colonna == 17 else "destra"

        img = random.choice(CARS)

        aggiungi_auto(
            colonna * 32, 20 * 32,
            (0, -1),
            img,
            "sud",
            corsia
        )

    # AUTO PROVENIENTI DA OVEST
    for riga in (11, 12):
        corsia = "destra" if riga == 12 else "sinistra"

        img = random.choice(CARS)

        aggiungi_auto(
            0, riga * 32,
            (1, 0),
            img,
            "ovest",
            corsia
        )

    # AUTO PROVENIENTI DA EST
    for riga in (9, 10):

        corsia = "destra" if riga == 9 else "sinistra"

        img = random.choice(CARS)

        aggiungi_auto(
            32 * 32, riga * 32,
            (-1, 0),
            img,
            "est",
            corsia
        )