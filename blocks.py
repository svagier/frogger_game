import pygame
import c #file with all constant values


class Block(pygame.sprite.Sprite):
    def __init__(self, lane, column, type):
        pygame.sprite.Sprite.__init__(self)
        if type == 'C':
            self.image = pygame.image.load('images/cone.png')
        else:
            self.image = pygame.image.load('images/goal.png')
        self.rect = self.image.get_rect()
        self.rect.top = lane*c.LANE_HEIGHT
        self.rect.left = column * c.VEHICLE_WIDTH/2
        self.lane_no = lane
        self.column_no = column


