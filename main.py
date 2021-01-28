# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pygame
import random

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1280
HEIGHT = 720
SPEED = 6
DASH_SPEED = 5
REG_SPEED = 2
TITLE = "<George's Jungle Jam>"
background_image = pygame.image.load("./assets/background.jpg")
background_image = pygame.transform.scale(background_image, (1280, 800))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Initialize Sprite
        self.image = pygame.image.load("./assets/monkey.png")
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2 - 97.5
        self.rect.y = HEIGHT - self.rect.height

        # Vector
        self.vel_x = 0
        self.monkey_speed = 0

    def update(self):
        self.rect.x += self.vel_x * self.monkey_speed


class Banana(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Initialize Sprite
        self.image = pygame.image.load("./assets/banana.png")
        self.image = pygame.transform.scale(self.image, (112, 84))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = 0

        # Vector
        self.vel_y = 6

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.y == HEIGHT - self.rect.height:
            self.kill()


class Coconut(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Initialize Sprite
        self.image = pygame.image.load("./assets/coconut.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = 0

        # Vector
        self.vel_y = 10

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.y == HEIGHT - self.rect.height:
            self.kill()


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    banana_spawn_time = 1000
    coconut_spawn_time = random.randrange(8000, 12000)
    last_time_banana_spawned = pygame.time.get_ticks()
    last_time_coconut_spawned = pygame.time.get_ticks()
    game_over = False

    # Score
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_score_x = 30
    text_score_y = 10

    def show_score(x, y):
        score = font.render("Score: " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    # Lives
    lives_value = 3
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_lives_x = 1120
    text_lives_y = 10

    def show_lives(x, y):
        score = font.render("Lives: " + str(lives_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    # ----- Sprites
    all_sprites_group = pygame.sprite.RenderUpdates()
    bananas_group = pygame.sprite.Group()
    coconuts_group = pygame.sprite.Group()

    # ----- Player
    player = Player()
    all_sprites_group.add(player)

    # ----- Banana
#     for i in range(50):
#         banana = Banana()
#         all_sprites_group.add(banana)
#         bananas_group.add(banana)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if not game_over:

                if keys[pygame.K_LSHIFT]:
                    player.monkey_speed = DASH_SPEED
                else:
                    player.monkey_speed = REG_SPEED

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.vel_x = SPEED
                    elif event.key == pygame.K_LEFT:
                        player.vel_x = -SPEED

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.vel_x < 0:
                        player.vel_x = 0
                    if event.key == pygame.K_RIGHT and player.vel_x > 0:
                        player.vel_x = 0

        # ----- LOGIC
        all_sprites_group.update()
        
        # While the game is running
        if not game_over:
            # banana spawn
            if pygame.time.get_ticks() > last_time_banana_spawned + banana_spawn_time:
                # set the new time to this current time
                last_time_banana_spawned = pygame.time.get_ticks()
                # spawn banana
                banana = Banana()
                all_sprites_group.add(banana)
                bananas_group.add(banana)

            # coconut spawn
            if pygame.time.get_ticks() > last_time_coconut_spawned + coconut_spawn_time:
                last_time_coconut_spawned = pygame.time.get_ticks()
                # spawn coconut
                coconut = Coconut()
                all_sprites_group.add(coconut)
                coconuts_group.add(coconut)
            
        # check if banana has collided with player
            for banana in bananas_group:
                if banana.rect.top < 0:
                    banana.kill()

                # Player collision
                bananas_collected = pygame.sprite.spritecollide(player, bananas_group, True)
                if len(bananas_collected) > 0:
                    banana.kill()
                    score_value += 1

                # banana hits ground
                if banana.rect.y == HEIGHT - banana.rect.height:
                    lives_value -= 1

        # check if coconut has collied with player
            for coconut in coconuts_group:
                if coconut.rect.top < 0:
                    coconut.kill()

                # Player collision
                coconut_collected = pygame.sprite.spritecollide(player, coconuts_group, True)
                if len(coconut_collected) > 0:
                    coconut.kill()
                    score_value += 3

                # coconut hits ground
                if coconut.rect.y == HEIGHT - coconut.rect.height:
                    lives_value -= 1

        # Game over
        if lives_value <= 0:
            game_over = True

        # ----- DRAW
        screen.blit(background_image, (0,0))
        dirty_rectangles = all_sprites_group.draw(screen)
        
        # ----- UPDATE
        show_score(text_score_x, text_score_y)
        show_lives(text_lives_x, text_lives_y)
        pygame.display.update(dirty_rectangles)
        pygame.display.flip()
        clock.tick(60)

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

    pygame.quit()


if __name__ == "__main__":
    main()

