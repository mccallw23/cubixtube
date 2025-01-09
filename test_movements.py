"""
Test script to visualize CubixTube movements.
Generates visualizations for various cube states after different moves.
"""
from cubixtube import (
    CubixTube, initialize_front_face_solved, initialize_middle_layer_solved, 
    initialize_back_face_solved
)
from visualize_cubixtube import visualize_cubix_tube
import os
import shutil

def test_cube_movements():
    # Clean up and create output directory
    if os.path.exists("cube_moves"):
        shutil.rmtree("cube_moves")
    os.makedirs("cube_moves")

    # Initialize cube in solved state
    cube = CubixTube()
    initialize_front_face_solved(cube)
    initialize_middle_layer_solved(cube)
    initialize_back_face_solved(cube)

    # Test sequence of moves
    moves = [
        ("initial", lambda c: None),
        ("R", lambda c: c.R()),
        ("R_Prime", lambda c: c.R_Prime()),
        ("L", lambda c: c.L()),
        ("M_RL", lambda c: c.M_RL()),
        ("M_RL_Prime", lambda c: c.M_RL_Prime()),
    ]

    # Execute and visualize each move
    for move_name, move_func in moves:
        # Create a fresh cube for each move
        test_cube = CubixTube()
        initialize_front_face_solved(test_cube)
        initialize_middle_layer_solved(test_cube)
        initialize_back_face_solved(test_cube)
        
        # Apply the move and generate visualization
        move_func(test_cube)
        visualize_cubix_tube(test_cube, f"cube_moves/{move_name}")
        print(f"Generated visualization for {move_name}")

if __name__ == "__main__":
    test_cube_movements()
    print("\nMovement test visualizations generated in cube_moves/")
