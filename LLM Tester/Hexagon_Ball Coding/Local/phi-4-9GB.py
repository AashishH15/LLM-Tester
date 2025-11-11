import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 40)
BALL_RADIUS = 10
HEX_SIZE = 100
GRAVITY = 0.5
FRICTION = 0.99
SPIN_SPEED = 2

# Colors
WHITE = (255, 255, 255)

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vx = math.cos(math.radians(30)) * 5
        self.vy = -math.sin(math.radians(30)) * 5

    def move(self, walls):
        # Apply gravity
        self.vy += GRAVITY
        
        # Update position with velocity
        self.x += self.vx
        self.y += self.vy

        # Check for collisions and bounce off walls
        self.check_collisions(walls)

        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION

    def check_collisions(self, walls):
        for wall in walls:
            if wall.collide_point(self.x, self.y):
                normal = wall.normal()
                dot_product = (self.vx * normal[0] + self.vy * normal[1])

                # Reflect velocity
                self.vx -= 2 * dot_product * normal[0]
                self.vy -= 2 * dot_product * normal[1]

class Wall:
    def __init__(self, start, end):
        self.start = pygame.Vector2(start)
        self.end = pygame.Vector2(end)

    def collide_point(self, px, py):
        line_vec = self.end - self.start
        pnt_vec = pygame.Vector2(px, py) - self.start

        line_len = line_vec.length()
        line_unitvec = line_vec / line_len
        pnt_proj_length = pnt_vec.dot(line_unitvec)
        pnt_closest = line_unitvec * pnt_proj_length
        
        if 0 <= pnt_proj_length <= line_len:
            closest = self.start + pnt_closest
            dist_to_line = (pygame.Vector2(px, py) - closest).length()
            return dist_to_line < BALL_RADIUS
        return False

    def normal(self):
        line_vec = self.end - self.start
        norm = pygame.Vector2(-line_vec.y, line_vec.x)
        return norm.normalize()

def create_hexagon(center_x, center_y, size, angle=0):
    angles = [math.radians(60 * i + angle) for i in range(6)]
    points = [(center_x + math.cos(a) * size, center_y + math.sin(a) * size) for a in angles]
    return [Wall(points[i], points[(i+1)%6]) for i in range(6)]

def rotate_points(points, angle, origin=(0, 0)):
    ox, oy = origin
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)

    rotated_points = []
    for x, y in points:
        tx, ty = x - ox, y - oy
        rx = ox + (tx * cos_theta - ty * sin_theta)
        ry = oy + (tx * sin_theta + ty * cos_theta)
        rotated_points.append((rx, ry))
    
    return rotated_points

# Main loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball = Ball()
    hex_walls = create_hexagon(WIDTH // 2, HEIGHT // 2, HEX_SIZE)
    angle = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BG_COLOR)

        # Rotate hexagon
        angle += SPIN_SPEED * clock.get_time() / 1000.0
        rotated_points = rotate_points([(w.start.x, w.start.y) for w in hex_walls], angle)
        rotated_points.extend(rotate_points([(w.end.x, w.end.y) for w in hex_walls], angle))
        for i in range(6):
            start_point = pygame.Vector2(rotated_points[i])
            end_point = pygame.Vector2(rotated_points[i + 6])
            wall = Wall(start_point, end_point)
            pygame.draw.line(screen, WHITE, (start_point.x, start_point.y), (end_point.x, end_point.y), 3)

        ball.move(hex_walls)

        # Draw the ball
        pygame.draw.circle(screen, WHITE, (int(ball.x), int(ball.y)), BALL_RADIUS)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
