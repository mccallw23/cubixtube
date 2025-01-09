"""
Verification script for CubixTube visualization.
Prints the cube configuration for manual verification.
"""
from cubixtube import (
    CubixTube, initialize_front_face_solved, 
    initialize_middle_layer_solved, initialize_back_face_solved
)

def verify_cube_state():
    print("Verifying initial cube configuration...")
    cube = CubixTube()
    initialize_front_face_solved(cube)
    initialize_middle_layer_solved(cube)
    initialize_back_face_solved(cube)
    
    print("\nInitial cube configuration:")
    cube.print_cube_slices()
    
    print("\nVerification guide:")
    print("1. Check front slice (z=2) for correct piece orientations:")
    print("   - Corner pieces should have orientations 1-4 (up)")
    print("   - Straight pieces should be oriented correctly")
    print("\n2. Check middle slice (z=1) for:")
    print("   - Corner pieces with orientations 5-8 (horizontal)")
    print("   - Center pieces present")
    print("\n3. Check back slice (z=0) for:")
    print("   - Corner pieces with orientations 9-12 (down)")
    print("   - Correct color mapping (Red, Blue, Yellow)")

if __name__ == "__main__":
    verify_cube_state()
