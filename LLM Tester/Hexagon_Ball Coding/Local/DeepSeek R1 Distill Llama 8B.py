import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
fps = 60

# Ball properties
ball_radius = 15
ball_x = -50  # Initial position: left side of hexagon
ball_y = display_height / 2
vx = 0  # Initial horizontal velocity
vy = 0.5  # Initial vertical velocity
friction = 0.98  # Friction coefficient

# Hexagon properties
hex_side = 100
rotation_speed = 3
walls = [
    (0, 0), (hex_side, 0),
    (hex_side, -80), (0, -80),
    (0, -80), (-hex_side, -80),
    (-hex_side, 0), (0, 0)
]

# Colors
background_color = (255, 200, 150)
ball_color = (255, 0, 0)

def draw_hexagon():
    screen.fill(background_color)
    for i in range(len(walls)):
        x1, y1 = walls[i]
        x2, y2 = walls[(i+1) % len(walls)]
        pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 3)

def update_ball():
    global ball_x, ball_y, vx, vy

    # Apply gravity
    vy += 0.5  # Acceleration due to gravity

    # Apply friction
    if abs(vx) > 0.01:
        vx *= friction

    # Update position
    ball_x += vx
    ball_y += vy

    # Check for wall collisions
    collision = False
    for i in range(len(walls)):
        x1, y1 = walls[i]
        x2, y2 = walls[(i+1) % len(walls)]
        # Check if the ball hits a wall
        if (ball_x + ball_radius >= min(x1, x2)) and \
           (ball_x - ball_radius <= max(x1, x2)) and \
           (ball_y - ball_radius <= max(y1, y2)):
            # Calculate normal vector for collision
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            dist = math.hypot(ball_x + ball_radius - min(x1, x2), 
                              ball_y - ball_radius - min(y1, y2))
            if dist < ball_radius * 2:
                normal_vector = (min(x1, x2) - max(x1, x2), 
                                 max(y1, y2) - min(y1, y2))
                # Reverse velocity component along the wall
                dot_product = (ball_x + ball_radius - (min(x1, x2) if dx > 0 else max(x1, x2))) * normal_vector[0] + \
                             (ball_y - ball_radius - (min(y1, y2) if dy > 0 else max(y1, y2))) * normal_vector[1]
                vy = -vy - (dot_product / (dist)) * 2
                collision = True
                break
        elif (ball_x + ball_radius <= max(x1, x2)) and \
             (ball_x - ball_radius >= min(x1, x2)):
            # Check for top/bottom walls
            if y1 > y2:
                bottom = y2
                top = y1
            else:
                top = y1
                bottom = y2
            if ball_y - ball_radius <= bottom and ball_y + ball_radius >= top:
                normal_vector = (0, 1)
                dot_product = (ball_y - ball_radius - bottom) * normal_vector[0] + (ball_x) * normal_vector[1]
                vy = -vy - (dot_product / (dist)) * 2
                collision = True
                break

    if not collision:
        # Check for side walls
        min_x = min(walls[i][0] for i in range(len(walls)))
        max_x = max(walls[i][0] for i in range(len(walls)))
        min_y = min(walls[i][1] for i in range(len(walls)))
        max_y = max(walls[i][1] for i in range(len(walls)))

    # Keep ball within screen boundaries
    if ball_x - ball_radius <= 0:
        ball_x = ball_radius
        vx = abs(vx)
    elif ball_x + ball_radius >= display_width:
        ball_x = display_width - ball_radius
        vx = -abs(vx)

def draw_ball():
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

# Main game loop
running = True
while running:
    screen.fill(background_color)
    
    # Update ball position and velocity
    update_ball()
    
    # Draw the hexagon and ball
    draw_hexagon()
    draw_ball()
    
    pygame.display.flip()
    clock.tick(fps)
    
    # Check for events to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
