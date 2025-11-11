import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ball properties
ball_radius = 15
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [2, -3]  # Initial velocity

# Gravity and friction
gravity = 0.3
friction = 0.98

# Hexagon properties
hexagon_center = (WIDTH // 2, HEIGHT // 2)
hexagon_radius = 200
num_sides = 6
angle_increment = 2 * math.pi / num_sides
hexagon_rotation_angle = 0  # Initial angle of rotation

# Clock to control the frame rate
clock = pygame.time.Clock()

def draw_hexagon(center, radius, angle, sides):
    points = []
    for i in range(sides):
        x = center[0] + radius * math.cos(angle + i * angle_increment)
        y = center[1] - radius * math.sin(angle + i * angle_increment)
        points.append((x, y))
    
    pygame.draw.polygon(screen, BLACK, points, 2)

def point_in_hexagon(point, hexagon_center, radius, angle):
    # Rotate the point to align with the non-rotated hexagon
    x = point[0] - hexagon_center[0]
    y = point[1] - hexagon_center[1]
    
    x_rot = x * math.cos(angle) + y * math.sin(angle)
    y_rot = -x * math.sin(angle) + y * math.cos(angle)
    
    # Check if the rotated point is inside a non-rotated hexagon
    for i in range(num_sides):
        angle1 = i * angle_increment
        angle2 = (i + 1) * angle_increment
        
        p1x = radius * math.cos(angle1)
        p1y = -radius * math.sin(angle1)
        
        p2x = radius * math.cos(angle2)
        p2y = -radius * math.sin(angle2)
        
        # Line equations for the side of the hexagon
        line_eq1 = (p2y - p1y) * x_rot + (-p2x + p1x) * y_rot + p2x * p1y - p2y * p1x
        
        if line_eq1 <= 0:
            return False
    
    return True

def get_collision_normal(point, hexagon_center, radius, angle):
    # Rotate the point to align with the non-rotated hexagon
    x = point[0] - hexagon_center[0]
    y = point[1] - hexagon_center[1]
    
    x_rot = x * math.cos(angle) + y * math.sin(angle)
    y_rot = -x * math.sin(angle) + y * math.cos(angle)
    
    # Find the closest side of the hexagon
    min_distance = float('inf')
    collision_normal = None
    
    for i in range(num_sides):
        angle1 = i * angle_increment
        angle2 = (i + 1) * angle_increment
        
        p1x = radius * math.cos(angle1)
        p1y = -radius * math.sin(angle1)
        
        p2x = radius * math.cos(angle2)
        p2y = -radius * math.sin(angle2)
        
        # Project the point onto the line
        dx = p2x - p1x
        dy = p2y - p1y
        
        t = ((x_rot - p1x) * dx + (y_rot - p1y) * dy) / (dx ** 2 + dy ** 2)
        
        # Clamp the projection to the line segment
        tx = max(0, min(t, 1))
        ty = max(0, min(t, 1))
        
        px = p1x + tx * dx
        py = p1y + ty * dy
        
        distance_squared = (x_rot - px) ** 2 + (y_rot - py) ** 2
        
        if distance_squared < min_distance:
            min_distance = distance_squared
            collision_normal = (-dx, -dy)
    
    # Rotate the normal back to the original coordinate system
    nx, ny = collision_normal
    return (
        nx * math.cos(-angle) - ny * math.sin(-angle),
        nx * math.sin(-angle) + ny * math.cos(-angle)
    )

def main():
    global hexagon_rotation_angle
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Apply gravity and friction
        ball_vel[1] += gravity
        ball_vel[0] *= friction
        ball_vel[1] *= friction
        
        # Update ball position
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
        
        # Check for collision with the hexagon walls
        if not point_in_hexagon(ball_pos, hexagon_center, hexagon_radius, hexagon_rotation_angle):
            # Find collision normal
            collision_normal = get_collision_normal(
                ball_pos,
                hexagon_center,
                hexagon_radius,
                hexagon_rotation_angle
            )
            
            # Reflect the velocity vector
            nx, ny = collision_normal
            dot_product = ball_vel[0] * nx + ball_vel[1] * ny
            
            if dot_product < 0:
                ball_vel[0] -= 2 * dot_product * nx
                ball_vel[1] -= 2 * dot_product * ny
        
        # Clear the screen
        screen.fill(WHITE)
        
        # Draw the hexagon and the ball
        draw_hexagon(hexagon_center, hexagon_radius, hexagon_rotation_angle, num_sides)
        pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
        
        # Update the display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(60)
        
        # Rotate the hexagon
        hexagon_rotation_angle += 0.02
    
    pygame.quit()

if __name__ == "__main__":
    main()
