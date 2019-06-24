import pygame
import time
import random
import player
import lanes
import blocks
import c    #file with all constant values


# function displaying a message in case of losing/winning the game
def end_screen(if_won, window):
    font = pygame.font.Font('freesansbold.ttf', 32)
    if if_won is True:
        displayed_text = 'You won! Congrats!'
        color_1 = c.RED
        color_2 = c.WHITE
    else:
        displayed_text = 'You lost!'
        color_1 = c.RED
        color_2 = c.BLACK
    text = font.render(displayed_text, True, color_1, color_2)
    textRect = text.get_rect()
    textRect.center = (c.WIDTH // 2, c.HEIGHT // 2)
    window.blit(text, textRect)
    pygame.display.update()
    start_time = time.time()
    elapsed_time = 0
    while elapsed_time < 3:
        elapsed_time = time.time() - start_time


# the game loop is in the main function - it didn't make much sense to put it in a separate class
def main():
    # -------------------------- INITIALIZING ALL THE NECESSARY VALUES --------------------------
    pygame.init()
    window = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
    pygame.display.set_caption("Frogger")

    run = True

    # initializing lanes and adding them to the sprite group all_lanes
    # all directions are based on:
    # N - North (up the screen), S - South (down), E - East (right), W - West (left),
    direction_list = ['W', 'E']
    all_lanes = pygame.sprite.Group()
    for i in range(1, c.LANE_QUANTITY+1):
            all_lanes.add(lanes.Lane(c.LANE_HEIGHT*i, i, random.choice(direction_list)))

    # initializing goals and adding them to the sprite group all_goals
    all_goals = pygame.sprite.Group()
    for i in range(0, c.COLUMN_QUANTITY):
            all_goals.add(blocks.Block(0, i, 'D'))

    # initializing cones with random positions (columns) on the CONE_LANE:
    list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    cone1 = blocks.Block(c.CONE_LANE, list1.pop(random.randint(0, len(list1)-1)), 'C')
    cone2 = blocks.Block(c.CONE_LANE, list1.pop(random.randint(0, len(list1)-1)), 'C')
    cone3 = blocks.Block(c.CONE_LANE, list1.pop(random.randint(0, len(list1)-1)), 'C')
    cone4 = blocks.Block(c.CONE_LANE, list1.pop(random.randint(0, len(list1)-1)), 'C')
    # initializing two cones on the borders of the bottom (last) lane:
    cone5 = blocks.Block(c.LANE_QUANTITY-1, 0, 'C')
    cone6 = blocks.Block(c.LANE_QUANTITY-1, c.COLUMN_QUANTITY-1, 'C')
    # sprite group for cones:
    cones = pygame.sprite.Group()
    cones.add(cone1, cone2, cone3, cone4, cone5, cone6)

    # initializing player (the frog)
    frog = player.Player()

    # initializing sprite groups for player and goal blocks (needed for drawing)
    goals = pygame.sprite.Group()
    goals.add(all_goals)
    players = pygame.sprite.Group()
    players.add(frog)

    next_movement = pygame.time.get_ticks() + c.PLAYER_DELAY        # value for limiting player's movements
    paused = False                                                  # (so that the frog doesn't move too fast

    # -------------------------- GAME LOOP --------------------------
    while run:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:     # game may be paused with 'P' key
                    if not paused:
                        paused = True
                        print("\nPause ON")
                    else:
                        paused = False
                        print("Pause OFF")

        if not paused:
            all_lanes.update()

            if next_movement <= pygame.time.get_ticks():
                keystate = pygame.key.get_pressed()     # reading player's key input
                frog.update(cones, keystate)
                next_movement = pygame.time.get_ticks() + c.PLAYER_DELAY

            # graphics (drawing):
            window.fill(c.BLACK)
            all_lanes.draw(window)
            cones.draw(window)
            for lane_iter in all_lanes.sprites():
                lane_iter.draw(window)
            goals.draw(window)
            players.draw(window)

            # check if the frog collided with obstacle (if yes - game lost)
            for lane_iter in all_lanes.sprites():
                if lane_iter.collision_detector(frog):
                    end_screen(False, window)
                    run = False

            # else, if the frog steppend on the goal block - game won
            if pygame.sprite.spritecollideany(frog, all_goals) is not None:
                end_screen(True, window)
                run = False

            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()