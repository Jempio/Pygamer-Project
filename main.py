# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pygame

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1280
HEIGHT = 720
TITLE = "<Move and Groove>"


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


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # ----- Sprites
    all_sprites_group = pygame.sprite.RenderUpdates()

    # ----- Player
    player = Player()
    all_sprites_group.add(player)

    # ----- Level

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if keys[pygame.K_LSHIFT]:
                player.monkey_speed = 2
            else:
                player.monkey_speed = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.vel_x = 6
                elif event.key == pygame.K_LEFT:
                    player.vel_x = -6

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.vel_x < 0:
                    player.vel_x = 0
                if event.key == pygame.K_RIGHT and player.vel_x > 0:
                    player.vel_x = 0

        # ----- LOGIC

        # ----- DRAW
        screen.fill(BLACK)
        all_sprites_group.draw(screen)
        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)
        all_sprites_group.update()

    pygame.quit()


if __name__ == "__main__":
    main()
