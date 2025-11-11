import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
BALL_COLOR = (255, 0, 0)
HEXAGON_COLOR = (255, 255, 255)
FPS = 60

# Ball properties
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_radius = 10
ball_velocity = [2, 2]
GRAVITY = 0.5
FRICTION = 0.99

# Hexagon properties
hexagon_center = [WIDTH // 2, HEIGHT // 2]
hexagon_radius = 200
rotation_speed = 2  # degrees per frame
hexagon_points = []

def create_hexagon(center, radius):
    angles = [i * (math.pi * 2) / 6 for i in range(6)]
    points = [(center[0] + math.cos(angle) * radius, center[1] + math.sin(angle) * radius) for angle in angles]
    return points

def rotate_hexagon(points, center, angle):
    rotated_points = []
    rad_angle = math.radians(angle)
    cos_val, sin_val = math.cos(rad_angle), math.sin(rad_angle)
    for point in points:
        translated = (point[0] - center[0], point[1] - center[1])
        x_new = translated[0] * cos_val - translated[1] * sin_val
        y_new = translated[0] * sin_val + translated[1] * cos_val
        rotated_points.append((x_new + center[0], y_new + center[1]))
    return rotated_points

def draw_hexagon(screen, points, color):
    pygame.draw.polygon(screen, color, points)

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def closest_point_on_line(a, b, p):
    ap = [p[0] - a[0], p[1] - a[1]]
    ab = [b[0] - a[0], b[1] - a[1]]
    ab_squared = ab[0]**2 + ab[1]**2
    t = max(0, min(1, (ap[0]*ab[0] + ap[1]*ab[1]) / ab_squared))
    return [a[0] + t*ab[0], a[1] + t*ab[1]]

def reflect_velocity(normal):
    ball_to_center = [ball_pos[0] - hexagon_center[0], ball_pos[1] - hexagon_center[1]]
    normal_length = math.sqrt(normal[0]**2 + normal[1]**2)
    if normal_length == 0:
        return
    normal_unit = [normal[0]/normal_length, normal[1]/normal_length]
    velocity = ball_velocity
    dot_product = velocity[0]*normal_unit[0] + velocity[1]*normal_unit[1]
    ball_velocity[0] -= 2 * dot_product * normal_unit[0]
    ball_velocity[1] -= 2 * dot_product * normal_unit[1]

def main():
    global hexagon_points, ball_pos, ball_velocity
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    rotation_angle = 0

    hexagon_points = create_hexagon(hexagon_center, hexagon_radius)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Rotate the hexagon
        rotation_angle = (rotation_angle + rotation_speed) % 360
        rotated_hexagon = rotate_hexagon(hexagon_points, hexagon_center, rotation_angle)
        draw_hexagon(screen, rotated_hexagon, HEXAGON_COLOR)

        # Move the ball
        ball_velocity[1] += GRAVITY
        ball_pos[0] += ball_velocity[0]
        ball_pos[1] += ball_velocity[1]

        # Apply friction
        ball_velocity[0] *= FRICTION
        ball_velocity[1] *= FRICTION

        # Check for collision with hexagon walls
        for i in range(6):
            a = rotated_hexagon[i]
            b = rotated_hexagon[(i+1) % 6]
            closest = closest_point_on_line(a, b, ball_pos)
            d = distance(closest, ball_pos)
            if d <= ball_radius:
                # Collision detected
                normal = [ball_pos[0] - closest[0], ball_pos[1] - closest[1]]
                reflect_velocity(normal)
                break

        # Draw the ball
        pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
