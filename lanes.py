import pygame
import random
import vehicles
import c #file with all constant values


class Lane(pygame.sprite.Sprite):
    def __init__(self, y_position, lane_no, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane_no = lane_no
        self.direction = direction
        self.image = pygame.image.load('images/lane.png')
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = y_position
        self.my_vehicles = pygame.sprite.Group()
        # lanes with traffic have vehicles with delays added:
        if self.is_traffic_lane():
            self.number_of_vehicles = random.randint(c.MIN_VEHICLES, c.MAX_VEHICLES)
            self.delays_init()

    def delays_init(self):
            delays = [random.uniform(0, 1.5)]
            if delays[0] < 1:
                delays[0] *= -1
            for i in range(0, self.number_of_vehicles-1):
                delays.append(delays[i] + random.uniform(1, 2.5))
            for i in range(0, self.number_of_vehicles):
                self.my_vehicles.add(vehicles.Vehicle(self.direction, self.lane_no, delays[i]))

    def update(self):
        for car in self.my_vehicles.sprites():
            car.update()
        self.spawn_check()

    def draw(self, window):
        self.my_vehicles.draw(window)

    def collision_detector(self, sprite1):
        if pygame.sprite.spritecollideany(sprite1, self.my_vehicles) is not None:
            return True
        else:
            return False

    def spawn_check(self):
        if self.is_traffic_lane():          # check if cars can move on this lane
            flag = False                 # the flag is True when all cars have already 'appeared on the screen'
            for car in self.my_vehicles.sprites():
                flag = True                 # flag=True temporarily. if any of the cars is still 'behind the borders'
                if self.direction == 'W':   # (didn't start yet and is not on the screen), it will turn to False
                    if car.rect.right >= c.WIDTH:
                        flag = False
                if self.direction == 'E':
                    if car.rect.left <= 0:
                        flag = False
                if flag:
                    if car.next_delay != -1:    # if the car has already a next_delay chosen, we turn flag to False,
                        flag = False            # so the chosen delay will stay and won't be changed.

            if flag:    # if all cars have already appeared and new delays may be chosen:
                new_delays = [random.uniform(0.1, 1.5)]
                for i in range(0, self.number_of_vehicles-1):
                    new_delays.append(new_delays[i] + random.uniform(1, 2.5))
                n = 0
                for car in self.my_vehicles.sprites():
                    car.next_delay = new_delays[n]
                    n += 1

    def is_traffic_lane(self):          # true if cars can move on this lane
        if self.lane_no > 0 and self.lane_no != c.CONE_LANE and self.lane_no < c.LANE_QUANTITY -1:
            return True
        else:
            return False

