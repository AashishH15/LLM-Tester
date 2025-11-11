import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
GRAVITY = -9.81  # Acceleration due to gravity (m/s^2)
FRICTION = 0.1   # Coefficient of friction
TIME_STEP = 0.05  # Time step for simulation
RADIUS = 0.5     # Radius of the hexagon and ball
MASS = 1.0       # Mass of the ball (for friction calculation)

# Hexagon properties
NUM_SIDES = 6
SIDE_LENGTH = 2 * RADIUS / np.sqrt(3)

# Initial conditions
initial_position = np.array([0, 0, RADIUS])
velocity = np.array([0, 0, 0])

def rotate_vector(vector, axis, angle):
    """Rotate a vector by an angle around a given axis."""
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    cross_product = np.cross([0, 0, 1], axis)
    rotation_matrix = np.array([
        [cos_theta + axis[0]**2 * (1 - cos_theta), axis[0] * axis[1] * (1 - cos_theta) - axis[2] * sin_theta, axis[0] * axis[2] * (1 - cos_theta) + axis[1] * sin_theta],
         [axis[1] * axis[0] * (1 - cos_theta) + axis[2] * sin_theta, cos_theta + axis[1]**2 * (1 - cos_theta), axis[1] * axis[2] * (1 - cos_theta) - axis[0] * sin_theta],
         [axis[2] * axis[0] * (1 - cos_theta) - axis[1] * sin_theta, axis[2] * axis[1] * (1 - cos_theta) + axis[0] * sin_theta, cos_theta + axis[2]**2 * (1 - cos_theta)]
    ])
    return np.dot(rotation_matrix, vector)

def hexagon_vertices(center, radius):
    """Generate vertices of a regular hexagon."""
    angles = np.linspace(0, 2 * np.pi, NUM_SIDES + 1)
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    z = np.full_like(x, center[2])
    return np.vstack((x, y, z)).T

def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    vertices = hexagon_vertices([0, 0, RADIUS], RADIUS)
    faces = [[0, i+1, i+2] for i in range(NUM_SIDES-1)] + [[0, NUM_SIDES, 1]]
    
    ax.plot_trisurf(*vertices.T, triangles=faces, color='blue')
    
    ball, = ax.plot([], [], [], 'o', color='red')
    time_counter = 0
    
    while True:
        # Update position and velocity due to gravity and friction
        acceleration = np.array([0, 0, GRAVITY])
        velocity += acceleration * TIME_STEP
        velocity *= (1 - FRICTION)
        
        initial_position += velocity * TIME_STEP
        
        # Check for collisions with the hexagon walls
        if abs(initial_position[2] - RADIUS) <= RADIUS:
            velocity[2] = -velocity[2]  # Bounce off the ground/ceiling
        
        for i in range(NUM_SIDES):
            vertex1 = vertices[i]
            vertex2 = vertices[(i+1) % NUM_SIDES]
            
            if np.dot(initial_position - vertex1, vertex2 - vertex1) < 0:
                normal = (vertex2 - vertex1) / np.linalg.norm(vertex2 - vertex1)
                velocity -= 2 * np.dot(velocity, normal) * normal
        
        # Update plot
        ball.set_data([initial_position[0]], [initial_position[1]])
        ball.set_3d_properties([initial_position[2]])
        
        plt.draw()
        plt.pause(TIME_STEP)
        time_counter += TIME_STEP
    
if __name__ == "__main__":
    main()
