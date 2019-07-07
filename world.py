import os
import sys
import random
import pygame


BLACK = (0, 0, 255)
BACKGROUND = (255, 255, 255)
SCREEN_SIZE = (800, 800)
NUM_PARTICLES = 10


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
        pos = (self.x_pos, self.y_pos)
        pygame.draw.circle(self.screen, self.color, pos, self.radius)

    def update(self):
        self.update_velocity()

        self.x_pos += self.vx
        self.y_pos += self.vy

    def update_velocity(self):
        if self.crosses_x_border():
            self.vx = -self.vx
        if self.crosses_y_border():
            self.vy = -self.vy

    def crosses_x_border(self):
        width = self.screen.get_width()
        dx = self.x_pos + self.vx
        return dx > width or dx < 0

    def crosses_y_border(self):
        height = self.screen.get_height()
        dy = self.y_pos + self.vy
        return dy > height or dy < 0


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
    x = Particle(35, 150, -4, -2, 4)

    particles = []

    for i in range(0, NUM_PARTICLES):
        p = Particle(
            random.randint(0, screen.get_width()),
            random.randint(0, screen.get_height()),
            random.randint(-5, 5),
            random.randint(-5, 5),
            random.randint(2, 7))
        particles.append(p)

    # Prepare display objects
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update particle positions
        for particle in particles:
            particle.update()

        # Draw everything
        screen.blit(background, (0, 0))
        for particle in particles:
            particle.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
