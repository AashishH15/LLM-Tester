import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Hexagon properties
hexagon_center = (width // 2, height // 2)
hexagon_radius = 200
hexagon_line_color = white
hexagon_rotation_speed = 0.05  # Radians per frame
hexagon_angle = 0

# Ball properties
ball_radius = 20
ball_color = red
ball_position = [hexagon_center[0] - hexagon_radius / 2, hexagon_center[1]]  # Start near hexagon edge
ball_velocity = [5, 0]  # Initial velocity
gravity = 0.5
friction = 0.01
bounce_elasticity = 0.7

clock = pygame.time.Clock()

def calculate_hexagon_vertices(center_x, center_y, radius, angle):
    """Calculates the vertices of a hexagon rotated by 'angle'."""
    vertices = []
    for i in range(6):
        hexagon_angle_radians = math.radians(60 * i) + angle
        x = center_x + radius * math.cos(hexagon_angle_radians)
        y = center_y + radius * math.sin(hexagon_angle_radians)
        vertices.append((x, y))
    return vertices

def draw_hexagon(screen, vertices, color):
    """Draws the hexagon on the screen."""
    pygame.draw.polygon(screen, color, vertices, 2) # 2 pixel width for lines

def draw_ball(screen, position, radius, color):
    """Draws the ball on the screen."""
    pygame.draw.circle(screen, color, (int(position[0]), int(position[1])), radius)

def check_collision(ball_pos, ball_radius, hexagon_vertices):
    """Checks for collision between the ball and the hexagon walls."""
    for i in range(6):
        p1 = hexagon_vertices[i]
        p2 = hexagon_vertices[(i + 1) % 6]

        # Vector representing the edge of the hexagon
        edge = [p2[0] - p1[0], p2[1] - p1[1]]
        # Vector from point p1 to ball's center
        ball_to_p1 = [ball_pos[0] - p1[0], ball_pos[1] - p1[1]]

        # Distance from ball center to the line segment (edge)
        edge_len_sq = edge[0]**2 + edge[1]**2
        if edge_len_sq == 0: # Handle degenerate edge case (shouldn't happen in a hexagon)
            continue

        projection_factor = (ball_to_p1[0] * edge[0] + ball_to_p1[1] * edge[1]) / edge_len_sq
        projection_factor = max(0, min(1, projection_factor)) # Clamp to the segment

        closest_point_on_edge = [p1[0] + projection_factor * edge[0], p1[1] + projection_factor * edge[1]]
        distance_sq_to_edge = (ball_pos[0] - closest_point_on_edge[0])**2 + (ball_pos[1] - closest_point_on_edge[1])**2

        if distance_sq_to_edge <= ball_radius**2:
            # Collision detected!
            # Calculate collision normal (vector perpendicular to the edge, pointing outwards)
            normal = [-edge[1], edge[0]] # Rotate edge by 90 degrees counter-clockwise for outward normal
            normal_magnitude = math.sqrt(normal[0]**2 + normal[1]**2)
            if normal_magnitude > 0:
                normal = [normal[0] / normal_magnitude, normal[1] / normal_magnitude] # Normalize

            return normal
    return None # No collision

def reflect_velocity(velocity, normal, elasticity):
    """Reflects the velocity vector based on the collision normal and elasticity."""
    # v_out = v_in - 2 * (v_in . n) * n  (perfect reflection)
    # With elasticity:  v_out = v_in - (1 + elasticity) * (v_in . n) * n
    dot_product = velocity[0] * normal[0] + velocity[1] * normal[1]
    reflected_x = velocity[0] - (1 + elasticity) * dot_product * normal[0]
    reflected_y = velocity[1] - (1 + elasticity) * dot_product * normal[1]
    return [reflected_x, reflected_y]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(black)

    # Update hexagon rotation
    hexagon_angle += hexagon_rotation_speed

    # Calculate hexagon vertices based on rotation
    hexagon_vertices = calculate_hexagon_vertices(hexagon_center[0], hexagon_center[1], hexagon_radius, hexagon_angle)

    # --- Ball Physics ---
    # Apply gravity
    ball_velocity[1] += gravity

    # Apply friction (air resistance) - reduce velocity in both directions
    ball_velocity[0] *= (1 - friction)
    ball_velocity[1] *= (1 - friction)

    # Update ball position
    ball_position[0] += ball_velocity[0]
    ball_position[1] += ball_velocity[1]

    # --- Collision Detection and Handling ---
    collision_normal = check_collision(ball_position, ball_radius, hexagon_vertices)
    if collision_normal:
        ball_velocity = reflect_velocity(ball_velocity, collision_normal, bounce_elasticity)

        # Prevent ball from getting stuck *inside* the wall after collision (nudging it slightly out along the normal)
        overlap_magnitude = ball_radius # Approximation, but works reasonably well
        ball_position[0] += collision_normal[0] * overlap_magnitude * 0.1 # Small nudge
        ball_position[1] += collision_normal[1] * overlap_magnitude * 0.1

    # Floor and Ceiling Collision (optional - keeps ball somewhat contained if hexagon is off-center)
    if ball_position[1] + ball_radius > height:
        ball_position[1] = height - ball_radius
        ball_velocity[1] *= -bounce_elasticity
    elif ball_position[1] - ball_radius < 0:
        ball_position[1] = ball_radius
        ball_velocity[1] *= -bounce_elasticity
    # Left and Right Screen Boundaries (optional)
    if ball_position[0] + ball_radius > width:
        ball_position[0] = width - ball_radius
        ball_velocity[0] *= -bounce_elasticity
    elif ball_position[0] - ball_radius < 0:
        ball_position[0] = ball_radius
        ball_velocity[0] *= -bounce_elasticity


    # Draw everything
    draw_hexagon(screen, hexagon_vertices, hexagon_line_color)
    draw_ball(screen, ball_position, ball_radius, ball_color)

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60) # Limit to 60 frames per second

pygame.quit()