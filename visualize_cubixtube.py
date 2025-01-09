"""
3D visualization for the CubixTube puzzle using Matplotlib.

This module provides functionality to visualize the CubixTube puzzle in 3D space,
representing corner pieces as L-shapes and straight pieces as lines with proper
orientations and colors.
"""

import matplotlib
matplotlib.use('Agg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
from typing import cast
from cubixtube import (
    CubixTube, CornerPiece, StraightPiece,
    initialize_front_face_solved, initialize_middle_layer_solved, initialize_back_face_solved,
    initialize_front_face, initialize_middle_layer, initialize_back_face
)

# Color mapping for Matplotlib visualization
COLOR_MAP = {
    "Red": 'red',      # Pure red
    "Blue": 'blue',    # Pure blue
    "Yellow": 'yellow',# Pure yellow
    "Gray": 'gray'     # Gray for center pieces
}

# Constants for visualization
PIECE_LENGTH = 0.4  # Length of a piece's arm
GRID_SPACING = 1.0  # Space between piece centers
MARKER_SIZE = 100   # Size for center piece markers

def create_corner_piece(ax, pos, color_val, orientation):
    """
    Create a corner piece as two perpendicular lines using matplotlib.
    
    The orientation system follows:
    1-4: Up orientations (1: left, 2: forward, 3: right, 4: backward)
    5-8: Horizontal orientations (5: forward-left, 6: backward-left, 7: forward-right, 8: backward-right)
    9-12: Down orientations (9: left, 10: forward, 11: right, 12: backward)
    """
    # Base vectors for the L-shape
    orientation_transforms = {
        # Up orientations (1-4)
        1: ([0, PIECE_LENGTH, 0], [-PIECE_LENGTH, 0, 0]),      # Up and left
        2: ([0, PIECE_LENGTH, 0], [0, 0, PIECE_LENGTH]),       # Up and forward
        3: ([0, PIECE_LENGTH, 0], [PIECE_LENGTH, 0, 0]),       # Up and right
        4: ([0, PIECE_LENGTH, 0], [0, 0, -PIECE_LENGTH]),      # Up and backward
        
        # Horizontal orientations (5-8)
        5: ([-PIECE_LENGTH, 0, 0], [0, 0, PIECE_LENGTH]),    # Forward and left
        6: ([-PIECE_LENGTH, 0, 0], [0, 0, -PIECE_LENGTH]),   # Backward and left
        7: ([PIECE_LENGTH, 0, 0], [0, 0, PIECE_LENGTH]),     # Forward and right
        8: ([PIECE_LENGTH, 0, 0], [0, 0, -PIECE_LENGTH]),    # Backward and right
        
        # Down orientations (9-12)
        9: ([0, -PIECE_LENGTH, 0], [-PIECE_LENGTH, 0, 0]),   # Down and left
        10: ([0, -PIECE_LENGTH, 0], [0, 0, PIECE_LENGTH]),   # Down and forward
        11: ([0, -PIECE_LENGTH, 0], [PIECE_LENGTH, 0, 0]),   # Down and right
        12: ([0, -PIECE_LENGTH, 0], [0, 0, -PIECE_LENGTH]),  # Down and backward
    }
    
    # Get the appropriate vectors for this orientation
    arm1_vec, arm2_vec = orientation_transforms[orientation]
    
    # Plot first arm
    x = [pos[0], pos[0] + arm1_vec[0]]
    y = [pos[1], pos[1] + arm1_vec[1]]
    z = [pos[2], pos[2] + arm1_vec[2]]
    ax.plot(x, y, z, color=color_val, linewidth=2)
    
    # Plot second arm
    x = [pos[0], pos[0] + arm2_vec[0]]
    y = [pos[1], pos[1] + arm2_vec[1]]
    z = [pos[2], pos[2] + arm2_vec[2]]
    ax.plot(x, y, z, color=color_val, linewidth=2)

def create_straight_piece(ax, pos, color_val, orientation):
    """
    Create a straight piece as a single line using matplotlib.
    
    The orientation system for straight pieces:
    1: Horizontal (along x-axis)
    2: Through/Into the page (along z-axis)
    3: Vertical (along y-axis)
    """
    # Map all orientations to one of the three basic orientations (1, 2, 3)
    basic_orientation = orientation % 3 if orientation % 3 != 0 else 3
    orientation_vectors = {
        1: [PIECE_LENGTH, 0, 0],        # Horizontal (x-axis)
        2: [0, 0, PIECE_LENGTH],        # Into the page (z-axis)
        3: [0, PIECE_LENGTH, 0]         # Vertical (y-axis)
    }
    
    # Get the appropriate vector for this orientation
    vec = orientation_vectors[basic_orientation]
    
    # Plot the line
    x = [pos[0], pos[0] + vec[0]]
    y = [pos[1], pos[1] + vec[1]]
    z = [pos[2], pos[2] + vec[2]]
    ax.plot(x, y, z, color=color_val, linewidth=2)

def visualize_cubix_tube(cube: CubixTube, output_dir="cube_views"):
    """
    Create a 3D visualization of the CubixTube puzzle using matplotlib.
    
    Args:
        cube: A CubixTube instance containing the current state of the puzzle.
        output_dir: Directory to save the visualization images.
        
    Note:
        Generates multiple views of the cube from different angles and saves them as PNG files.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Define different view angles
    views = {
        'isometric': (30, 45),   # (elevation, azimuth)
        'front': (0, 0),
        'top': (90, -90),
        'right': (0, 90)
    }
    
    for view_name, (elev, azim) in views.items():
        # Create figure and 3D axes for each view
        fig = plt.figure(figsize=(10, 10))
        ax = cast(Axes3D, fig.add_subplot(111, projection='3d'))
        
        # Calculate grid offset to center the cube
        offset = np.array([GRID_SPACING, GRID_SPACING, GRID_SPACING])
        
        # Iterate through all positions in the cube
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    piece = cube.get_piece(x, y, z)
                    if piece:  # Handle all non-None pieces
                        # Calculate the position in 3D space
                        pos = np.array([x * GRID_SPACING, y * GRID_SPACING, z * GRID_SPACING]) - offset
                        
                        if isinstance(piece, str):  # Handle center pieces
                            color = COLOR_MAP["Blue"] if piece == "Blue Center" else COLOR_MAP["Gray"]
                            ax.scatter(pos[0], pos[1], pos[2], marker='o', color=color, s=100)
                        else:  # Handle corner and straight pieces
                            color_val = COLOR_MAP[piece.color]
                            if isinstance(piece, CornerPiece):
                                create_corner_piece(ax, pos, color_val, piece.orientation)
                            elif isinstance(piece, StraightPiece):
                                create_straight_piece(ax, pos, color_val, piece.orientation)
        
        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        try:
            ax.set_zlabel('Z')
        except AttributeError:
            pass  # Some matplotlib versions don't support set_zlabel
            
        ax.set_title(f'CubixTube - {view_name.capitalize()} View')
        
        # Set axis limits
        ax.set_xlim((-1.5, 1.5))
        ax.set_ylim((-1.5, 1.5))
        try:
            ax.set_zlim((-1.5, 1.5))
        except AttributeError:
            pass  # Some matplotlib versions don't support set_zlim
            
        # Set the view angle
        try:
            ax.view_init(elev=elev, azim=azim)
        except AttributeError:
            pass  # Some matplotlib versions don't support view_init
        
        # Save the plot
        plt.savefig(f'{output_dir}/{view_name}.png')
        plt.close()

if __name__ == "__main__":
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description='Visualize CubixTube puzzle state')
    parser.add_argument('--state', choices=['solved', 'custom'], default='solved',
                       help='Initial state of the cube (solved or custom configuration)')
    parser.add_argument('--output-dir', default='cube_views',
                       help='Directory to save visualization images')
    
    args = parser.parse_args()
    
    # Create a new CubixTube instance
    cube = CubixTube()
    
    if args.state == 'solved':
        # Initialize the solved state
        initialize_front_face_solved(cube)
        initialize_middle_layer_solved(cube)
        initialize_back_face_solved(cube)
    else:
        # Initialize with a custom configuration
        initialize_front_face(cube)
        initialize_middle_layer(cube)
        initialize_back_face(cube)
    
    # Create the visualization and save views
    visualize_cubix_tube(cube, args.output_dir)
    print(f"Visualization images saved to {os.path.abspath(args.output_dir)}/")
    print("Generated views: isometric.png, front.png, top.png, right.png")
