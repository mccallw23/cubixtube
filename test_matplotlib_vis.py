import matplotlib
matplotlib.use('Agg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def test_3d_plot():
    # Create figure and 3D axes
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Create vertices for a cube
    points = np.array([[-1, -1, -1],
                      [1, -1, -1],
                      [1, 1, -1],
                      [-1, 1, -1],
                      [-1, -1, 1],
                      [1, -1, 1],
                      [1, 1, 1],
                      [-1, 1, 1]])

    # Plot cube vertices
    ax.scatter(points[:, 0], points[:, 1], points[:, 2])

    # Plot cube edges
    for i in range(4):
        # Vertical edges
        ax.plot([points[i][0], points[i+4][0]],
                [points[i][1], points[i+4][1]],
                [points[i][2], points[i+4][2]], 'b')
        # Bottom face edges
        ax.plot([points[i][0], points[(i+1)%4][0]],
                [points[i][1], points[(i+1)%4][1]],
                [points[i][2], points[(i+1)%4][2]], 'b')
        # Top face edges
        ax.plot([points[i+4][0], points[((i+1)%4)+4][0]],
                [points[i+4][1], points[((i+1)%4)+4][1]],
                [points[i+4][2], points[((i+1)%4)+4][2]], 'b')

    # Set view angle for better visualization
    ax.view_init(elev=30, azim=45)

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Test 3D Visualization')

    # Save the plot
    plt.savefig('test_cube.png')
    print("Test visualization saved as test_cube.png")

if __name__ == "__main__":
    test_3d_plot()
