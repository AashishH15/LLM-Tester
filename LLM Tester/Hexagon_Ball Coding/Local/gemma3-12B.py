import pygame
import math

# --- Constants ---
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# --- Ball Properties ---
BALL_RADIUS = 20
GRAVITY = 0.5
FRICTION = 0.1
BOUNCE_DAMPING = 0.8  # Reduce velocity after bounce

# --- Hexagon Properties ---
HEXAGON_SIZE = 200
HEXAGON_COLOR = BLUE
ROTATION_SPEED = 0.5 # Degrees per frame

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
clock = pygame.time.Clock()


# --- Helper Functions ---
def calculate_hexagon_coordinates(center_x, center_y, size):
    """Calculates the coordinates of the hexagon's vertices."""
    vertices = []
    for i in range(6):
        angle = math.radians(i * 60)  # 60 degrees per vertex
        x = center_x + size * math.cos(angle)
        y = center_y + size * math.sin(angle)
        vertices.append((x, y))
    return vertices

def distance(point1, point2):
    """Calculates the distance between two points."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


# --- Ball Class ---
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0  # Velocity in x direction
        self.vy = 0  # Velocity in y direction

    def update(self, hexagon_vertices):
        """Updates the ball's position and velocity."""
        # Apply gravity
        self.vy += GRAVITY

        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

        # Collision detection and response with walls
        for vertex in hexagon_vertices:
            dist = distance((self.x, self.y), vertex)
            if dist < BALL_RADIUS:
                # Calculate normal vector (vector from the ball to the wall)
                normal_x = vertex[0] - self.x
                normal_y = vertex[1] - self.y
                norm_length = math.sqrt(normal_x**2 + normal_y**2)
                normal_x /= norm_length
                normal_y /= norm_length

                # Calculate dot product of velocity and normal vector
                dot_product = self.vx * normal_x + self.vy * normal_y

                # Reverse the component of velocity along the normal
                self.vx -= 2 * dot_product * normal_x
                self.vy -= 2 * dot_product * normal_y

                # Apply damping to reduce velocity after bounce
                self.vx *= BOUNCE_DAMPING
                self.vy *= BOUNCE_DAMPING

        # Friction
        self.vx *= (1 - FRICTION)
        self.vy *= (1 - FRICTION)


    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), BALL_RADIUS)



# --- Main Program ---

# Calculate hexagon vertices
center_x = WIDTH // 2
center_y = HEIGHT // 2
hexagon_vertices = calculate_hexagon_coordinates(center_x, center_y, HEXAGON_SIZE)


# Create the ball
ball = Ball(WIDTH // 2, HEIGHT // 2)

rotation_angle = 0  # Initial rotation angle of the hexagon

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position and velocity
    ball.update(hexagon_vertices)

    # Rotate the hexagon vertices
    rotated_vertices = []
    for vertex in hexagon_vertices:
        rad = math.radians(rotation_angle)
        new_x = vertex[0] * math.cos(rad) - vertex[1] * math.sin(rad)
        new_y = vertex[0] * math.sin(rad) + vertex[1] * math.cos(rad)
        rotated_vertices.append((new_x, new_y))

    # Draw the hexagon
    pygame.draw.polygon(screen, HEXAGON_COLOR, rotated_vertices)

    # Draw the ball
    ball.draw(screen)


    # Update display
    pygame.display.flip()

    # Control rotation speed
    rotation_angle += ROTATION_SPEED

    clock.tick(FPS)

pygame.quit()