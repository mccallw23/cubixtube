import heapq
import random

def initialize_front_face_solved(cubix_tube):
    # Correcting the configuration for the solved state's front face
    configuration = [
        [CornerPiece("Blue", 8), StraightPiece("Blue", 9), CornerPiece("Blue", 4)],
        [CornerPiece("Yellow", 12), CornerPiece("Yellow", 3), CornerPiece("Yellow", 6)],  # Corrected middle piece
        [CornerPiece("Red", 3), StraightPiece("Red", 1), CornerPiece("Red", 6)]
    ]
    for x, row in enumerate(configuration):
        for y, piece in enumerate(row):
            cubix_tube.add_piece(x, y, 2, piece)  # Add each piece to the front face

def initialize_middle_layer_solved(cubix_tube):
    # Assuming direct handling of center pieces is not required here
    configuration = [
        [StraightPiece("Blue", 2), "Blue Center", StraightPiece("Blue", 2)],
        [StraightPiece("Yellow", 2), "Center", StraightPiece("Yellow", 2)],
        [CornerPiece("Red", 8), StraightPiece("Red", 1), CornerPiece("Red", 5)]
    ]
    for x, row in enumerate(configuration):
        for y, piece in enumerate(row):
            if piece in ["Center", "Blue Center"]:  # Skipping center pieces
                continue
            cubix_tube.add_piece(x, y, 1, piece)  # Add each piece to the middle layer


def initialize_back_face_solved(cubix_tube):
    # Configuration for the solved state's back face
    configuration = [
        [CornerPiece("Blue", 7), StraightPiece("Blue", 1), CornerPiece("Blue", 5)],
        [CornerPiece("Yellow", 7), StraightPiece("Yellow", 1), CornerPiece("Yellow", 5)],
        [CornerPiece("Red", 7), StraightPiece("Red", 1), CornerPiece("Red", 9)]
    ]
    for x, row in enumerate(configuration):
        for y, piece in enumerate(row):
            cubix_tube.add_piece(x, y, 0, piece)  # Add each piece to the back face


def initialize_front_face(cubix_tube):
    # Front face configuration as provided
    configuration = [
        [CornerPiece("Red", 7), StraightPiece("Red", 1), CornerPiece("Red", 9)],
        [StraightPiece("Blue", 3), StraightPiece("Red", 1), StraightPiece("Red", 3)],
        [CornerPiece("Blue", 4), CornerPiece("Red", 6), CornerPiece("Red", 4)]
    ]
    for x, row in enumerate(configuration):
        for y, piece in enumerate(row):
            cubix_tube.add_piece(x, y, 2, piece)  # Add each piece to the front face

def initialize_middle_layer(cubix_tube):
    # Middle layer configuration as provided
    configuration = [
        [CornerPiece("Red", 12), StraightPiece("Yellow", 1), CornerPiece("Yellow", 9)],
        [StraightPiece("Yellow", 3), "Center", StraightPiece("Yellow", 2)],
        [CornerPiece("Yellow", 3), CornerPiece("Yellow", 5), CornerPiece("Yellow", 1)]
    ]
    for x, row in enumerate(configuration):
        for y, piece in enumerate(row):
            if piece == "Center":
                # Skip adding the center piece, assuming it's a special non-rotatable piece or handled differently
                continue
            # The Z index for the middle layer is 1
            cubix_tube.add_piece(x, y, 1, piece)  # Add each piece to the middle layer


def initialize_back_face(cubix_tube):
    # Back face configuration as provided
    configuration = [
        [CornerPiece("Red", 7), CornerPiece("Yellow", 9), CornerPiece("Blue", 7)],
        [StraightPiece("Blue", 3), "Blue Center", StraightPiece("Blue", 3)],
        [CornerPiece("Blue", 3), CornerPiece("Blue", 7), CornerPiece("Blue", 1)]
    ]
    for x, row in enumerate(configuration):
        for y, piece in enumerate(row):
            if piece == "Blue Center":
                # Assuming the blue center is a special non-rotatable piece
                # If "Blue Center" is merely a placeholder and does not require a distinct class,
                # you may simply skip adding it, or handle it differently based on your cube's implementation
                continue
            cubix_tube.add_piece(x, y, 0, piece)  # Add each piece to the back face

class CubixTube:

    def print_cube_slices(self):
    # Define slices based on z-coordinates
        slices = {
            "Front Slice (z=2)": 2,
            "Middle Slice (z=1)": 1,
            "Back Slice (z=0)": 0
        }

        for slice_name, z in slices.items():
            print(f"{slice_name}:")
            # Extract and print each slice
            for x in range(3):
                row_repr = []
                for y in range(3):
                    piece = self.cube[x][y][z]
                    if hasattr(piece, 'representation'):
                        row_repr.append(piece.representation())
                    else:
                        # For empty or special slots like "Center", adjust as needed
                        row_repr.append(str(piece) if piece else " ")
                print(" ".join(row_repr))
            print("\n")

    @staticmethod
    def rotate_face_clockwise(face):
        # This method assumes 'face' is a list of lists.
        # Transpose and reverse each row to rotate clockwise.
        return [list(row) for row in zip(*face[::-1])]
    
    @staticmethod
    def rotate_face_forward_clockwise(face):
        """
        Rotates the left face of the cube forward in a clockwise direction.
        This rotation is equivalent to turning the left face towards us, rotating around the X-axis.
        """
        # Assuming 'face' is a 3x3 section of the cube where each element is accessed by [y][z].
        # The rotation involves moving elements in the Y-Z plane.
        new_face = [[None for _ in range(3)] for _ in range(3)]
        for y in range(3):
            for z in range(3):
                # The element at [y][z] moves to [z][2-y], rotating the face forward clockwise.
                new_face[z][2 - y] = face[y][z]
        return new_face
    
    
    def rotate_left_face_positionally(self):
        # Correct extraction of the left face positions
        left_face_positions = [[self.cube[x][0][z] for z in range(3)] for x in range(3)]

        # Correctly apply rotation to these positions
        rotated_positions = [[None for _ in range(3)] for _ in range(3)]
        for x in range(3):
            for z in range(3):
                # Rotate clockwise: The piece at [x][0][z] moves to [z][0][2-x]
                rotated_positions[z][2-x] = left_face_positions[x][z]

        # Update the cube with the rotated positions for the left face
        for x in range(3):
            for z in range(3):
                self.cube[x][0][z] = rotated_positions[x][z]

    def rotate_right_face_positionally(self):
        # Extract the positions of pieces on the right face
        right_face_positions = [[self.cube[x][2][z] for z in range(3)] for x in range(3)]
        
        # Apply rotation to these positions
        rotated_positions = [[None for _ in range(3)] for _ in range(3)]
        for x in range(3):
            for z in range(3):
                # Rotate clockwise: The piece at [x][z] moves to [z][2-x] on the right face
                rotated_positions[z][2-x] = right_face_positions[x][z]
        
        # Update the cube with the rotated positions for the right face
        for x in range(3):
            for z in range(3):
                self.cube[x][2][z] = rotated_positions[x][z]

    def rotate_top_face_positionally(self):
        # Extract the positions of pieces on the top face (X=0)
        top_face_positions = [[self.cube[0][y][z] for z in range(3)] for y in range(3)]
        
        # Apply rotation to these positions
        rotated_positions = [[None for _ in range(3)] for _ in range(3)]
        for y in range(3):
            for z in range(3):
                # Rotate clockwise: The piece at [y][z] moves to [z][2-y]
                rotated_positions[z][2-y] = top_face_positions[y][z]
        
        # Update the cube with the rotated positions for the top face
        for y in range(3):
            for z in range(3):
                self.cube[0][y][z] = rotated_positions[y][z]


    def rotate_MRL_positionally(self):
        # Extract the positions of pieces on the middle layer (Y=1)
        middle_layer_positions = [[self.cube[x][1][z] for z in range(3)] for x in range(3)]
        
        # Apply rotation to these positions
        rotated_positions = [[None for _ in range(3)] for _ in range(3)]
        for x in range(3):
            for z in range(3):
                # Rotate clockwise: The piece at [x][z] moves to [z][2-x]
                rotated_positions[z][2-x] = middle_layer_positions[x][z]

        # Update the cube with the rotated positions for the middle layer
        for x in range(3):
            for z in range(3):
                self.cube[x][1][z] = rotated_positions[x][z]

            
    def rotate_MUD_positionally(self):
        # Extract the positions of pieces on the middle layer (X=1)
        middle_layer_positions = [[self.cube[1][y][z] for z in range(3)] for y in range(3)]
        
        # Apply rotation to these positions
        rotated_positions = [[None for _ in range(3)] for _ in range(3)]
        for y in range(3):
            for z in range(3):
                # Rotate counter-clockwise: The piece at [y][z] moves to [2-z][y]
                rotated_positions[2-z][y] = middle_layer_positions[y][z]
        
        # Update the cube with the rotated positions for the middle layer
        for y in range(3):
            for z in range(3):
                self.cube[1][y][z] = rotated_positions[y][z]


    def rotate_bottom_face_positionally(self):
        # Extract the positions of pieces on the bottom face (X=2)
        bottom_face_positions = [[self.cube[2][y][z] for z in range(3)] for y in range(3)]
        
        # Apply rotation to these positions
        rotated_positions = [[None for _ in range(3)] for _ in range(3)]
        for y in range(3):
            for z in range(3):
                # Rotate clockwise: The piece at [y][z] moves to [z][2-y], similar to the top face but on the bottom layer
                rotated_positions[z][2-y] = bottom_face_positions[y][z]
        
        # Update the cube with the rotated positions for the bottom face
        for y in range(3):
            for z in range(3):
                self.cube[2][y][z] = rotated_positions[y][z]

    
    def __init__(self):
        # Initialize a 3x3x3 cube filled with None
        self.cube = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]

        # Optionally, set the central piece and blue centerpiece as non-functional
        self.cube[1][1][1] = "Center"  # Central non-functional piece
        # Assuming the blue centerpiece is at a specific location, e.g., front center
        self.cube[1][1][0] = "Blue Center"  # Blue centerpiece

    def add_piece(self, x, y, z, piece):
        if self.cube[x][y][z] is None:  # Ensure the slot is empty and valid
            self.cube[x][y][z] = piece
        else:
            print("Slot already occupied or invalid:  value of slot is ", self.cube[x][y][z])

    def get_piece(self, x, y, z):
        return self.cube[x][y][z]


    def rotate_left_face(self):
        # Temporary storage for the left face
        temp_face = [[None for _ in range(3)] for _ in range(3)]
        
        # Copying the current left face into temporary storage
        for y in range(3):
            for z in range(3):
                temp_face[y][z] = self.cube[0][y][z]
        
        # Rotating the left face clockwise
        for y in range(3):
            for z in range(3):
                self.cube[0][z][2 - y] = temp_face[y][z]

    def print_cube_slices(self):
        # Define slices based on z-coordinates
        slices = {
            "Front Slice (z=2)": 2,
            "Middle Slice (z=1)": 1,
            "Back Slice (z=0)": 0
        }
 
        for slice_name, z in slices.items():
            print(f"{slice_name}:")
            # Extract and print each slice
            for x in range(3):
                row_repr = []
                for y in range(3):
                    piece = self.cube[x][y][z]
                    if hasattr(piece, 'representation'):
                        row_repr.append(piece.representation())
                    else:
                        # For empty or special slots like "Center", adjust as needed
                        row_repr.append(str(piece) if piece else " ")
                print(" ".join(row_repr))
            print("\n")

    def Z_update_piece_orientation(self, piece):
        # Orientation update maps
        straight_piece_orientation_map = {
            1: 3,
            3: 1,
            2: 2,
        }

        corner_piece_orientation_map = {
            1: 3, 2: 7, 3: 11, 4: 8,
            5: 2, 6: 4, 7: 10, 8: 12,
            9: 1, 10: 5, 11: 9, 12: 6,
        }
        if isinstance(piece, StraightPiece):
            piece.orientation = straight_piece_orientation_map.get(piece.orientation, piece.orientation)
        elif isinstance(piece, CornerPiece):
            piece.orientation = corner_piece_orientation_map.get(piece.orientation, piece.orientation)

    def X_update_piece_orientation(self, piece):
        # Orientation update maps for the U_Prime move
        straight_piece_orientation_map_U = {
            1: 2,  # Horizontal becomes into the page
            2: 1,  # Into the page becomes horizontal
            3: 3   # Vertical stays vertical
        }

        corner_piece_orientation_map_U = {
            1: 2, 2: 3, 3: 4, 4: 1,
            5: 7, 7: 8, 8: 6, 6: 5,
            9: 10, 10: 11, 11: 12, 12: 9
        }

        if isinstance(piece, StraightPiece):
            piece.orientation = straight_piece_orientation_map_U.get(piece.orientation, piece.orientation)
        elif isinstance(piece, CornerPiece):
            piece.orientation = corner_piece_orientation_map_U.get(piece.orientation, piece.orientation)


    def Y_update_piece_orientation(self, piece):
        # Orientation update maps for the L move
        straight_piece_orientation_map_L = {
            1: 1,  # Horizontal stays horizontal
            2: 3,  # Into the page becomes vertical
            3: 2,  # Vertical becomes into the page
        }

        corner_piece_orientation_map_L = {
            1: 5,
            2: 10,
            3: 7,
            4: 2,
            5: 9,
            6: 1,
            7: 11,
            8: 3,
            9: 6,
            10: 12,
            11: 8,
            12: 4,
        }

        if isinstance(piece, StraightPiece):
            piece.orientation = straight_piece_orientation_map_L.get(piece.orientation, piece.orientation)
        elif isinstance(piece, CornerPiece):
            piece.orientation = corner_piece_orientation_map_L.get(piece.orientation, piece.orientation)


    # def R(self):
    #     self.R_Prime()
    #     self.R_Prime()
    #     self.R_Prime()

    # def R2(self):
        # self.R_Prime()
        # self.R_Prime()

 # right face
    def R_Prime(self):
        # Rotate the right face positionally
        self.rotate_right_face_positionally()
        
        # Update the orientations for pieces on the right face
        for x in range(3):
            for z in range(3):
                piece = self.cube[x][2][z]
                if piece:
                    # Assuming Y_update_piece_orientation applies correct orientation updates for the right face as well
                    self.Y_update_piece_orientation(piece)
    
    def R(self):
        self.R_Prime()
        self.R_Prime()
        self.R_Prime()

    def R2(self):
        self.R_Prime()
        self.R_Prime()

    def M_RL(self):
        self.rotate_MRL_positionally()

        for x in range(3):
            for z in range(3):
                piece = self.cube[x][1][z]
                if piece:
                    # Assuming Y_update_piece_orientation applies correct orientation updates for the right face as well
                    self.Y_update_piece_orientation(piece)

    def M_RL_2(self):
        self.M_RL()
        self.M_RL()

    def M_RL_Prime(self):
        self.M_RL()
        self.M_RL()
        self.M_RL()

    def L(self):

        # Correctly rotate the left face
        self.rotate_left_face_positionally()

        # Update orientations for pieces on the left face
        for x in range(3):
            for z in range(3):
                piece = self.cube[x][0][z]
                if piece:
                    self.Y_update_piece_orientation(piece)

    def L_Prime(self):
        self.L()
        self.L()
        self.L()
# front face
        
    def L2(self):
        self.L()
        self.L()

        
    def F(self):

        # Extract the front face
        front_face = [[self.get_piece(x, y, 2) for y in range(3)] for x in range(3)]

        # Rotate the front face clockwise
        rotated_face = CubixTube.rotate_face_clockwise(front_face)

        # Apply the rotated face back to the cube
        for x in range(3):
            for y in range(3):
                self.cube[x][y][2] = rotated_face[x][y]

        # Update piece orientations for the front face
        for x in range(3):
            for y in range(3):
                piece = self.get_piece(x, y, 2)
                if piece not in ["Center", "Blue Center"]:
                    self.Z_update_piece_orientation(piece)


    def F_Prime(self):
        self.F()
        self.F()
        self.F()

    def F2(self):

        self.F()
        self.F()


# by convention, the middle layer will rotate in the same direction as:
# the front face, the top face, and the right face.  In this case we're dealing with the front face
    def M_FB(self):
        middle_face = [[self.cube[x][y][1] for y in range(3)] for x in range(3)]
        rotated_middle_face = CubixTube.rotate_face_clockwise(middle_face)

        for x, new_row in enumerate(rotated_middle_face):
            for y, new_piece in enumerate(new_row):
                self.cube[x][y][1] = new_piece  # Use x, y, 0 instead of x, 0, y

        for x in range(3):
            for y in range(3):
                piece = self.get_piece(x, y, 1)
                if piece not in ["Center", "Blue Center"]:
                    self.Z_update_piece_orientation(piece)

    def M_FB_Prime(self):
        self.M_FB()
        self.M_FB()
        self.M_FB()

    def M_FB_2(self):
        self.M_FB()
        self.M_FB()

# back face
    def B_Prime(self):

        # Extract the back face (z=0 for all pieces in the slice)
        back_face = [[self.cube[x][y][0] for y in range(3)] for x in range(3)]

        # Rotate the back face counter-clockwise
        rotated_face = CubixTube.rotate_face_clockwise(back_face)

        # Apply the rotated face back to the cube
        for x, new_row in enumerate(rotated_face):
            for y, new_piece in enumerate(new_row):
                self.cube[x][y][0] = new_piece  # Use x, y, 0 instead of x, 0, y

        for x in range(3):
            for y in range(3):
                piece = self.get_piece(x, y, 0)
                if piece not in ["Center", "Blue Center"]:
                    self.Z_update_piece_orientation(piece)

    def B(self):
        self.B_Prime()
        self.B_Prime()
        self.B_Prime()

    def B2(self):
        self.B_Prime()
        self.B_Prime()

# top face
    def U_Prime(self):
        self.rotate_top_face_positionally()
        # Orientation updates for the top face
        for y in range(3):
            for z in range(3):
                piece = self.cube[0][y][z]
                if piece:
                    # Apply orientation updates for the top face
                    self.X_update_piece_orientation(piece)
   
    def U(self):
        self.U_Prime()
        self.U_Prime()
        self.U_Prime()

    def U2(self):
        self.U_Prime()
        self.U_Prime()

    # middle layer
    def M_UD_Prime(self):
        self.rotate_MUD_positionally()
        # Apply orientation updates for the middle layer
        for y in range(3):
            for z in range(3):
                piece = self.cube[1][y][z]
                if piece:
                    self.X_update_piece_orientation(piece)


    def M_UD(self):
        self.M_UD_Prime()
        self.M_UD_Prime()
        self.M_UD_Prime()

    def M_UD_2(self):
        self.M_UD_Prime()
        self.M_UD_Prime()

    # bottom face
    def D(self):
        self.rotate_bottom_face_positionally()
        # Orientation updates for the bottom face
        for y in range(3):
            for z in range(3):
                piece = self.cube[2][y][z]
                if piece:
                    # Apply orientation updates for the bottom face
                    self.X_update_piece_orientation(piece)

    def D_Prime(self):
        self.D()
        self.D()
        self.D()

    def D2(self):
        self.D()
        self.D()


class Piece:
    def __init__(self, color, orientation):
        self.color = color
        self.orientation = orientation

    def __repr__(self):
        return f"{self.color}-{self.orientation}"
    
    def representation(self):
    # Map color names to circle emojis
        color_emoji_map = {
            "Red": "🔴",
            "Yellow": "🟡",
            "Blue": "🔵"
        }
    
        # Get the emoji based on the piece's color
        color_emoji = color_emoji_map.get(self.color, "")
        
        # Return a string that includes the piece type, emoji based on color, and orientation
        # return f"{color_emoji}"
        return f"{self.__class__.__name__}({color_emoji}, {self.orientation})"

class CornerPiece(Piece):
    def __init__(self, color, orientation):
        super().__init__(color, orientation)
        self.piece_type = "corner"
        # No need for max_orientations if we're directly setting the orientation

class StraightPiece(Piece):
    def __init__(self, color, orientation):
        super().__init__(color, orientation)
        self.piece_type = "straight"

# code to serialize the cube state
def serialize_cube_state(cube):
    """
    Serialize the cube state to include type, color, and orientation of each piece.
    """
    serialized_state = []
    for layer in cube:
        for row in layer:
            for piece in row:
                if piece is None:
                    serialized_state.append('None')
                elif isinstance(piece, str):  # Handling "Center" pieces
                    serialized_state.append(piece)
                else:
                    # Include piece_type in serialization
                    serialized_state.append(f"{piece.__class__.__name__}-{piece.color}-{piece.orientation}")
    return '|'.join(serialized_state)


def simplified_to_cubix_tube(serialized_state):
    # Split the serialized state back into individual piece representations
    pieces_info = serialized_state.split('|')
    
    # Create a new CubixTube instance
    # this is gonna be an issue if the blue center is around...
    new_cube = CubixTube()
    
    # Initialize counters for iterating through pieces_info
    piece_counter = 0
    
    # Iterate over layers, rows, and pieces according to the cube structure
    for layer_idx in range(3):  # For each layer in the cube
        for row_idx in range(3):  # For each row in a layer
            for piece_idx in range(3):  # For each piece in a row
                piece_info = pieces_info[piece_counter]
                piece_counter += 1
                
                if piece_info == 'None':
                    continue  # Skip None values, the slot is already initialized as None
                
                elif piece_info == 'Center' or piece_info == 'Blue Center':
                    # Directly assign special center pieces
                    new_cube.cube[layer_idx][row_idx][piece_idx] = piece_info
                
                else:
                    # Parse the piece_info to get type, color, and orientation
                    piece_type, color, orientation = piece_info.split('-')
                    orientation = int(orientation)  # Convert orientation string to int
                    
                    if piece_type == "CornerPiece":
                        piece = CornerPiece(color, orientation)
                    elif piece_type == "StraightPiece":
                        piece = StraightPiece(color, orientation)
                    else:
                        raise ValueError(f"Unknown piece type encountered: {piece_type}")
                    
                    # Place the piece object in the correct position within the cube
                    new_cube.cube[layer_idx][row_idx][piece_idx] = piece
    
    return new_cube


def deserialize_cube_state(serialized_state):
    pieces = serialized_state.split('|')
    cube = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]
    
    piece_type_map = {
    'CornerPiece': CornerPiece,
    'StraightPiece': StraightPiece,
}

    idx = 0  # Index to iterate through the flattened cube structure
    for x in range(3):
        for y in range(3):
            for z in range(3):
                piece_data = pieces[idx]
                if piece_data == 'None':
                    cube[x][y][z] = None
                elif piece_data in ['Center', 'Blue Center']:
                    cube[x][y][z] = piece_data  # Special center pieces
                else:
                    piece_type, color, orientation = piece_data.split('-')
                    orientation = int(orientation)
                    piece_class = piece_type_map[piece_type]
                    cube[x][y][z] = piece_class(color, orientation)
                idx += 1

    return cube



def calculate_heuristic(cube_state, solved_state):
    score = 0
    
    for x in range(3):
        for y in range(3):
            for z in range(3):
                current_piece = cube_state[x][y][z]
                solved_piece = solved_state[x][y][z]
                
                # Skip center pieces and None values
                if isinstance(current_piece, str) or isinstance(solved_piece, str) or current_piece is None or solved_piece is None:
                    continue
                
                is_piece_type_correct = isinstance(current_piece, type(solved_piece))
                is_color_correct = current_piece.color == solved_piece.color if current_piece and solved_piece else False
                is_orientation_correct = current_piece.orientation == solved_piece.orientation if current_piece and solved_piece else False
                
                if is_piece_type_correct:
                    if is_color_correct:
                        if is_orientation_correct:
                            # Correctly placed and oriented
                            score += 0 if isinstance(current_piece, CornerPiece) else 0
                        else:
                            # Correct piece type and color but wrong orientation
                            score += 3 if isinstance(current_piece, CornerPiece) else 2
                    else:
                        # Correct piece type but color mismatch (should be rare due to piece type check)
                        score += 5
                else:
                    # Completely misplaced or mismatched piece types
                    score += 7

                    # we need to assign a value to every possible state we could find the piece in such that the heuristic is 0 when the cube is solved
                    # we can't just assign a value of 1 to every misplaced piece, because then the heuristic would be the number of misplaced pieces.

                    # proposed heuristic:
                    # 0 for correct piece type, color, and orientation
                    # 2 for correct piece type and color but wrong orientation
                    # 5 for correct piece type but color mismatch
                    # 7 for completely misplaced or mismatched piece types
                    # we should distinguish for when the piece is a corner piece or a straight piece
                    # we should also consider the distance of the piece from its correct position
                    # we should also consider the orientation of the piece
                    # we should also consider the color of the piece
                    # we should also consider the type of the piece
                    # we should also consider the position of the piece
                    # proposed heuristic:
                    # 0 for correct piece type, color, and orientation if piece is corner
                    # 0 for correct piece type, color, and orientation if piece is straight
                    # 3 for correct piece type and color but wrong orientation if piece is corner
                    # 2 for correct piece type and color but wrong orientation if piece is straight
                    # 5 for correct piece type but color mismatch
                    # 7 for completely misplaced or mismatched piece types
                

    return score



def apply_random_moves(cube, num_moves):
    serialized_states = []
    applied_moves = []
    for _ in range(num_moves):
        move = random.choice(list(move_pairs.keys()))
        getattr(cube, move)()
        applied_moves.append(move)
        serialized_states.append(serialize_cube_state(cube.cube))
    return serialized_states, applied_moves


def revert_random_moves(cube, applied_moves):
    # use move_pairs to get the reverse move for each applied move
    for move in reversed(applied_moves):
        reverse_move = move_pairs[move][1]
        getattr(cube, reverse_move)()


def a_star_search(start_cube, goal_state_serialized, goal_cubix_tube):
    """
    Perform A* search to find the shortest path to solve the Rubik's cube.

    Args:
        start_cube: An instance of CubixTube representing the starting state.
        goal_state_serialized: A serialized string representing the goal state.

    Returns:
        A list of moves representing the path from the start state to the goal state.
    """
    # Initialize the priority queue with the start state
    open_set = [(0, 0, serialize_cube_state(start_cube.cube))]
    heapq.heapify(open_set)
    min_heuristic = 50
    
    # Initialize score tracking
    g_score = {serialize_cube_state(start_cube.cube): 0}
    came_from = {}  # Track the path
    closed_set = set()  # Track visited states

    # Define available moves
    moves = ['L', 'R', 'F', 'B', 'U', 'D', 'M_RL', 'M_FB', 'M_UD']

    while open_set:
        _, current_g, current_serialized = heapq.heappop(open_set)

        # Goal check
        if current_serialized == goal_state_serialized:
            return reconstruct_path(came_from, current_serialized)

        closed_set.add(current_serialized)

        # Temporarily deserialize the cube for move exploration
        temp_cube = simplified_to_cubix_tube(current_serialized)

        print(f"Deserialized cube: {serialize_cube_state(temp_cube.cube)}")


        # Explore each move from the current state
        
        for move_name in moves:
            new_serialized = apply_move(temp_cube, move_name)

            if new_serialized in closed_set:
                print("found duplicate in set")
                continue  # Skip already visited states

            tentative_g_score = current_g + 1

            # Update path and score if a better path is found
            if new_serialized not in g_score or tentative_g_score < g_score[new_serialized]:

                new_cubix_tube = simplified_to_cubix_tube(new_serialized)
                came_from[new_serialized] = current_serialized
                g_score[new_serialized] = tentative_g_score
                f_score = tentative_g_score + calculate_heuristic(new_cubix_tube.cube, goal_cubix_tube.cube)

                if f_score < min_heuristic:
                    min_heuristic = f_score
                    new_cubix_tube.print_cube_slices()
                    goal_cubix_tube.print_cube_slices()
                    print(min_heuristic)
               
                heapq.heappush(open_set, (f_score, tentative_g_score, new_serialized))
                

        print("Min Heuristic: ", min_heuristic, "Closed Set Size: ", len(closed_set))
        print(reconstruct_path(came_from, current_serialized))


    return None  # Return None if no path to goal state is found


def a_star_search_alpha(start_cube, goal_state_serialized, goal_cubix_tube):

    """
    Perform A* search to find the shortest path to solve the Rubik's cube.

    Args:
        start_cube: An instance of CubixTube representing the starting state.
        goal_state_serialized: A serialized string representing the goal state.

    Returns:
        A list of moves representing the path from the start state to the goal state.
    """
    # Initialize the priority queue with the start state
    print("Starting Phase Alpha...")
    open_set = [(0, 0, serialize_cube_state(start_cube.cube))]
    heapq.heapify(open_set)
    min_heuristic = 100

    # Initialize score tracking
    g_score = {serialize_cube_state(start_cube.cube): 0}
    came_from = {}  # Track the path
    closed_set = set()  # Track visited states

    # Define available moves
    moves = ['L', 'L_Prime', 'R', 'R_Prime', 'F', 'F_Prime', 'B', 'B_Prime', 'U', 'U_Prime', 'D', 'D_Prime', 'L2', 'R2', 'F2', 'B2', 'U2', 'D2']

    while open_set:
        _, current_g, current_serialized = heapq.heappop(open_set)

        # Goal check
        if current_serialized == goal_state_serialized:
            return reconstruct_path(came_from, current_serialized)

        closed_set.add(current_serialized)

        # Temporarily deserialize the cube for move exploration
        # temp_cube_simplified = deserialize_cube_state(current_serialized)
        # this might double execution time and possibly memory usage...
        temp_cube = simplified_to_cubix_tube(current_serialized)

        # Explore each move from the current state

        for move_name in moves:
            new_serialized = apply_move(temp_cube, move_name)

            if new_serialized in closed_set:
                continue  # Skip already visited states

            tentative_g_score = current_g + 1  # Cost of each move is 1

            # Update path and score if a better path is found
            if new_serialized not in g_score or tentative_g_score < g_score[new_serialized]:

                new_cubix_tube = simplified_to_cubix_tube(new_serialized)
                came_from[new_serialized] = current_serialized
                g_score[new_serialized] = tentative_g_score
                f_score = tentative_g_score + calculate_heuristic_alpha(new_cubix_tube.cube, goal_cubix_tube.cube, orientation_matrix)

                if f_score < min_heuristic:
                    min_heuristic = f_score
                    new_cubix_tube.print_cube_slices()
                    goal_cubix_tube.print_cube_slices()
                heapq.heappush(open_set, (f_score, tentative_g_score, new_serialized))

        if random.randint(1, 1000) == 1:
            print("Min Heuristic: ", min_heuristic, "Closed Set Size: ", len(closed_set))
           

    return None  # Return None if no path to goal state is found


orientation_matrix = {1: [2, 3, 4, 5, 6, 9],
 2: [1, 3, 4, 5, 7, 10],
 3: [1, 2, 4, 7, 8, 11],
 4: [1, 2, 3, 6, 8, 12],
 5: [1, 2, 6, 7, 9, 10],
 6: [1, 4, 5, 8, 9, 12],
 7: [2, 3, 5, 8, 10, 11],
 8: [3, 4, 6, 7, 11, 12],
 9: [1, 5, 6, 10, 11, 12],
 10: [2, 5, 7, 9, 11, 12],
 11: [3, 7, 8, 9, 10, 12],
 12: [4, 6, 8, 9, 10, 11]}


def calculate_heuristic_alpha(cube_state, solved_state, orientation_matrix):
    score = 0
    
    # Focus only on the X=2 layer for the red face
    x = 2
    for y in range(3):
        for z in range(3):
            current_piece = cube_state[x][y][z]
            solved_piece = solved_state[x][y][z]

            # Skip center pieces and None values
            if isinstance(current_piece, str) or isinstance(solved_piece, str) or current_piece is None or solved_piece is None:
                continue
            
            # Check for correct piece type and color
            is_piece_type_correct = isinstance(current_piece, type(solved_piece))
            is_color_correct = current_piece.color == "Red" if current_piece else False  # Focusing on red color
            is_orientation_correct = current_piece.orientation == solved_piece.orientation if current_piece and solved_piece and is_piece_type_correct else False
            
            # Adjust scoring based on piece status
            if is_piece_type_correct and is_color_correct:
                if is_orientation_correct:
                    # Correctly placed and oriented
                    score -= 0  # Ideal case, no additional score
                else:
                    # Check orientation adjustment penalty for corners
                    if isinstance(current_piece, CornerPiece):
                        if current_piece.orientation in orientation_matrix[current_piece.orientation]:
                            # One move away from correct orientation
                            score += 3
                        else:
                            # Two moves away from correct orientation
                            score += 4
                    elif isinstance(current_piece, StraightPiece):
                        # Straight pieces have a fixed penalty for wrong orientation
                        score += 1
            elif is_color_correct and not is_piece_type_correct:
                # Correct color but wrong type
                score += 11
            else:
                # Wrong color or completely misplaced
                score += 19

    return score



def reconstruct_path(came_from, current_serialized):
    # Reconstruct the path from start to goal by following came_from links
    path = [current_serialized]
    while current_serialized in came_from:
        current_serialized = came_from[current_serialized]
        path.append(current_serialized)
    path.reverse()
    # now we need to check what moves were made to get this path and return that.  The way to do this is to check all moves and see which move was made to get to the next state in the path

    possible_move_names = ['L', 'L_Prime', 'R', 'R_Prime', 'F', 'F_Prime', 'B', 'B_Prime', 'U', 'U_Prime', 'D', 'D_Prime', 'L2', 'R2', 'F2', 'B2', 'U2', 'D2']

    move_path = []
    for i in range(len(path) - 1):
        current_state = deserialize_cube_state(path[i])
        next_state = deserialize_cube_state(path[i + 1])
        for move_name in possible_move_names:
            temp_cube = CubixTube()
            temp_cube.cube = current_state
            getattr(temp_cube, move_name)()
            if cubes_are_equal(temp_cube.cube, next_state):
                move_path.append(move_name)
                break
    
    return move_path

# code to return a hashed cube state for efficiency
def hash_cube_state(cube):

    serialized_state = serialize_cube_state(cube)
    return hash(serialized_state)

def cubes_are_equal(cube1, cube2):
    for x in range(3):
        for y in range(3):
            for z in range(3):
                piece1 = cube1[x][y][z]
                piece2 = cube2[x][y][z]
                
                if type(piece1) != type(piece2):
                    return False
                elif piece1 is None and piece2 is None:
                    continue
                elif isinstance(piece1, str) or isinstance(piece2, str):
                    if piece1 != piece2:
                        return False
                elif piece1.color != piece2.color or piece1.orientation != piece2.orientation:
                    return False
    return True

move_pairs = {
    'L': ('L', 'L_Prime'),
    'L_Prime': ('L_Prime', 'L'),
    'L2': ('L2', 'L2'),  # L2 is its own inverse
    'R': ('R', 'R_Prime'),
    'R_Prime': ('R_Prime', 'R'),
    'R2': ('R2', 'R2'),  # R2 is its own inverse
    'F': ('F', 'F_Prime'),
    'F_Prime': ('F_Prime', 'F'),
    'F2': ('F2', 'F2'),  # F2 is its own inverse
    'B': ('B', 'B_Prime'),
    'B_Prime': ('B_Prime', 'B'),
    'B2': ('B2', 'B2'),  # B2 is its own inverse
    'U': ('U', 'U_Prime'),
    'U_Prime': ('U_Prime', 'U'),
    'U2': ('U2', 'U2'),  # U2 is its own inverse
    'D': ('D', 'D_Prime'),
    'D_Prime': ('D_Prime', 'D'),
    'D2': ('D2', 'D2'),  # D2 is its own inverse
    'M_RL': ('M_RL', 'M_RL_Prime'),
    'M_RL_Prime': ('M_RL_Prime', 'M_RL'),
    'M_RL_2': ('M_RL_2', 'M_RL_2'),
    'M_FB': ('M_FB', 'M_FB_Prime'),
    'M_FB_Prime': ('M_FB_Prime', 'M_FB'),
    'M_FB_2': ('M_FB_2', 'M_FB_2'),
    'M_UD': ('M_UD', 'M_UD_Prime'),
    'M_UD_Prime': ('M_UD_Prime', 'M_UD'),
    'M_UD_2': ('M_UD_2', 'M_UD_2'),
    
}

# returns a serialized state after applying a move:
def apply_move(cube, move_name):
    """
    Apply a move to the cube and immediately apply its inverse to revert the state.
    This is used within the A* search to explore moves without altering the cube's state.
    """
    move, inverse_move = move_pairs[move_name]
    # Apply the move
    getattr(cube, move)()
    # Serialize state for A* exploration
    serialized_state = serialize_cube_state(cube.cube)
    # Immediately apply the inverse to revert
    getattr(cube, inverse_move)()
    return serialized_state

def apply_moves_random(cube, moves, num_moves):
    """
    Apply a random sequence of moves to the cube.

    Args:
        cube: An instance of CubixTube representing the cube to scramble.
        moves: A list of available moves to choose from.
        num_moves: The number of random moves to apply.
    """

    #
    for _ in range(num_moves):
        move_name = random.choice(moves)
        getattr(cube, move_name)()


def is_goal_state(current_state_serialized, goal_state_serialized):
    current_state = deserialize_cube_state(current_state_serialized)
    goal_state = deserialize_cube_state(goal_state_serialized)
    return cubes_are_equal(current_state, goal_state)

def test_move_inverse_pairs(cube, move_pairs):
    """
    Test each move and its inverse to ensure they correctly revert the cube to its original state.
    
    Args:
        cube: An instance of CubixTube representing the cube to test on.
        move_pairs: A dictionary where keys are move names and values are tuples of (move, inverse_move) functions.
    """
    original_serialized_state = serialize_cube_state(cube.cube)
    
    for move_name, (move, inverse_move) in move_pairs.items():
        # Apply the move
        getattr(cube, move)()
        # Apply the inverse move
        getattr(cube, inverse_move)()
        # Serialize the state after applying the move and its inverse
        new_serialized_state = serialize_cube_state(cube.cube)
        
        # Check if the cube has returned to its original state
        if original_serialized_state != new_serialized_state:
            print(f"Test failed for {move_name}. Cube did not return to its original state.")
        else:
            print(f"Test passed for {move_name}. Cube returned to its original state.")


cubix_tube_solved = CubixTube()
initialize_front_face_solved(cubix_tube_solved)
initialize_middle_layer_solved(cubix_tube_solved)
initialize_back_face_solved(cubix_tube_solved)

cubix_tube = CubixTube()
initialize_front_face(cubix_tube)
initialize_middle_layer(cubix_tube)
initialize_back_face(cubix_tube)

# test_move_inverse_pairs(cubix_tube, move_pairs)

#path = a_star_search_alpha(cubix_tube, serialize_cube_state(cubix_tube_solved.cube), cubix_tube_solved)
#path = a_star_search(cubix_tube, serialize_cube_state(cubix_tube_solved.cube), cubix_tube_solved)
# let's try the other way:
path = a_star_search(cubix_tube_solved, serialize_cube_state(cubix_tube.cube), cubix_tube)
print(path)


# 1-4 up
# 5-8 horizontal
# 9-12 down

# 1 is up and left
# 2 up and forward
# 3 up and right
# 4 up and backwards

# 5 forward and left
# 6 backward and left
# 7 forward and right
# 8 backward and right

# 9-12 down and...
# 9. Left
# 10. forward
# 11. right
# 12. backwards


# research notes:
# Iterative deepening prevents long paths and unecessary search
# Big idea:  Checkpoints.
# Korf's algorithm uses a database.  I'm hoping to use randomness instead.

# commutative moves can be pruned.

# Examples of commutative moves:
# R and L
# F and B
# U and D

# neutral elements can be pruned.
# R and R'
# F and F'
# U and U'
# L and L'
# B and B'
# D and D'


#TODO:
# Implement Checkpoint Alpha: Red pieces.


# import random



# def a_star_search_with_randomness(start_cube, goal_state_serialized, goal_cubix_tube):
#     """
#     Perform A* search to find the shortest path to solve the Rubik's cube, with randomness injection to escape local minima.
#     """
#     open_set = [(0, 0, serialize_cube_state(start_cube))]
#     heapq.heapify(open_set)

#     # Maps for score tracking and path reconstruction
#     g_score = {serialize_cube_state(start_cube): 0}
#     came_from = {}
#     closed_set = set()

#     # Introduce randomness when progress stalls
#     last_improvement_iteration = 0
#     min_heuristic = float('inf')
#     improvement_threshold = 20000  # Trigger random moves after 20,000 iterations without improvement

#     # Moves
#     moves = ['L', 'L_Prime', 'R', 'R_Prime', 'F', 'F_Prime', 'B', 'B_Prime', 'U', 'U_Prime', 'D', 'D_Prime']

#     while open_set:
#         _, current_g, current_serialized = heapq.heappop(open_set)
#         current_cube = simplified_to_cubix_tube(current_serialized)

#         # Goal check
#         if current_serialized == goal_state_serialized:
#             return reconstruct_path(came_from, current_serialized)

#         closed_set.add(current_serialized)

#         # Randomness injection if stuck
#         if len(closed_set) - last_improvement_iteration >= improvement_threshold:
#             random_move_num = random.randint(1, 10)
#             applied_moves, serialized_cube_state = apply_random_moves(current_cube, random_move_num)
#             new_serialized_after_random = serialize_cube_state(current_cube)
#             if new_serialized_after_random not in closed_set:
#                 # Only proceed if the random state is new
#                 revert_random_moves(current_cube, applied_moves)  # Revert to the original state to continue with regular A* steps
#                 last_improvement_iteration = len(closed_set)  # Reset the counter as we've attempted to escape the local minimum

#         for move_name in moves:
#             # Regular A* expansion with each move
#             new_serialized = apply_move(current_cube, move_name)

#             if new_serialized in closed_set:
#                 continue  # Skip already visited states

#             tentative_g_score = current_g + 1
#             if new_serialized not in g_score or tentative_g_score < g_score[new_serialized]:
#                 # New state or better path found
#                 came_from[new_serialized] = current_serialized
#                 g_score[new_serialized] = tentative_g_score
#                 f_score = tentative_g_score + calculate_heuristic(current_cube, goal_cubix_tube)

#                 if f_score < min_heuristic:
#                     min_heuristic = f_score
#                     last_improvement_iteration = len(closed_set)  # Update last improvement

#                 heapq.heappush(open_set, (f_score, tentative_g_score, new_serialized))

#     return None  # No solution found, or complete the function with appropriate return



