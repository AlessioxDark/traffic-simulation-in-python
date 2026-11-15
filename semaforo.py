import pygame
class Semaforo:
    def __init__(self,color,img):
        self.color = color
        self.img = img

    def change_color(self,color):
        self.color = color
        match color:
            case "RED":
                self.img = semaforo_rosso
            case "YELLOW":    
                self.img = semaforo_giallo
            case "GREEN":
                self.img = semaforo_verde
            case "GREEN_LEFT":
                self.img = semaforo_verde_sinistra

FPS = 60
SEC_GIALLO_NS = 12
SEC_ROSSO_NS = 15
SEC_VERDE_EO = 18
SEC_GIALLO_EO = 23
SEC_ROSSO_EO = 26
SEC_FINE_CICLO = 30
class GestoreTraffico:
    def __init__(self,semaforo_nord,semaforo_sud,semaforo_est,semaforo_ovest):
        self.current_phase = 1
        self.semaforo_nord = semaforo_nord
        self.semaforo_sud = semaforo_sud
        self.semaforo_est = semaforo_est
        self.semaforo_ovest = semaforo_ovest
        self.time = 0

    def aggiorna(self):
        if self.time == 0:
            print("fase 1")
            self.semaforo_nord.change_color("GREEN")
            self.semaforo_sud.change_color("GREEN")

        elif self.time == SEC_GIALLO_NS * FPS:
            print("fase 2")
            self.semaforo_nord.change_color("GREEN_LEFT")
            self.semaforo_sud.change_color("YELLOW")

        elif self.time == SEC_ROSSO_NS * FPS:
            print("fase 3")
            self.semaforo_nord.change_color("RED")
            self.semaforo_sud.change_color("RED")

        elif self.time == SEC_VERDE_EO * FPS:
            print("fase 4")
            self.semaforo_ovest.change_color("GREEN")
            self.semaforo_est.change_color("GREEN")

        elif self.time == SEC_GIALLO_EO * FPS:
            print("fase 5")
            self.semaforo_ovest.change_color("YELLOW")
            self.semaforo_est.change_color("YELLOW")

        elif self.time == SEC_ROSSO_EO * FPS:
            print("fase 6")
            self.semaforo_ovest.change_color("RED")
            self.semaforo_est.change_color("RED")

        elif self.time == SEC_FINE_CICLO * FPS:
            self.time = -1


        print("TIME",self.time)
        self.time+=1

    # def aggiorna(self):
    #     if self.time == 0:
    #         print("fase 1")
    #         self.semaforo_nord.change_color("GREEN")
    #         self.semaforo_sud.change_color("GREEN")

    #     elif self.time == SEC_GIALLO_NS * FPS:
    #         print("fase 2")
    #         self.semaforo_nord.change_color("YELLOW")
    #         self.semaforo_sud.change_color("YELLOW")

    #     elif self.time == SEC_ROSSO_NS * FPS:
    #         print("fase 3")
    #         self.semaforo_nord.change_color("RED")
    #         self.semaforo_sud.change_color("RED")

    #     elif self.time == SEC_VERDE_EO * FPS:
    #         print("fase 4")
    #         self.semaforo_ovest.change_color("GREEN")
    #         self.semaforo_est.change_color("GREEN")

    #     elif self.time == SEC_GIALLO_EO * FPS:
    #         print("fase 5")
    #         self.semaforo_ovest.change_color("YELLOW")
    #         self.semaforo_est.change_color("YELLOW")

    #     elif self.time == SEC_ROSSO_EO * FPS:
    #         print("fase 6")
    #         self.semaforo_ovest.change_color("RED")
    #         self.semaforo_est.change_color("RED")

    #     elif self.time == SEC_FINE_CICLO * FPS:
    #         self.time = -1


    #     print("TIME",self.time)
    #     self.time+=1




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

semaforo_nord = Semaforo("RED",semaforo_rosso)
semaforo_sud = Semaforo("RED",semaforo_rosso)
semaforo_est = Semaforo("RED",semaforo_rosso)
semaforo_ovest = Semaforo("RED",semaforo_rosso)