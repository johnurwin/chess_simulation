# Coordinate conversion
files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
file_to_index = {f: i for i, f in enumerate(files)}
index_to_file = {i: f for f, i in file_to_index.items()}

def pos_to_coords(pos):
    return file_to_index[pos[0]], int(pos[1]) - 1

def coords_to_pos(coords):
    f, r = coords
    return f"{index_to_file[f]}{r + 1}"

# Base class
class Piece:
    def __init__(self, file_idx, rank_idx):
        self.file = file_idx
        self.rank = rank_idx

# Bishop
class Bishop(Piece):
    def can_capture(self, target):
        return abs(self.file - target.file) == abs(self.rank - target.rank)
    
    def is_valid_move(self, new_file, new_rank):
        # Check diagonal move and that the path is clear
        delta_file = abs(new_file - self.file)
        delta_rank = abs(new_rank - self.rank)
        if delta_file == delta_rank and delta_file != 0:
            # Optionally check no pieces in the way (if you track that)
            return True
        return False

    def move(self, new_file, new_rank):
        self.file = new_file
        self.rank = new_rank

# Rook
class Rook(Piece):
    def can_capture(self, target):
        return self.file == target.file or self.rank == target.rank
    
    def move_up(self, steps):
        self.rank = (self.rank + steps) % 8
    
    def move_right(self, steps):
        self.file = (self.file + steps) % 8
