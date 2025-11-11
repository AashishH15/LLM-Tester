import pygame
import math

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
BALL_RADIUS = 10
GRAVITY = 0.5
FRICTION = 0.9

class Ball:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vx = 5
        self.vy = -5

    def update(self):
        self.vy += GRAVITY
        self.vy *= FRICTION
        self.y += self.vy
        self.x += self.vx

class Hexagon:
    def __init__(self):
        self.radius = 200
        self.center_x = WIDTH / 2
        self.center_y = HEIGHT / 2
        self.rotation = 0

    def update(self):
        self.rotation += 0.01

    def get_points(self):
        points = []
        for i in range(6):
            angle = math.pi * (i / 3 + self.rotation)
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            points.append((x, y))
        return points

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball = Ball()
    hexagon = Hexagon()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        ball.update()
        hexagon.update()

        # Check collision with hexagon walls
        points = hexagon.get_points()
        for i in range(6):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % 6]
            if (x1 - ball.x) ** 2 + (y1 - ball.y) ** 2 < BALL_RADIUS ** 2:
                # Bounce off wall
                ball.vx *= -1
                ball.vy *= -1

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.polygon(screen, RED, points, 1)
        pygame.draw.circle(screen, (0, 0, 255), (int(ball.x), int(ball.y)), BALL_RADIUS)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
