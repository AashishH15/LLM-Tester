import numpy as np
import matplotlib.pyplot as plt

# Define the function and its derivative
def f(x):
    return x**2

def df(x):
    return 2 * x

# Choose the point of tangency
x0 = 1
y0 = f(x0)
slope = df(x0)

# Define the tangent line function: y = f(x0) + f'(x0)*(x - x0)
def tangent(x):
    return y0 + slope * (x - x0)

# Create an array of x values
x_values = np.linspace(-2, 3, 400)
y_values = f(x_values)
y_tangent = tangent(x_values)

# Plot the parabola and the tangent line
plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values, label='f(x) = x^2')
plt.plot(x_values, y_tangent, '--', label='Tangent at x = 1')
plt.scatter([x0], [y0], color='red', zorder=5, label='Point of Tangency (1,1)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Parabola and Its Tangent Line at x=1')
plt.legend()
plt.grid(True)
plt.show()
