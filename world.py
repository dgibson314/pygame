import os, sys
import pygame


BLACK = (0, 0, 255)
BACKGROUND = (255, 255, 255)
SCREEN_SIZE = (800, 800)


class Particle():
    def __init__(self, x_pos, y_pos, vx, vy, radius):
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.vx = vx
        self.vy = vy

        self.radius = radius
        self.color = BLACK

        self.screen = pygame.display.get_surface()

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x_pos, self.y_pos), self.radius)

    def update(self):
        self.update_velocity()
        self.x_pos += self.vx
        self.y_pos += self.vy

    def update_velocity(self):
        self.vy += 1


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # Create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BACKGROUND)

    # Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Add particles
    p = Particle(50, 50, 3, -10, 5)

    # Prepare display objects
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(10)

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update particle positions
        p.update()

        # Draw everything
        screen.blit(background, (0, 0))
        p.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
