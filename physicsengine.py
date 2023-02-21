import pygame
import random
import math
import sys

# Constants
WIDTH = 600
HEIGHT = 400
FLOOR_Y = 350
LEFT_WALL_X = 50
RIGHT_WALL_X = 550
GRAVITY = pygame.math.Vector2(0, 0.1)

# Classes
class PhysicsObject:
    def __init__(self, x, y, width, height, color, mass):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.mass = mass
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self, gravity, left_wall_x, right_wall_x, floor_y):
        # Apply gravity
        self.velocity += gravity

        # Update position based on velocity
        self.rect.move_ip(self.velocity)

        # Check for collision with floor
        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.velocity.y = -abs(self.velocity.y) * 0.6  # reduce restitution factor

        if self.rect.left <= left_wall_x:
            self.rect.left = left_wall_x
            self.velocity.x = abs(self.velocity.x) * 0.6  # reduce restitution factor
        elif self.rect.right >= right_wall_x:
            self.rect.right = right_wall_x
            self.velocity.x = -abs(self.velocity.x) * 0.6  # reduce restitution factor

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def collides_with(self, other):
        return self.rect.colliderect(other.rect)

    def resolve_collision(self, other):
        # Calculate relative velocity
        rel_velocity = other.velocity - self.velocity

        # Calculate impulse magnitude
        impulse_mag = (-(1 + 0.6) * rel_velocity.dot(other.rect.center - self.rect.center)) / \
                      ((1 / self.mass) + (1 / other.mass))

        # Calculate impulse vector
        impulse = impulse_mag * pygame.math.Vector2.normalize(other.rect.center - self.rect.center)

        # Update velocities
        self.velocity -= impulse / self.mass
        other.velocity += impulse / other.mass


# Initialize Pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create objects
obj1 = PhysicsObject(50, 50, 50, 50, (255, 0, 0), 1)
obj2 = PhysicsObject(200, 50, 50, 50, (0, 255, 0), 1)

# Set up clock
clock = pygame.time.Clock()

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update objects
    obj1.update(GRAVITY, LEFT_WALL_X, RIGHT_WALL_X, FLOOR_Y)
    obj2.update(GRAVITY, LEFT_WALL_X, RIGHT_WALL_X, FLOOR_Y)

    # Check for collision between objects
    if obj1.collides_with(obj2):
        obj1.resolve_collision(obj2)

    # Draw objects and environment
    screen.fill((0, 0, 0))
    obj1.draw(screen)
    obj2.draw(screen)
    pygame.draw.rect(screen, (255, 255, 255), (LEFT_WALL_X, 0, 5, FLOOR_Y))
    pygame.draw.rect(screen, (255, 255, 255), (RIGHT_WALL_X, 0, 5, FLOOR_Y))
    pygame.draw.rect(screen, (255, 255, 255), (0, FLOOR_Y, WIDTH, 5))

    # Show velocity of objects
    font = pygame.font.Font(None, 24)
    velocity_text_obj1 = font.render(f"Velocity: ({obj1.velocity.x:.1f}, {obj1.velocity.y:.1f})", True, (255, 255, 255))
    velocity_text_obj2 = font.render(f"Velocity: ({obj2.velocity.x:.1f}, {obj2.velocity.y:.1f})", True, (255, 255, 255))
    screen.blit(velocity_text_obj1, (obj1.rect.x, obj1.rect.y - 30))
    screen.blit(velocity_text_obj2, (obj2.rect.x, obj2.rect.y - 30))

    # Check for collision between objects
    if obj1.collides_with(obj2):
        obj1.resolve_collision(obj2)

    # Update screen
    pygame.display.flip()

    # Wait for next frame
    clock.tick(60)
