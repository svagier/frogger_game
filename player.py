import pygame
import c #file with all constant values


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/frog_up.png')
        self.rect = self.image.get_rect()
        self.rect.left = (c.COLUMN_QUANTITY//2)*c.VEHICLE_WIDTH/2
        self.rect.bottom = c.HEIGHT
        self.speedx = 0
        self.speedy = 0
        self.lane_no = self.set_lane()
        self.column_no = self.set_column()
        self.rect.top = self.lane_no*c.LANE_HEIGHT

    def update(self, obstacles, keystate):
        self.speedx = 0
        self.speedy = 0
        self.movement(keystate)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pygame.sprite.spritecollideany(self, obstacles) is not None:
            self.rect.x -= self.speedx
            self.rect.y -= self.speedy
        self.set_lane()
        self.set_column()

    def movement(self, keystate):
        if keystate[pygame.K_UP]:
            self.image = pygame.image.load('images/frog_up.png')
            if self.rect.top != 0:
                self.speedy = -c.PLAYER_SPEED
        elif keystate[pygame.K_DOWN]:
            self.image = pygame.image.load('images/frog_down.png')
            if self.rect.bottom != c.HEIGHT:
                self.speedy += c.PLAYER_SPEED
        elif keystate[pygame.K_LEFT]:
            self.image = pygame.image.load('images/frog_left.png')
            if self.rect.left != 0:
                self.speedx = -c.PLAYER_SPEED
        elif keystate[pygame.K_RIGHT]:
            self.image = pygame.image.load('images/frog_right.png')
            if self.rect.right != c.WIDTH:
                self.speedx = c.PLAYER_SPEED

    def set_column(self):
        self.column_no = self.rect.left // c.BLOCK_WIDTH
        return self.column_no

    def set_lane(self):
            self.lane_no = self.rect.top // c.LANE_HEIGHT
            return self.lane_no

