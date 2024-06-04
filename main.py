import pygame
import time
import cv2

from djitellopy import Tello


def key_pressed(key):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == getattr(pygame, 'K_{}'.format(key)):
                return True
    
    return False


def key_holded(key):
    for event in pygame.event.get():
        pass

    if pygame.key.get_pressed()[getattr(pygame, 'K_{}'.format(key))]:
        return True
    
    return False


class Drone:
    def __init__(self):
        self.drone = Tello()

        self.drone.connect()
        self.send_rc_control = False
        
        self.drone.streamoff()
        self.drone.streamon()

        pygame.init()
        pygame.display.set_caption("Drone Control")

        self.screen = pygame.display.set_mode([960, 720])

    
    def in_fly(self):
        if self.drone.get_height():
            return True
        
        return False


    def start(self):
        frame_read = self.drone.get_frame_read()
        while True:
            self.frame = frame_read.frame

            cv2.putText(self.frame, str(self.drone.get_battery()) + "%", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(self.frame, time.strftime("%H:%M:%S"), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

            self.frame = pygame.surfarray.make_surface(self.frame)
            self.frame = pygame.transform.rotate(self.frame, 90)
            self.frame = pygame.transform.flip(self.frame, False, True)
            
            self.control()

            self.screen.blit(self.frame, (0, 0))
            pygame.time.Clock().tick(30)
            pygame.display.update()

    
    def control(self):
        fb, lr, ud, cw = 0, 0, 0, 0
        speed = 60

        if key_pressed("SPACE"):
            if self.in_fly():
                self.drone.land()
                self.send_rc_control = False
            else:
                self.drone.takeoff()
                self.send_rc_control = True

        if self.send_rc_control:
            if key_holded("LSHIFT"):
                speed += 40
            else:
                speed = 60

            if key_holded("w"):
                fb = speed

            if key_holded("a"):
                lr = -speed

            if key_holded("s"):
                fb = -speed

            if key_holded("d"):
                lr = speed

            if key_holded("UP"):
                ud = speed

            if key_holded("DOWN"):
                ud = -speed

            if key_holded("RIGHT"):
                cw = speed

            if key_holded("LEFT"):
                cw = -speed

            self.drone.send_rc_control(lr, fb, ud, cw)

    
if __name__ == "__main__":
    Drone().start()