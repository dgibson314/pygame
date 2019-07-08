import os
import sys
import math
import random
import pygame


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

SCREEN_SIZE = (1000, 1000)
NUM_PARTICLES = 10
NUM_BUBBLES = 20


class State():
    def __init__(self, x_pos, y_pos, vx, vy):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vx = vx
        self.vy = vy

    def __repr__(self):
        return 'x:{x} y:{y} vx:{vx} vy:{vy}'.format(
                x=self.x_pos, y=self.y_pos, vx=self.vx, vy=self.vy)


class Particle():
    def __init__(self, state, radius, color=BLACK):
        self.state = state

        self.radius = radius
        self.color = color

        self.screen = pygame.display.get_surface()

    def draw(self):
        pos = (self.state.x_pos, self.state.y_pos)
        pygame.draw.circle(self.screen, self.color, pos, self.radius)

    def update(self):
        self.update_velocity()

        self.state.x_pos += self.state.vx
        self.state.y_pos += self.state.vy

    def update_velocity(self):
        if self.crosses_x_border():
            self.state.vx = -self.state.vx
        if self.crosses_y_border():
            self.state.vy = -self.state.vy

    def crosses_x_border(self):
        width = self.screen.get_width()
        dx = self.state.x_pos + self.state.vx
        return dx > width or dx < 0

    def crosses_y_border(self):
        height = self.screen.get_height()
        dy = self.state.y_pos + self.state.vy
        return dy > height or dy < 0

    def touching(self, particle):
        delta_x = self.state.x_pos - particle.state.x_pos
        delta_y = self.state.y_pos - particle.state.y_pos
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        return distance <= (self.radius + particle.radius)


class Bubble(Particle):
    def __init__(self, state, radius, thickness, color=BLUE):
        Particle.__init__(self, state, radius, color)
        self.thickness = thickness

    def draw(self):
        pos = (self.state.x_pos, self.state.y_pos)
        pygame.draw.circle(self.screen, self.color, pos, self.radius, self.thickness)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # Create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)

    # Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Add particles and shells
    particles = []
    bubbles = []

    for i in range(0, NUM_PARTICLES):
        rand_state = State(
            random.randint(0, screen.get_width()),
            random.randint(0, screen.get_height()),
            random.randint(-7, 7),
            random.randint(-7, 7))
        rand_radius = random.randint(2, 7)
        particles.append(Particle(rand_state, rand_radius))

    for i in range(0, NUM_BUBBLES):
        rand_state = State(
            random.randint(0, screen.get_width()),
            random.randint(0, screen.get_height()),
            random.randint(-1, 1),
            random.randint(-1, 1))
        rand_radius = random.randint(15, 20)
        bubbles.append(Bubble(rand_state, rand_radius, 2))

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
            for bubble in bubbles:
                if particle.touching(bubble):
                    bubbles.remove(bubble)
                else:
                    bubble.update()

        # Draw everything
        screen.blit(background, (0, 0))
        for particle in particles:
            particle.draw()
        for bubble in bubbles:
            bubble.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
