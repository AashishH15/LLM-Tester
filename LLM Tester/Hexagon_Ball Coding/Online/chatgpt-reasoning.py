import pygame
import sys
import math

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Physics parameters (in pixels/second², etc.)
GRAVITY = 500              # downward acceleration (pixels/s²)
AIR_FRICTION = 0.999       # slight damping of velocity each frame

# Ball properties
BALL_RADIUS = 15
BALL_COLOR = (255, 0, 0)

# Hexagon (bouncing container) properties
HEXAGON_COLOR = (0, 255, 0)
HEXAGON_CENTER = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
HEXAGON_RADIUS = 250       # distance from center to vertex
NUM_SIDES = 6              # hexagon
angular_velocity = 5.0     # rotation speed in radians per second
hex_rotation = 0.0         # current rotation angle

# Collision response parameters
RESTITUTION = 0.9          # bounciness (1.0 = perfectly elastic)
WALL_FRICTION = 0.1        # friction along the wall surface

# --- Helper Functions ---
def get_hexagon_vertices(center, radius, rotation):
    """
    Returns a list of vertices for a regular hexagon (or NUM_SIDES polygon)
    rotated by 'rotation' (radians) about the center.
    """
    vertices = []
    for i in range(NUM_SIDES):
        angle = rotation + (2 * math.pi * i / NUM_SIDES)
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        vertices.append(pygame.math.Vector2(x, y))
    return vertices

def closest_point_on_segment(A, B, P):
    """
    Returns the closest point on line segment AB to point P,
    along with the projection factor t (0 ≤ t ≤ 1 means interior of segment).
    """
    AB = B - A
    ab2 = AB.length_squared()
    if ab2 == 0:
        return A, 0
    t = (P - A).dot(AB) / ab2
    if t < 0:
        return A, t
    elif t > 1:
        return B, t
    else:
        return A + AB * t, t

def edge_interior_normal(A, B, hex_center):
    """
    Returns the inward-pointing (normalized) normal for edge AB.
    (The “inside” of the hexagon is assumed to contain hex_center.)
    """
    edge = B - A
    # Two perpendicular candidates
    candidate1 = pygame.math.Vector2(edge.y, -edge.x)
    candidate2 = pygame.math.Vector2(-edge.y, edge.x)
    mid = (A + B) / 2
    # Choose the candidate that points toward the hexagon center.
    if (hex_center - mid).dot(candidate1) > 0:
        return candidate1.normalize()
    else:
        return candidate2.normalize()

# --- Main Program ---
def main():
    global hex_rotation  # Use the global hex_rotation variable
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")
    clock = pygame.time.Clock()

    # Initialize ball state (starting near the center with an initial velocity)
    ball_pos = pygame.math.Vector2(HEXAGON_CENTER)
    ball_vel = pygame.math.Vector2(200, -100)  # pixels per second

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds passed since last frame

        # --- Event Processing ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Update Simulation ---
        # Update hexagon rotation angle.
        hex_rotation += angular_velocity * dt

        # Update ball velocity with gravity and slight air friction.
        ball_vel.y += GRAVITY * dt
        ball_vel *= AIR_FRICTION

        # Update ball position.
        ball_pos += ball_vel * dt

        # Get current (rotated) hexagon vertices.
        vertices = get_hexagon_vertices(HEXAGON_CENTER, HEXAGON_RADIUS, hex_rotation)

        # Check collisions with each hexagon edge.
        for i in range(NUM_SIDES):
            A = vertices[i]
            B = vertices[(i + 1) % NUM_SIDES]
            closest, t_val = closest_point_on_segment(A, B, ball_pos)
            distance = (ball_pos - closest).length()

            if distance < BALL_RADIUS:
                # Determine penetration depth.
                penetration = BALL_RADIUS - distance

                # Determine the collision normal.
                # If the collision is with the "flat" part of the edge (0 ≤ t ≤ 1),
                # use the wall’s interior normal; otherwise (collision near a vertex)
                # use the normalized vector from the vertex to the ball.
                if 0 <= t_val <= 1:
                    normal = edge_interior_normal(A, B, HEXAGON_CENTER)
                else:
                    # If hitting an endpoint, use the vector from that endpoint.
                    if t_val < 0:
                        endpoint = A
                    else:
                        endpoint = B
                    if (ball_pos - endpoint).length() != 0:
                        normal = (ball_pos - endpoint).normalize()
                    else:
                        normal = pygame.math.Vector2(0, -1)  # arbitrary fallback

                # Push the ball out of the wall to resolve penetration.
                ball_pos += normal * penetration

                # Compute the wall’s velocity at the collision point.
                rel_pos = closest - HEXAGON_CENTER
                # In 2D, the velocity due to rotation: v = ω × r.
                wall_velocity = pygame.math.Vector2(-angular_velocity * rel_pos.y,
                                                      angular_velocity * rel_pos.x)

                # Compute the ball's velocity relative to the moving wall.
                rel_velocity = ball_vel - wall_velocity

                # Only resolve the collision if the ball is moving into the wall.
                if rel_velocity.dot(normal) < 0:
                    # Decompose relative velocity into normal and tangential components.
                    vn = normal * rel_velocity.dot(normal)
                    vt = rel_velocity - vn

                    # Reflect the normal component (with restitution)
                    # and reduce the tangential component (simulate friction).
                    new_rel_velocity = -RESTITUTION * vn + (1 - WALL_FRICTION) * vt

                    # Transform back to the stationary frame.
                    ball_vel = new_rel_velocity + wall_velocity

        # --- Drawing ---
        screen.fill((0, 0, 0))  # black background

        # Draw the hexagon (as a polygon outline).
        hex_points = [(v.x, v.y) for v in vertices]
        pygame.draw.polygon(screen, HEXAGON_COLOR, hex_points, 3)

        # Draw the ball.
        pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos.x), int(ball_pos.y)), BALL_RADIUS)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
