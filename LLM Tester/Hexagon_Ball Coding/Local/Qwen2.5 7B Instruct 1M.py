import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Bouncing in a Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ball properties
BALL_RADIUS = 20
BALL_X, BALL_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100
BALL_VEL_X, BALL_VEL_Y = random.uniform(-5, 5), random.uniform(-5, 5)
GRAVITY = 0.7
FRICTION = 0.98

# Hexagon properties
HEX_RADIUS = SCREEN_WIDTH // 4
HEX_CENTRE_X = SCREEN_WIDTH // 2
HEX_CENTRE_Y = SCREEN_HEIGHT // 2
HEX_SIDES = 6
ROTATION_SPEED = math.pi / 120  # Rotate hexagon by this much each frame

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

def draw_hexagon(x, y, radius):
    vertices = []
    for i in range(HEX_SIDES):
        angle = (i * math.pi * 2 / HEX_SIDES) - (math.pi / 2)
        vertex_x = x + int(radius * math.cos(angle))
        vertex_y = y + int(radius * math.sin(angle))
        vertices.append((vertex_x, vertex_y))
    pygame.draw.polygon(screen, BLACK, vertices)

def draw_ball(x, y):
    pygame.draw.circle(screen, RED, (int(x), int(y)), BALL_RADIUS)

def vector_length(vx, vy):
    return math.sqrt(vx**2 + vy**2)

def normalize_vector(vx, vy):
    length = vector_length(vx, vy)
    if length == 0:
        return vx, vy
    else:
        return vx / length, vy / length

# Initialize the rotation angle for the hexagon
HEX_ANGLE = 0

def check_line_intersection(p1, p2, q1, q2):
    # Function to determine if two line segments intersect
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    return ccw(p1, q2, q1) != ccw(p2, q2, q1) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation angle
    HEX_ANGLE += ROTATION_SPEED
    HEX_CENTRE_X += math.cos(HEX_ANGLE) * HEX_RADIUS
    HEX_CENTRE_Y += math.sin(HEX_ANGLE) * HEX_RADIUS

    screen.fill(WHITE)

    # Calculate new ball position and velocity
    BALL_X += BALL_VEL_X
    BALL_Y += BALL_VEL_Y

    # Apply gravity
    BALL_VEL_Y += GRAVITY

    # Friction (reduce x and y velocities)
    BALL_VEL_X *= FRICTION
    BALL_VEL_Y *= FRICTION

    # Check collision with hexagon walls
    HEX_CENTRE_X = HEX_CENTRE_X + math.cos(HEX_ANGLE) * HEX_RADIUS
    HEX_CENTRE_Y = HEX_CENTRE_Y + math.sin(HEX_ANGLE) * HEX_RADIUS

    vertices = []
    for i in range(HEX_SIDES):
        angle = (i * math.pi * 2 / HEX_SIDES) - (math.pi / 2)
        vertex_x = HEX_CENTRE_X + int(math.cos(angle + HEX_ANGLE) * HEX_RADIUS)
        vertex_y = HEX_CENTRE_Y + int(math.sin(angle + HEX_ANGLE) * HEX_RADIUS)
        vertices.append((vertex_x, vertex_y))

    for i in range(HEX_SIDES):
        angle1 = (i * math.pi * 2 / HEX_SIDES) - (math.pi / 2)
        x1 = HEX_CENTRE_X + int(math.cos(angle1 + HEX_ANGLE) * HEX_RADIUS)
        y1 = HEX_CENTRE_Y + int(math.sin(angle1 + HEX_ANGLE) * HEX_RADIUS)

        for j in range(i, len(vertices)):
            angle2 = (j * math.pi * 2 / HEX_SIDES) - (math.pi / 2)
            x2 = HEX_CENTRE_X + int(math.cos(angle2 + HEX_ANGLE) * HEX_RADIUS)
            y2 = HEX_CENTRE_Y + int(math.sin(angle2 + HEX_ANGLE) * HEX_RADIUS)

            # Check if ball is inside the hexagon
            def line_segment_intersection(x1, y1, x2, y2):
                return (x1 == x2) or (y1 == y2)

            if not line_segment_intersection(x1, y1, x2, y2):
                intersection = check_line_intersection((BALL_X, BALL_Y), (BALL_X + BALL_VEL_X * 50, BALL_Y + BALL_VEL_Y * 50),
                                                       (x1, y1), (x2, y2))
                if intersection:
                    collision_angle = math.atan2(x2 - x1, y2 - y1)
                    normal_vector = normalize_vector(math.cos(collision_angle), math.sin(collision_angle))

                    # Calculate reflection vector
                    tangent_vector = (-normal_vector[1], normal_vector[0])
                    reflected_vector = (BALL_VEL_X * math.cos(2 * collision_angle) - BALL_VEL_Y * math.sin(2 * collision_angle),
                                        BALL_VEL_Y * math.cos(2 * collision_angle) + BALL_VEL_X * math.sin(2 * collision_angle))

                    # Normalize and scale the reflected vector
                    reflected_vector = normalize_vector(reflected_vector[0], reflected_vector[1])
                    reflected_vector = (reflected_vector[0] * 3, reflected_vector[1] * 3)

                    # Update ball velocity after collision
                    BALL_VEL_X = reflected_vector[0]
                    BALL_VEL_Y = reflected_vector[1]

                    # Apply friction to the new velocity
                    BALL_VEL_X *= FRICTION
                    BALL_VEL_Y *= FRICTION

                    break

    # Draw hexagon and ball
    draw_hexagon(HEX_CENTRE_X, HEX_CENTRE_Y, HEX_RADIUS)
    draw_ball(BALL_X, BALL_Y)

    # Cap the frame rate
    clock.tick(FPS)

    # Update the display
    pygame.display.flip()

pygame.quit()
