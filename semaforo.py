import pygame
class Semaforo:
    def __init__(self,color):
        self.color = color

    def change_color(self,color):
        self.color = color
        
FPS = 60
T_VERDE_DRITTO_NS = 8 * FPS
T_GIALLO_DRITTO_NS = 10 * FPS
T_VERDE_SX_NS = 14 * FPS
T_GIALLO_SX_NS = 16 * FPS
T_ALLRED_1 = 18 * FPS
T_VERDE_DRITTO_EO = 26 * FPS
T_GIALLO_DRITTO_EO = 28 * FPS
T_VERDE_SX_EO = 32 * FPS
T_GIALLO_SX_EO = 34 * FPS
T_FINE_CICLO = 36 * FPS
class GestoreTraffico:
    def __init__(self):
        self.semafori = {
        "nord": Semaforo("RED"),
        "nord_sx": Semaforo("RED_LEFT"),
        "sud": Semaforo("RED"),
        "sud_sx": Semaforo("RED_LEFT"),
        "est": Semaforo("RED"),
        "est_sx": Semaforo("RED_LEFT"),
        "ovest": Semaforo("RED"),
        "ovest_sx": Semaforo("RED_LEFT"),
    }        
        self.time = 0

    def aggiorna(self):
        if self.time == 0:
            self.semafori["nord"].change_color("GREEN")
            self.semafori["sud"].change_color("GREEN")
            self.semafori["nord_sx"].change_color("RED_LEFT")
            self.semafori["sud_sx"].change_color("RED_LEFT")

            # 2. Giallo Dritto N-S
        elif self.time == T_VERDE_DRITTO_NS:
            self.semafori["nord"].change_color("YELLOW")
            self.semafori["sud"].change_color("YELLOW")

            # 3. Verde Sinistra N-S (il dritto diventa rosso, la sinistra diventa verde)
        elif self.time == T_GIALLO_DRITTO_NS:
            self.semafori["nord"].change_color("RED")
            self.semafori["sud"].change_color("RED")
            self.semafori["nord_sx"].change_color("GREEN_LEFT")
            self.semafori["sud_sx"].change_color("GREEN_LEFT")

            # 4. Giallo Sinistra N-S
        elif self.time == T_VERDE_SX_NS:
            self.semafori["nord_sx"].change_color("YELLOW_LEFT")
            self.semafori["sud_sx"].change_color("YELLOW_LEFT")

            # 5. All-Red / Tutto Rosso 1
        elif self.time == T_GIALLO_SX_NS:
            self.semafori["nord_sx"].change_color("RED_LEFT")
            self.semafori["sud_sx"].change_color("RED_LEFT")

            # 6. Verde Dritto E-O
        elif self.time == T_ALLRED_1:
            self.semafori["est"].change_color("GREEN")
            self.semafori["ovest"].change_color("GREEN")

            # 7. Giallo Dritto E-O
        elif self.time == T_VERDE_DRITTO_EO:
            self.semafori["est"].change_color("YELLOW")
            self.semafori["ovest"].change_color("YELLOW")

            # 8. Verde Sinistra E-O
        elif self.time == T_GIALLO_DRITTO_EO:
            self.semafori["est"].change_color("RED")
            self.semafori["ovest"].change_color("RED")
            self.semafori["est_sx"].change_color("GREEN_LEFT")
            self.semafori["ovest_sx"].change_color("GREEN_LEFT")

            # 9. Giallo Sinistra E-O
        elif self.time == T_VERDE_SX_EO:
            self.semafori["est_sx"].change_color("YELLOW_LEFT")
            self.semafori["ovest_sx"].change_color("YELLOW_LEFT")

            # 10. All-Red Finale
        elif self.time == T_GIALLO_SX_EO:
            self.semafori["est_sx"].change_color("RED_LEFT")
            self.semafori["ovest_sx"].change_color("RED_LEFT")

        

        elif self.time == T_FINE_CICLO:
            self.time = -1


        self.time+=1

    def get_semaforo(self, provenienza, manovra):

        if manovra == "sinistra":
            nome = provenienza + "_sx"
        else:
            nome = provenienza

        return self.semafori[nome]


def can_enter(self, provenienza, manovra):

    semaforo = self.get_semaforo(provenienza, manovra)

    if manovra == "sinistra":
        return semaforo.color == "GREEN_LEFT"

    return semaforo.color == "GREEN"




semaforo_rosso = pygame.image.load(
    r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\red_light.png"
).convert_alpha()
semaforo_giallo = pygame.image.load(
    r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\yellow_light.png"
).convert_alpha()
semaforo_verde = pygame.image.load(
    r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\green_light.png"
).convert_alpha()
semaforo_verde_sinistra = pygame.image.load(
    r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\green_light_left.png"
).convert_alpha()
semaforo_giallo_sinistra = pygame.image.load(
    r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\yellow_light_left.png"
).convert_alpha()
semaforo_rosso_sinistra = pygame.image.load(
    r"C:\Users\aless\Desktop\Progetti Personali\traffic_system\assets\red_light_left.png"
).convert_alpha()


SEMAFORI_IMG = {"RED":semaforo_rosso,
    "YELLOW":semaforo_giallo,
    "GREEN":semaforo_verde,
    "GREEN_LEFT":semaforo_verde_sinistra,
    "RED_LEFT":semaforo_rosso_sinistra,
    "YELLOW_LEFT":semaforo_giallo_sinistra,
    
} 
traffic_controller = GestoreTraffico()