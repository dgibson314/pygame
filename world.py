import os
import sys
import math
import random
import pygame


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

SCREEN_SIZE = (1500, 1500)
CLOCK = 60

NUM_PARTICLES = 0
NUM_BUBBLES = 0
NUM_PLANETS = 4

STRENTH_OF_GRAVITY = 1.e2
DENSITY = 0.001

PLANETS = []


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
        pos = (int(self.state.x_pos), int(self.state.y_pos))
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


class Sun(Particle):
    def __init__(self, state, radius, color=YELLOW):
        Particle.__init__(self, state, radius, color)
        self.mass = self.mass_from_radius()

    def __repr__(self):
        return 'Sun: ' + repr(self.state)


class Planet(Particle):
    def __init__(self, state, radius, color=GREEN):
        Particle.__init__(self, state, radius, color)
        self.mass = self.mass_from_radius()

    def __repr__(self):
        return 'Planet: ' + repr(self.state)

    def mass_from_radius(self):
        return DENSITY * 4/3 * math.pi * (self.radius ** 3)

    def update_velocity(self):
        ax = 0.0
        ay = 0.0

        for planet in PLANETS:
            if planet is not self:
                delta_x = self.state.x_pos - planet.state.x_pos
                delta_y = self.state.y_pos - planet.state.y_pos
                distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

                force = STRENTH_OF_GRAVITY * self.mass * planet.mass / distance**2

                ax += force * delta_x / distance
                ay += force * delta_y / distance

        self.state.vx -= ax
        self.state.vy -= ay


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

    # Generate Planets
    for i in range(0, NUM_PLANETS):
        rand_state = State(
            float(random.randint(0, screen.get_width())),
            float(random.randint(0, screen.get_height())),
            0,
            0)
        rand_radius = random.randint(6, 10)
        rand_mass = random.randint(1, 5)
        PLANETS.append(Planet(rand_state, rand_radius, rand_mass))

    # Prepare display objects
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(CLOCK)

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update object positions
        for particle in particles:
            particle.update()
            for bubble in bubbles:
                if particle.touching(bubble):
                    bubbles.remove(bubble)
                else:
                    bubble.update()
        for planet in PLANETS:
            planet.update()

        # Draw everything
        screen.blit(background, (0, 0))
        for particle in particles:
            particle.draw()
        for bubble in bubbles:
            bubble.draw()
        for planet in PLANETS:
            planet.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
