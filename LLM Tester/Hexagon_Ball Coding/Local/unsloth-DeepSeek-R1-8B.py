import math

# Constants
ball_radius = 0.25
r = 1.5  # Radius of the hexagon
delta_theta = 0.1  # Rotation increment in radians per frame
gravity = 0.5  # Acceleration due to gravity
friction = 0.98  # Coefficient of friction

theta = 0.0  # Initial angle of rotation

# Initial position: center of the hexagon with a small y-offset to start moving down
ball_x, ball_y = r - ball_radius, 10.0
dx = 0.0  # Initial horizontal velocity
dy = -gravity * ball_radius  # Initial vertical velocity downward

# List to hold the polygon vertices' positions each frame
vertices = []
for k in range(6):
    angle = (k * 60.0 - theta) % 360.0
    x = r * math.cos(math.radians(angle))
    y = r * math.sin(math.radians(angle))
    vertices.append((x, y))

# Collision detection function for a line segment and point
def collide(segment, point, radius):
    v1, v2 = segment
    # Compute the line equation for the segment
    x0, y0 = v1
    x1, y1 = v2
    # Compute normal vector to the segment (perpendicular)
    dx_segment = x1 - x0
    dy_segment = y1 - y0
    dir_perp = (-dy_segment, dx_segment)  # Perpendicular direction
    len_seg = math.hypot(dx_segment, dy_segment)
    
    # Project point onto the line's direction and find closest point on segment
    proj_dir = (point[0] - x0) * dx_segment + (point[1] - y0) * dy_segment
    t = proj_dir / len_seg if len_seg != 0 else 0.0
    t_clamped = max(0.0, min(1.0, t))
    
    closest_x = x0 + dx_segment * t_clamped
    closest_y = y0 + dy_segment * t_clamped
    
    # Compute distance from point to closest point on segment
    dist = math.hypot(point[0] - closest_x, point[1] - closest_y)
    return dist <= radius

# Main simulation loop
import sys
input = sys.stdin.read(1)
while True:
    if input:
        break
    
    # Rotate the hexagon's vertices by delta_theta
    # global theta
    theta += delta_theta
    # Update vertices' positions
    vertices = []
    for k in range(6):
        angle = (k * 60.0 - theta) % 360.0
        x = r * math.cos(math.radians(angle))
        y = r * math.sin(math.radians(angle))
        vertices.append((x, y))
    
    # Update ball position based on gravity and friction
    if abs(dy) < 1e-8:
        dx *= friction
        dy = 0.0
    else:
        dy += gravity * (ball_y - (-ball_radius))  # Apply gravity
        dy *= friction
    
    # Add some air resistance or adjust as needed
    if abs(dx) > 1e-8:
        dx *= friction
    ball_x += dx
    ball_y += dy
    
    # Check for collision with any of the hexagon's sides
    for i in range(6):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % 6]
        if collide((v1, v2), (ball_x, ball_y), ball_radius):
            # Calculate relative velocity component perpendicular to the wall
            x0, y0 = v1
            x1, y1 = v2
            dx_segment = x1 - x0
            dy_segment = y1 - y0
            len_seg = math.hypot(dx_segment, dy_segment)
            
            # Vector from segment midpoint to point
            vec_x = ball_x - (x0 + 0.5 * dx_segment)
            vec_y = ball_y - (y0 + 0.5 * dy_segment)
            
            # Perpendicular velocity component
            normal_dx = -dy_segment
            normal_dy = dx_segment
            perp_velocity = vec_x * normal_dx + vec_y * normal_dy
            
            # Reflect the velocity component perpendicular to the wall
            reflection_factor = (perp_velocity / len_seg) * (-len_seg)
            dy -= 2 * reflection_factor
            dx += -reflection_factor * dy_segment / len_seg
            
            # Update position based on remaining movement after bounce
            ball_x = v1[0] + v1[0] - ball_x
            ball_y = v1[1] + v1[1] - ball_y
    
    print(f"Ball pos: ({ball_x:.3f}, {ball_y:.3f}), Vel: ({dx:.3f}, {dy:.3f})")
    input = sys.stdin.read(1)
