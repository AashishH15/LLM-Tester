import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 40)
BALL_RADIUS = 15
GRAVITY = 0.5
FRICTION = -0.02
SPIN_SPEED = 50 * math.pi / 180  # radians per frame

# Colors
BALL_COLOR = (255, 100, 50)
HEXAGON_COLOR = (100, 150, 200)

class Wall:
    def __init__(self, start, end):
        self.start = start  # tuple (x, y)
        self.end = end      # tuple (x, y)

    def normal(self):
        start_vec = pygame.Vector2(self.start)
        end_vec = pygame.Vector2(self.end)
        dx = end_vec.x - start_vec.x
        dy = end_vec.y - start_vec.y
        length = math.hypot(dx, dy)
        if length == 0:
            return pygame.Vector2(0, 1)  # Default normal for degenerate segments
        nx = -dy / length
        ny = dx / length
        return pygame.Vector2(nx, ny)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 5
        self.vy = 2

    def update(self, hexagon_points):
        # Apply gravity
        self.vy += GRAVITY

        # Predict new position
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        # Build wall segments from hexagon points
        walls = []
        for i in range(len(hexagon_points)):
            start = hexagon_points[i]
            end = hexagon_points[(i + 1) % len(hexagon_points)]
            walls.append(Wall(start, end))

        # Check collisions based on predicted position
        self.check_collisions(walls, new_x, new_y)

        # Update position
        self.x += self.vx
        self.y += self.vy

    def check_collisions(self, walls, new_x, new_y):
        ball_center = pygame.Vector2(new_x, new_y)
        for wall in walls:
            start = pygame.Vector2(wall.start)
            end = pygame.Vector2(wall.end)
            line_vec = end - start
            pnt_vec = ball_center - start

            line_len_sq = line_vec.length_squared()
            if line_len_sq == 0:
                continue

            t = max(0, min(1, pnt_vec.dot(line_vec) / line_len_sq))
            closest = start + line_vec * t

            distance_vec = ball_center - closest
            dist_to_line = distance_vec.length()

            if dist_to_line < BALL_RADIUS:
                self.resolve_collision(wall, distance_vec, dist_to_line)

    def resolve_collision(self, wall, distance_vec, dist_to_line):
        # Reflect velocity vector off the wall's normal
        normal = wall.normal()
        dot_product = self.vx * normal.x + self.vy * normal.y

        self.vx -= 2 * dot_product * normal.x
        self.vy -= 2 * dot_product * normal.y

        # Correct position so the ball no longer penetrates the wall
        if distance_vec.length() != 0:
            correction_vec = distance_vec.normalize() * (BALL_RADIUS - dist_to_line)
            self.x += correction_vec.x
            self.y += correction_vec.y

    def draw(self, screen):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)

class Hexagon:
    def __init__(self, center_x, center_y, size):
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.angle = 0

    def update(self):
        # Spin the hexagon
        self.angle += SPIN_SPEED

    def get_points(self):
        points = []
        for i in range(6):
            angle_deg = 60 * i + self.angle
            angle_rad = math.radians(angle_deg)
            x = self.center_x + self.size * math.cos(angle_rad)
            y = self.center_y + self.size * math.sin(angle_rad)
            points.append((x, y))
        return points

    def draw(self, screen):
        pygame.draw.polygon(screen, HEXAGON_COLOR, self.get_points(), 2)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    hexagon = Hexagon(WIDTH // 2, HEIGHT // 2, 150)
    ball = Ball(WIDTH // 2, HEIGHT // 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game objects
        hexagon.update()
        ball.update(hexagon.get_points())

        # Render everything
        screen.fill(BACKGROUND_COLOR)
        hexagon.draw(screen)
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
