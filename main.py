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
        self.image = pygame.image.load("./assets/player.png")
        self.image = pygame.transform.scale(self.image, (175, 200))
        self.rect = self.image.get_rect()

        # Vector
        self.vel_x = 0

    def update(self):
        self.rect.x = self.vel_x

    # Player-controlled movement:
    def move_left(self):
        """ Called when the user hits the left arrow. """
        self.vel_x = -6

    def move_right(self):
        """ Called when the user hits the right arrow. """
        self.vel_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.vel_x = 0


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
    player.rect.x = WIDTH/2 - 97.5
    player.rect.y = HEIGHT - player.rect.height

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.stop()
                if event.key == pygame.K_RIGHT:
                    player.stop()

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
