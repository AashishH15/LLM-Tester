import math

class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0.1
        self.dy = 0
        self.radius = 5

class Hexagon:
    def __init__(self, center, size, color, rotation_speed):
        self.center = center
        self.size = size
        self.color = color
        self.rotation_speed = rotation_speed

def main():
    width = 800
    height = 600
    ball = Ball()
    
    # Initialize the hexagon with proper dimensions and rotation
    center_x = (width // 2)
    center_y = (height // 2) - 50  # Adjusting for screen edges
    hex_size = width * 0.7
    hex_color = "red"
    hex_rot_speed = 1
    
    my_hexagon = Hexagon((center_x, center_y), hex_size, hex_color, hex_rot_speed)
    
    gravity = 0.1
    friction = 0.98
    
    dt = 1  # Time step for each frame
    
    while True:
        ball.x += (ball.dx) * dt
        ball.y += (ball.dy + gravity * dt) * dt
        
        dx = ball.dx
        dy = ball.dy
        
        # Applying friction to velocity
        dx *= friction
        dy *= friction
        
        # Check for wall collisions and update angles accordingly
        bounce_angle = 0.5  # Coefficient affecting the angle after collision
        
        if (ball.x - ball.radius < my_hexagon.size / 2 or 
            ball.x + ball.radius > width - my_hexagon.size / 2):
            dx *= -1
            
        # Calculate distance from center to determine rotation
        distance = math.sqrt((ball.x - my_hexagon.center[0])**2 + (ball.y - my_hexagon.center[1])**2)
        
        if distance < my_hexagon.size / 2:
            angle = math.atan2(ball.y - my_hexagon.center[1], ball.x - my_hexagon.center[0])
            rotated_dx = dx * math.cos(bounce_angle) - dy * math.sin(bounce_angle)
            rotated_dy = dx * math.sin(bounce_angle) + dy * math.cos(bounce_angle)
            
            ball.dx, ball.dy = rotated_dx, rotated_dy
        
        # Draw the screen
        import random
        color = my_hexagon.color
        if distance < (my_hexagon.size / 2):
            color = "white"
        
        for _ in range(40):  # Number of dots to simulate the center
            rdx = int((ball.x - ball.radius) + (ball.dx * random.uniform(-1, 1)))
            rdY = int((ball.y - ball.radius) + (ball.dy * random.uniform(-1, 1)))
            
            if (
                abs(rdx - my_hexagon.center[0]) < ball.radius and 
                abs(rdY - my_hexagon.center[1]) < ball.radius
            ):
                rdx += dx
                rdY += dy
                
        import matplotlib.pyplot as plt
        figure = plt.figure()
        axes = figure.add_subplot(1, 1, 1)
        axes.set_xlim(0, width)
        axes.set_ylim(height - 600, height + 600)
        
        for _ in range(40):
            x = int(rdx) + my_hexagon.center[0]
            y = int(rdY) + my_hexagon.center[1]
            
            if (abs(x - center_x) < hex_size / 2 and 
                abs(y - center_y) < hex_size / 2):
                axes.scatter(x, y, c=color, edgecolor='black', s=40)
        
        import random
        for _ in range(100):  # Number of dots to simulate the ball's movement
            rdx = int((ball.x - ball.radius) + (ball.dx * random.uniform(-1, 1)))
            rdY = int((ball.y - ball.radius) + (ball.dy * random.uniform(-1, 1)))
            
            if (
                abs(rdx - my_hexagon.center[0]) < ball.radius and 
                abs(rdY - my_hexagon.center[1]) < ball.radius
            ):
                rdx += dx
                rdY += dy
                
        plt.show()

if __name__ == "__main__":
    main()
