import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Ball properties
ball_radius = 10
ball_color = red
ball_x, ball_y = width // 2, height // 2
ball_velocity_x, ball_velocity_y = 5, -3
gravity = 0.5
friction = 0.9

# Hexagon properties
hexagon_side_length = 150
hexagon_color = white
hexagon_center = (width // 2, height // 2)
hexagon_rotation_speed = 2  # degrees per frame

def draw_hexagon(surf, center, side_length, color):
    """Draws a hexagon on the given surface."""
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.radians(angle_deg)
        x = center[0] + side_length * math.cos(angle_rad)
        y = center[1] + side_length * math.sin(angle_rad)
        points.append((x, y))
    pygame.draw.polygon(surf, color, points)

def rotate_point(point, origin, angle):
    """Rotates a point around an origin by the given angle in degrees."""
    angle_rad = math.radians(angle)
    dx = point[0] - origin[0]
    dy = point[1] - origin[1]
    qx = origin[0] + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
    qy = origin[1] + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
    return (qx, qy)

def check_collision_and_bounce(point, velocity, angle):
    """Checks collision with the hexagon and updates the velocity."""
    angle_deg = 30
    for i in range(6):
        angle_rad = math.radians(angle_deg * i + angle)
        next_angle_rad = math.radians(angle_deg * (i + 1) + angle)

        x1, y1 = hexagon_center[0] + hexagon_side_length * math.cos(angle_rad), \
                  hexagon_center[1] + hexagon_side_length * math.sin(angle_rad)
        x2, y2 = hexagon_center[0] + hexagon_side_length * math.cos(next_angle_rad), \
                  hexagon_center[1] + hexagon_side_length * math.sin(next_angle_rad)

        # Check if the point is outside the hexagon
        d = (point[0] - x1) * (y2 - y1) - (x2 - x1) * (point[1] - y1)
        if d > 0.1:
            continue

        # Calculate the normal vector to the edge
        normal_x = -(y2 - y1)
        normal_y = (x2 - x1)

        # Reflect the velocity based on the angle of incidence
        dot_product = velocity[0] * normal_x + velocity[1] * normal_y
        reflected_velocity_x = velocity[0] - 2 * dot_product * normal_x / (normal_x**2 + normal_y**2)
        reflected_velocity_y = velocity[1] - 2 * dot_product * normal_y / (normal_x**2 + normal_y**2)

        # Apply friction to the velocity
        reflected_velocity_x *= friction
        reflected_velocity_y *= friction

        return (reflected_velocity_x, reflected_velocity_y)

    return velocity

# Main loop
running = True
clock = pygame.time.Clock()
hexagon_rotation_angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_x += ball_velocity_x * 1.5  # Increase speed for better visibility
    ball_y += ball_velocity_y * 1.5

    # Check collision with hexagon walls and update velocity
    new_velocity = check_collision_and_bounce((ball_x, ball_y), (ball_velocity_x, ball_velocity_y), hexagon_rotation_angle)
    if new_velocity != (ball_velocity_x, ball_velocity_y):
        ball_velocity_x, ball_velocity_y = new_velocity

    # Update gravity and friction
    ball_velocity_y += gravity * 1.5  # Increase speed for better visibility
    ball_velocity_x *= friction
    ball_velocity_y *= friction

    # Check boundaries to prevent the ball from going out of screen
    if ball_x - ball_radius < 0 or ball_x + ball_radius > width:
        ball_velocity_x *= -1
        ball_x = max(ball_radius, min(width - ball_radius, ball_x))

    if ball_y - ball_radius < 0 or ball_y + ball_radius > height:
        ball_velocity_y *= -1
        ball_y = max(ball_radius, min(height - ball_radius, ball_y))

    # Rotate the hexagon
    hexagon_rotation_angle = (hexagon_rotation_angle + hexagon_rotation_speed) % 360

    screen.fill(black)

    # Draw the hexagon with rotation
    rotated_hexagon_points = []
    for i in range(6):
        angle_deg = 60 * i - 30 + hexagon_rotation_angle
        angle_rad = math.radians(angle_deg)
        x = hexagon_center[0] + hexagon_side_length * math.cos(angle_rad)
        y = hexagon_center[1] + hexagon_side_length * math.sin(angle_rad)
        rotated_hexagon_points.append((x, y))
    pygame.draw.polygon(screen, hexagon_color, rotated_hexagon_points)

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
