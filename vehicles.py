import pygame
import time
import random
import c #file with all constant values


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, direction, lane, delay):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.birth = time.time()
        self.delay = delay
        self.lane = lane
        self.next_delay = -1
        dummy = random.randint(1, 100)
        if self.direction == 'W':
            if dummy % 2 == 1:
                self.image = pygame.image.load('images/truck_l.png')
            else:
                self.image = pygame.image.load('images/truck2_l.png')
            self.rect = self.image.get_rect()
            if self.delay < 0:
                self.delay = 0
                self.rect.left = random.randint(250, 300)
            else:
                self.rect.left = c.WIDTH
        elif self.direction == 'E':
            if dummy % 2 == 1:
                self.image = pygame.image.load('images/truck_r.png')
            else:
                self.image = pygame.image.load('images/truck2_r.png')
            self.rect = self.image.get_rect()
            if self.delay < 0:
                self.delay = 0
                self.rect.right = random.randint(50, 100)
            else:
                self.rect.right = 0
        self.rect.top = lane*c.LANE_HEIGHT
        self.columns = self.set_columns()

    def update(self):
        if self.delay == 0:
            if self.direction == 'W':
                if self.rect.right < 0 and self.next_delay >= 0:
                    self.delay = self.next_delay
                    self.next_delay = -1
                    self.birth = time.time()
                    self.rect.left = c.WIDTH
                else:
                    self.rect.x += -c.VEHICLE_SPEED
            elif self.direction == 'E':
                if self.rect.left > c.WIDTH and self.next_delay >= 0:
                    self.delay = self.next_delay
                    self.next_delay = -1
                    self.birth = time.time()
                    self.rect.right = 0
                else:
                    self.rect.x += +c.VEHICLE_SPEED

        if self.delay != 0 and time.time() - self.birth >= self.delay:
            self.delay = 0
            self.birth = time.time()
        self.set_columns()

    def set_columns(self):
        a = self.rect.left // c.BLOCK_WIDTH
        b = self.rect.right // c.BLOCK_WIDTH
        if abs(a-b) == 2:
            middle = abs(a)+1
            self.columns = (a, middle, b)
        else:
            self.columns = (a, b)
        return self.columns
