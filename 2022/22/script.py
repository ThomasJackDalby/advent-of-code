CUBE_ORDER = 2
NUM_TILES_FACE = CUBE_ORDER * CUBE_ORDER
FACE_POSITIONS = [
    [0, 1, 2, 3, 4, 5],
    [1, 2, 0, 4, 5, 3],
    [2, 0, 1, 5, 3, 4],
    [3, 5, 4, 0, 2, 1],
    [4, 3, 5, 1, 0, 2],
    [5, 4, 3, 2, 1, 0]
]
FACE_ROTATIONS = [
    [0, 0, 0, 0, 0, 0],
    [3, 2, 3, 3, 0, 1],
    [1, 1, 2, 3, 1, 0],
    [3, 3, 1, 1, 3, 1],
    [2, 0, 1, 0, 2, 3],
    [2, 3, 2, 2, 1, 2]
]

def get_tile_index(f, x, y):
    """Get the index for a tile in the cube state."""
    return f * NUM_TILES_FACE + get_face_index(x, y)

def get_face_index(x, y):
    """Get the index for a tile within a face."""
    return y * CUBE_ORDER + x

def rotate_face(face, amount):
    if amount == 0:
        return face
    elif amount < 0:
        delta = 1
        get_rotated_face_index = lambda x, y: get_face_index(y, CUBE_ORDER - x - 1)
    else:
        delta = -1
        get_rotated_face_index = lambda x, y: get_face_index(CUBE_ORDER - y - 1, x)

    next_face = [0] * NUM_TILES_FACE
    for y in range(CUBE_ORDER):
        for x in range(CUBE_ORDER):
            i = get_face_index(x, y)
            j = get_rotated_face_index(x, y)
            next_face[j] = face[i]
    return rotate_face(next_face, amount + delta)

def get_face_transform(f):
    """transforms the cube data from absolute, to 'face relative'"""
    positions = FACE_POSITIONS[f]
    rotations = FACE_ROTATIONS[f]
    return [tile for face in [rotate_face([i + positions[j] * NUM_TILES_FACE for i in range(NUM_TILES_FACE)], rotations[j]) for j in range(6)] for tile in face]

