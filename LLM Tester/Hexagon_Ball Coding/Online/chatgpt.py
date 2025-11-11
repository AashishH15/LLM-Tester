import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
BG_COLOR = (20, 20, 20)
BALL_COLOR = (255, 100, 100)
HEX_COLOR = (100, 200, 255)
GRAVITY = np.array([0, 0.3])
FRICTION = 0.99
BOUNCE = 0.8
HEX_RADIUS = 200
HEX_CENTER = np.array([WIDTH // 2, HEIGHT // 2])
BALL_RADIUS = 10

# Ball properties
ball_pos = np.array([WIDTH // 2, HEIGHT // 2 - 100], dtype=np.float64)
ball_vel = np.array([2, 0], dtype=np.float64)

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
angle = 0
angular_speed = 0.05  # Radians per frame

# Function to get hexagon points
def get_hexagon_points(center, radius, angle):
    points = []
    for i in range(6):
        theta = angle + i * np.pi / 3
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        points.append((x, y))
    return points

# Function to check collision with hexagon walls
def check_collision(ball_pos, ball_vel, hex_points):
    for i in range(6):
        p1 = np.array(hex_points[i])
        p2 = np.array(hex_points[(i + 1) % 6])
        
        edge = p2 - p1
        edge_normal = np.array([-edge[1], edge[0]])
        edge_normal /= np.linalg.norm(edge_normal)
        
        ball_to_edge = ball_pos - p1
        dist = np.dot(ball_to_edge, edge_normal)
        
        if abs(dist) <= BALL_RADIUS:  # Possible collision
            projection = ball_to_edge - dist * edge_normal
            projected_point = p1 + projection
            if np.dot(projected_point - p1, edge) >= 0 and np.dot(projected_point - p2, -edge) >= 0:
                ball_pos -= (1 + BOUNCE) * dist * edge_normal
                ball_vel -= (1 + BOUNCE) * np.dot(ball_vel, edge_normal) * edge_normal
                ball_vel *= FRICTION
    return ball_pos, ball_vel

# Main loop
running = True
while running:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update ball physics
    ball_vel += GRAVITY
    ball_pos += ball_vel
    
    # Update hexagon rotation
    angle += angular_speed
    hex_points = get_hexagon_points(HEX_CENTER, HEX_RADIUS, angle)
    
    # Collision detection
    ball_pos, ball_vel = check_collision(ball_pos, ball_vel, hex_points)
    
    # Draw hexagon
    pygame.draw.polygon(screen, HEX_COLOR, hex_points, 2)
    
    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, ball_pos.astype(int), BALL_RADIUS)
    
    # Refresh screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
