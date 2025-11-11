import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Physics parameters
gravity = 0.5
friction = 0.995
restitution = 0.8
rotation_speed = 0.05  # Radians per frame
ball_radius = 10

# Hexagon parameters
center = (width//2, height//2)
hex_radius = 200

# Initialize ball
ball_pos = [center[0], center[1] - 100]
ball_vel = [0, 0]

def get_hexagon_points(angle):
    """Generate hexagon vertices based on current rotation angle"""
    return [(center[0] + hex_radius * math.cos(angle + math.radians(60*i)),
             center[1] + hex_radius * math.sin(angle + math.radians(60*i)))
            for i in range(6)]

def calculate_normal(p1, p2):
    """Calculate inward-pointing normal vector for a wall segment"""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    normal = (-dy, dx)
    
    # Ensure normal points inward
    mid = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)
    to_center = (center[0] - mid[0], center[1] - mid[1])
    dot = normal[0] * to_center[0] + normal[1] * to_center[1]
    
    if dot < 0:
        normal = (dy, -dx)
    
    # Normalize
    length = math.hypot(*normal)
    return (normal[0]/length, normal[1]/length) if length != 0 else (0, 0)

# Main loop
angle = 0
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update rotation angle
    angle += rotation_speed
    
    # Apply physics
    ball_vel[1] += gravity
    ball_vel[0] *= friction
    ball_vel[1] *= friction
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Collision detection
    hex_points = get_hexagon_points(angle)
    for i in range(6):
        p1 = hex_points[i]
        p2 = hex_points[(i+1)%6]
        
        # Find closest point on segment to ball center
        segment_vec = (p2[0]-p1[0], p2[1]-p1[1])
        ball_vec = (ball_pos[0]-p1[0], ball_pos[1]-p1[1])
        t = max(0, min(1, (ball_vec[0]*segment_vec[0] + ball_vec[1]*segment_vec[1]) / 
                     (segment_vec[0]**2 + segment_vec[1]**2 + 1e-8)))
        closest = (p1[0] + t*segment_vec[0], p1[1] + t*segment_vec[1])
        
        # Check collision
        dx = ball_pos[0] - closest[0]
        dy = ball_pos[1] - closest[1]
        if dx*dx + dy*dy < ball_radius**2:
            normal = calculate_normal(p1, p2)
            
            # Calculate wall velocity at collision point
            rel_x = closest[0] - center[0]
            rel_y = closest[1] - center[1]
            wall_vx = -rotation_speed * rel_y
            wall_vy = rotation_speed * rel_x
            
            # Calculate relative velocity
            rel_vel_x = ball_vel[0] - wall_vx
            rel_vel_y = ball_vel[1] - wall_vy
            
            # Reflect relative velocity
            dot = rel_vel_x * normal[0] + rel_vel_y * normal[1]
            if dot < 0:
                rel_vel_x -= 2 * dot * normal[0]
                rel_vel_y -= 2 * dot * normal[1]
                
                # Apply restitution
                rel_vel_x *= restitution
                rel_vel_y *= restitution
                
                # Update ball velocity
                ball_vel[0] = rel_vel_x + wall_vx
                ball_vel[1] = rel_vel_y + wall_vy
                
                # Move ball outside collision
                penetration = ball_radius - math.hypot(dx, dy)
                ball_pos[0] += normal[0] * penetration
                ball_pos[1] += normal[1] * penetration

    # Drawing
    screen.fill(BLACK)
    pygame.draw.polygon(screen, WHITE, hex_points, 2)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()