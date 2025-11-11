import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Hexagon parameters
hexagon_center = (width // 2, height // 2)
hexagon_radius = 150
rotation_angle = 0
rotation_speed = 0.02  # Radians per frame

# Ball parameters
ball_radius = 10
ball_x = hexagon_center[0]
ball_y = hexagon_center[1] - hexagon_radius + ball_radius # Start at top
ball_dx = 5  # Initial x velocity
ball_dy = 0  # Initial y velocity
gravity = 0.5
friction = 0.98

# Clock for controlling frame rate
clock = pygame.time.Clock()
fps = 60

def draw_hexagon(center, radius, angle):
    points = []
    for i in range(6):
        x = center[0] + radius * math.cos(math.pi * 2 * i / 6 + angle)
        y = center[1] + radius * math.sin(math.pi * 2 * i / 6 + angle)
        points.append((x, y))
    pygame.draw.polygon(screen, white, points, 2)  # Draw the hexagon outline

def ball_collision(ball_x, ball_y, ball_dx, ball_dy, center, radius, angle):
    for i in range(6):
        x1 = center[0] + radius * math.cos(math.pi * 2 * i / 6 + angle)
        y1 = center[1] + radius * math.sin(math.pi * 2 * i / 6 + angle)
        x2 = center[0] + radius * math.cos(math.pi * 2 * (i + 1) / 6 + angle)
        y2 = center[1] + radius * math.sin(math.pi * 2 * (i + 1) / 6 + angle)

        # Distance from ball center to the line segment
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:  # Avoid division by zero
            continue

        t = ((ball_x - x1) * dx + (ball_y - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))  # Clamp t to 0-1 range

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        distance = math.sqrt((ball_x - closest_x)**2 + (ball_y - closest_y)**2)

        if distance < ball_radius:
            # Collision detected!  Reflect the ball's velocity.
            nx = -(closest_y - ball_y) # Normal vector (pointing outwards)
            ny = closest_x - ball_x
            
            magnitude = math.sqrt(nx*nx + ny*ny)
            nx /= magnitude
            ny /= magnitude

            dot_product = ball_dx * nx + ball_dy * ny
            ball_dx -= 2 * dot_product * nx
            ball_dy -= 2 * dot_product * ny

            # Small adjustment to prevent sticking
            ball_x += nx * (ball_radius - distance + 1)
            ball_y += ny * (ball_radius - distance + 1)

            return ball_x, ball_y, ball_dx, ball_dy

    return ball_x, ball_y, ball_dx, ball_dy



# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update rotation
    rotation_angle += rotation_speed

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Apply gravity
    ball_dy += gravity

    # Apply friction
    ball_dx *= friction
    ball_dy *= friction
    
    # Check for collision with hexagon walls
    ball_x, ball_y, ball_dx, ball_dy = ball_collision(ball_x, ball_y, ball_dx, ball_dy, hexagon_center, hexagon_radius, rotation_angle)


    # Clear the screen
    screen.fill(black)

    # Draw the hexagon
    draw_hexagon(hexagon_center, hexagon_radius, rotation_angle)

    # Draw the ball
    pygame.draw.circle(screen, red, (int(ball_x), int(ball_y)), ball_radius)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(fps)

pygame.quit()