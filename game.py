import random
import pygame
from pieces import Bishop, Rook, pos_to_coords, coords_to_pos
from graphics import TILE_SIZE, draw_board

class GameState:
    ROOK_MOVE = 0
    BISHOP_MOVE = 1
    GAME_OVER = 2

    def __init__(self):
        self.bishop = None
        self.rook = None
        self.bishop_wins = 0
        self.rook_wins = 0
        self.round_num = 1
        self.max_rounds = 15
        self.state = None
        self.message = ""
        self.game_over = False
        self.bishop_mode = None
        self.reset_game()

    def reset_game(self):
        self.bishop = Bishop(*pos_to_coords("c3"))
        self.rook = Rook(*pos_to_coords("h1"))
        self.round_num = 1
        self.max_rounds = 15
        self.game_over = False
        self.message = "Rook moves first."
        self.state = self.ROOK_MOVE

    def animate_rook_move(self, screen):
        board_rect = pygame.Rect(0, 0, TILE_SIZE * 8, TILE_SIZE * 8)
        direction = random.choice(["up", "right"])
        steps = random.randint(1, 6) + random.randint(1, 6)

        self.message = f"Round {self.round_num}: Rook moving {direction} by {steps} steps..."
        for _ in range(steps):
            if direction == "up":
                self.rook.move_up(1)
            else:
                self.rook.move_right(1)
            screen.fill((255, 255, 255), board_rect)
            draw_board(screen, self.bishop, self.rook)
            pygame.display.update(board_rect)
            pygame.time.delay(150)

        self.message = f"Round {self.round_num}: Rook moved {direction} by {steps} steps to {coords_to_pos((self.rook.file, self.rook.rank))}."

        if self.bishop.can_capture(self.rook):
            self.message += " Bishop captures rook! Bishop wins!"
            self.game_over = True
            self.state = self.GAME_OVER
            self.bishop_wins += 1

        elif self.rook.can_capture(self.bishop):
            self.message += " Rook captures bishop! Rook wins!"
            self.game_over = True
            self.state = self.GAME_OVER
            self.rook_wins += 1

        else:
            if self.bishop_mode == "human":
                self.message += " Your turn: Move the bishop."
                self.state = self.BISHOP_MOVE
            else:
                self.round_num += 1
                if self.round_num > self.max_rounds:
                    self.message = f"Rook survives all {self.max_rounds} rounds — Rook wins!"
                    self.game_over = True
                    self.state = self.GAME_OVER
                    self.rook_wins += 1