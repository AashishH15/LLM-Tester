import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Physics constants
GRAVITY = 0.5
FRICTION = 0.97
RESTITUTION = 0.8
ROTATION_SPEED = 2.0  # degrees per frame

class Ball:
    def __init__(self, x, y, radius):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0.0, 0.0])
        self.radius = radius

    def update(self):
        # Apply gravity
        self.vel[1] += GRAVITY
        
        # Update position
        self.pos += self.vel
        
        # Apply friction
        self.vel *= FRICTION

class Hexagon:
    def __init__(self, center_x, center_y, radius):
        self.center = np.array([center_x, center_y])
        self.radius = radius
        self.angle = 0
        
    def get_vertices(self):
        vertices = []
        for i in range(6):
            angle = math.radians(self.angle + i * 60)
            x = self.center[0] + self.radius * math.cos(angle)
            y = self.center[1] + self.radius * math.sin(angle)
            vertices.append(np.array([x, y]))
        return vertices
    
    def get_edges(self):
        vertices = self.get_vertices()
        edges = []
        for i in range(6):
            edges.append((vertices[i], vertices[(i + 1) % 6]))
        return edges
    
    def rotate(self):
        self.angle += ROTATION_SPEED

def line_intersection(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return None
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    
    if 0 <= t <= 1:
        intersection_x = x1 + t * (x2 - x1)
        intersection_y = y1 + t * (y2 - y1)
        return np.array([intersection_x, intersection_y])
    return None

def check_collision(ball, hexagon):
    next_pos = ball.pos + ball.vel
    
    for edge_start, edge_end in hexagon.get_edges():
        intersection = line_intersection(
            ball.pos, next_pos,
            edge_start, edge_end
        )
        
        if intersection is not None:
            # Calculate edge normal
            edge_vector = edge_end - edge_start
            edge_normal = np.array([-edge_vector[1], edge_vector[0]])
            edge_normal = edge_normal / np.linalg.norm(edge_normal)
            
            # Reflect velocity
            dot_product = np.dot(ball.vel, edge_normal)
            ball.vel = ball.vel - (2 * dot_product * edge_normal)
            ball.vel *= RESTITUTION
            
            # Move ball to intersection point
            ball.pos = intersection
            return True
    return False

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")
clock = pygame.time.Clock()

# Create objects
hexagon = Hexagon(WIDTH//2, HEIGHT//2, 200)
ball = Ball(WIDTH//2, HEIGHT//2 - 100, 10)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    hexagon.rotate()
    check_collision(ball, hexagon)
    ball.update()
    
    # Draw
    screen.fill(BLACK)
    
    # Draw hexagon
    vertices = hexagon.get_vertices()
    pygame.draw.polygon(screen, WHITE, vertices, 2)
    
    # Draw ball
    pygame.draw.circle(screen, RED, ball.pos.astype(int), ball.radius)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()