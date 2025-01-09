"""
3D visualization for the CubixTube puzzle using VPython.

This module provides functionality to visualize the CubixTube puzzle in 3D space,
representing corner pieces as L-shapes and straight pieces as lines with proper
orientations and colors.
"""

from vpython import box, vector, color, cylinder, compound, canvas, rate
from cubixtube import (
    CubixTube, CornerPiece, StraightPiece,
    initialize_front_face_solved, initialize_middle_layer_solved, initialize_back_face_solved,
    initialize_front_face, initialize_middle_layer, initialize_back_face
)

# Color mapping for VPython visualization
# Using slightly adjusted colors for better visibility
COLOR_MAP = {
    "Red": vector(1, 0, 0),      # Pure red
    "Blue": vector(0, 0, 1),     # Pure blue
    "Yellow": vector(1, 1, 0)    # Pure yellow
}

# Material properties for pieces
PIECE_MATERIAL = {
    "opacity": 0.8,           # Slight transparency for better depth perception
    "shininess": 0.7,         # Add some shine to make pieces more visible
    "emissive": False         # Don't make pieces glow
}

# Constants for visualization
PIECE_LENGTH = 0.4  # Length of a piece's arm
PIECE_THICKNESS = 0.1  # Thickness of pieces
GRID_SPACING = 1.2  # Space between piece centers (increased for better visibility)
GRID_OFFSET = vector(GRID_SPACING, GRID_SPACING, GRID_SPACING)  # Offset to center the cube

def create_corner_piece(pos, color_val, orientation):
    """
    Create a corner piece as two perpendicular cylinders.
    
    The orientation system follows:
    1-4: Up orientations (1: left, 2: forward, 3: right, 4: backward)
    5-8: Horizontal orientations (5: forward-left, 6: backward-left, 7: forward-right, 8: backward-right)
    9-12: Down orientations (9: left, 10: forward, 11: right, 12: backward)
    """
    # Base vectors for the L-shape
    base_arm1 = vector(0, PIECE_LENGTH, 0)  # Vertical arm
    base_arm2 = vector(PIECE_LENGTH, 0, 0)  # Horizontal arm
    
    # Orientation mappings
    orientation_transforms = {
        # Up orientations (1-4)
        1: (base_arm1, vector(-PIECE_LENGTH, 0, 0)),      # Up and left
        2: (base_arm1, vector(0, 0, PIECE_LENGTH)),       # Up and forward
        3: (base_arm1, vector(PIECE_LENGTH, 0, 0)),       # Up and right
        4: (base_arm1, vector(0, 0, -PIECE_LENGTH)),      # Up and backward
        
        # Horizontal orientations (5-8)
        5: (vector(-PIECE_LENGTH, 0, 0), vector(0, 0, PIECE_LENGTH)),    # Forward and left
        6: (vector(-PIECE_LENGTH, 0, 0), vector(0, 0, -PIECE_LENGTH)),   # Backward and left
        7: (vector(PIECE_LENGTH, 0, 0), vector(0, 0, PIECE_LENGTH)),     # Forward and right
        8: (vector(PIECE_LENGTH, 0, 0), vector(0, 0, -PIECE_LENGTH)),    # Backward and right
        
        # Down orientations (9-12)
        9: (vector(0, -PIECE_LENGTH, 0), vector(-PIECE_LENGTH, 0, 0)),   # Down and left
        10: (vector(0, -PIECE_LENGTH, 0), vector(0, 0, PIECE_LENGTH)),   # Down and forward
        11: (vector(0, -PIECE_LENGTH, 0), vector(PIECE_LENGTH, 0, 0)),   # Down and right
        12: (vector(0, -PIECE_LENGTH, 0), vector(0, 0, -PIECE_LENGTH)),  # Down and backward
    }
    
    # Get the appropriate vectors for this orientation
    arm1_axis, arm2_axis = orientation_transforms[orientation]

    # Create the two arms of the corner piece
    arm1 = cylinder(pos=pos, axis=arm1_axis, radius=PIECE_THICKNESS/2, 
                    color=color_val, opacity=PIECE_MATERIAL["opacity"],
                    shininess=PIECE_MATERIAL["shininess"], emissive=PIECE_MATERIAL["emissive"])
    arm2 = cylinder(pos=pos, axis=arm2_axis, radius=PIECE_THICKNESS/2,
                    color=color_val, opacity=PIECE_MATERIAL["opacity"],
                    shininess=PIECE_MATERIAL["shininess"], emissive=PIECE_MATERIAL["emissive"])
    
    return compound([arm1, arm2])

def create_straight_piece(pos, color_val, orientation):
    """
    Create a straight piece as a single cylinder.
    
    The orientation system for straight pieces:
    1: Horizontal (along x-axis)
    2: Through/Into the page (along z-axis)
    3: Vertical (along y-axis)
    """
    # Orientation mappings for straight pieces
    orientation_transforms = {
        1: vector(PIECE_LENGTH, 0, 0),        # Horizontal
        2: vector(0, 0, PIECE_LENGTH),        # Into the page
        3: vector(0, PIECE_LENGTH, 0)         # Vertical
    }
    
    # Get the appropriate vector for this orientation
    axis = orientation_transforms[orientation]
        
    return cylinder(pos=pos, axis=axis, radius=PIECE_THICKNESS/2,
                    color=color_val, opacity=PIECE_MATERIAL["opacity"],
                    shininess=PIECE_MATERIAL["shininess"], emissive=PIECE_MATERIAL["emissive"])

def visualize_cubix_tube(cube: CubixTube):
    """
    Create a 3D visualization of the CubixTube puzzle.
    
    Args:
        cube: A CubixTube instance containing the current state of the puzzle.
        
    Note:
        The visualization will open in a new window. Use mouse to rotate view:
        - Left click and drag to rotate
        - Right click and drag to zoom
        - Middle click and drag to pan
    """
    # Create a canvas for the 3D visualization
    scene = canvas(width=800, height=600, center=vector(0, 0, 0))
    scene.camera.pos = vector(3, 3, 3)
    scene.camera.axis = vector(-3, -3, -3)  # Point towards the origin
    scene.up = vector(0, 1, 0)  # Set up vector for proper orientation
    
    # Clear any existing objects
    for obj in scene.objects:
        obj.visible = False
    
    # Iterate through all positions in the cube
    for x in range(3):
        for y in range(3):
            for z in range(3):
                piece = cube.get_piece(x, y, z)
                if piece and not isinstance(piece, str):  # Skip None and center pieces
                    # Calculate the position in 3D space
                    # Offset the entire cube by GRID_OFFSET to center it
                    pos = vector(x * GRID_SPACING, y * GRID_SPACING, z * GRID_SPACING) - GRID_OFFSET
                    color_val = COLOR_MAP[piece.color]
                    
                    # Create the appropriate piece visualization
                    if isinstance(piece, CornerPiece):
                        create_corner_piece(pos, color_val, piece.orientation)
                    elif isinstance(piece, StraightPiece):
                        create_straight_piece(pos, color_val, piece.orientation)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize CubixTube puzzle state')
    parser.add_argument('--state', choices=['solved', 'custom'], default='solved',
                       help='Initial state of the cube (solved or custom configuration)')
    
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
    
    # Create the visualization
    visualize_cubix_tube(cube)
    
    # Keep the window open (VPython will handle the event loop)
    while True:
        rate(30)  # Limit to 30 FPS
