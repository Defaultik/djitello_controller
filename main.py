import pygame, cv2

from datetime import datetime
from djitellopy import Tello


def GetKey(key):
    for event in pygame.event.get():
        pass

    if pygame.key.get_pressed()[getattr(pygame, 'K_{}'.format(key))]:
        return True
    
    return False


def GetKeyOnce(key):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == getattr(pygame, 'K_{}'.format(key)):
                return True
        else:
            pass

        return False


class Drone:
    def in_fly(self):
        if self.drone.get_flight_time:
            return True
        
        return False


    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Drone Control")

        self.screen = pygame.display.set_mode([960, 720])

        self.drone = Tello()

        self.control = False
        self.send_rc_control = False

    
    def start(self):
        self.drone.connect()

        self.drone.streamoff()
        self.drone.streamon()

        frame_read = self.drone.get_frame_read()
        while True:
            frame = frame_read.frame

            cv2.putText(frame, str(self.drone.get_battery()) + "%", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, datetime.now().strftime("%H:%M:%S"), (10, 65), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

            if GetKey("HOME"):
                print("Screenshot successful")

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imwrite(datetime.now().strftime("H%H.M%M.S%S") + ".jpg", frame)

            frame = pygame.surfarray.make_surface(frame)
            frame = pygame.transform.rotate(frame, 90)
            frame = pygame.transform.flip(frame, False, True)

            self.screen.blit(frame, (0, 0))

            pygame.time.Clock().tick(30)
            pygame.display.update()

            self.controller()

    
    def controller(self):
        self.speed = 60
        self.fb, self.lr, self.ud, self.cw = 0, 0, 0, 0

        if GetKey("t"):
            self.drone.takeoff()
            self.send_rc_control = True
        elif GetKey("l"):
            self.drone.land()
            self.send_rc_control = False

        if self.in_fly():
            if GetKey("LSHIFT"):
                self.speed += 40
            else:
                self.speed = 60

            if GetKey("w"):
                self.fb = self.speed

            if GetKey("a"):
                self.lr = -self.speed

            if GetKey("s"):
                self.fb = -self.speed

            if GetKey("d"):
                self.lr = self.speed

            if GetKey("UP"):
                self.ud = self.speed

            if GetKey("DOWN"):
                self.ud = -self.speed

            if GetKey("RIGHT"):
                self.cw = self.speed

            if GetKey("LEFT"):
                self.cw = -self.speed

            if self.send_rc_control:
                self.drone.send_rc_control(self.lr, self.fb, self.ud, self.cw)


if __name__ == "__main__":
    Drone().start()