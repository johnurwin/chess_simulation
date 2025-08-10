import random
import pygame
from pieces import Bishop, Rook, pos_to_coords, coords_to_pos
from board import draw_board, TILE_SIZE

def draw_button(screen, rect, text, font, active=True):
    color = (0, 150, 0) if active else (100, 100, 100)
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def animate_rook_move(screen, rook, direction, steps, bishop):
    board_rect = pygame.Rect(0, 0, TILE_SIZE * 8, TILE_SIZE * 8)
    for step in range(steps):
        if direction == "up":
            rook.move_up(1)
        else:
            rook.move_right(1)

        # Clear and redraw only board area
        screen.fill((255, 255, 255), board_rect)
        draw_board(screen, bishop, rook)

        pygame.display.update(board_rect)  # Update just the board
        pygame.time.delay(150)  # delay for animation smoothness

def play_game():
    pygame.init()
    screen = pygame.display.set_mode((TILE_SIZE * 8, TILE_SIZE * 8 + 200))
    pygame.display.set_caption("Rook vs Bishop")

    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 36)

    stationary_button = pygame.Rect(TILE_SIZE * 1, TILE_SIZE * 8 + 90, TILE_SIZE * 3, 40)
    human_button = pygame.Rect(TILE_SIZE * 4, TILE_SIZE * 8 + 90, TILE_SIZE * 3, 40)
    restart_button = pygame.Rect(TILE_SIZE * 3, TILE_SIZE * 8 + 150, TILE_SIZE * 2, 40)

    bishop_mode = None
    bishop_wins = 0
    rook_wins = 0

    ROOK_MOVE = 0
    BISHOP_MOVE = 1
    GAME_OVER = 2

    bishop = None
    rook = None
    round_num = 1
    max_rounds = 15
    game_over = False
    message = ""
    state = None

    def reset_game():
        nonlocal bishop, rook, round_num, max_rounds, game_over, message, state
        bishop = Bishop(*pos_to_coords("c3"))
        rook = Rook(*pos_to_coords("h1"))
        round_num = 1
        max_rounds = 15
        game_over = False
        message = "Rook moves first."
        state = ROOK_MOVE

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Mode buttons (always active)
                if stationary_button.collidepoint(event.pos):
                    if bishop_mode != "stationary":
                        bishop_mode = "stationary"
                        reset_game()
                        print("Bishop mode: Stationary")
                elif human_button.collidepoint(event.pos):
                    if bishop_mode != "human":
                        bishop_mode = "human"
                        reset_game()
                        print("Bishop mode: Human-controlled")
                # Restart button (only on game over)
                elif state == GAME_OVER and restart_button.collidepoint(event.pos):
                    reset_game()
                # Bishop move input if human-controlled and bishop turn
                elif state == BISHOP_MOVE and bishop_mode == "human" and not game_over:
                    mouse_x, mouse_y = event.pos
                    if mouse_y <= TILE_SIZE * 8:
                        file_clicked = mouse_x // TILE_SIZE
                        rank_clicked = 7 - (mouse_y // TILE_SIZE)

                        if bishop.is_valid_move(file_clicked, rank_clicked):
                            bishop.move(file_clicked, rank_clicked)
                            message = f"Bishop moved to {coords_to_pos((file_clicked, rank_clicked))}"
                            state = ROOK_MOVE
                            round_num += 1

                            if bishop.can_capture(rook):
                                message = f"🏆 Bishop captures Rook at {coords_to_pos((rook.file, rook.rank))} — You win!"
                                game_over = True
                                state = GAME_OVER
                                bishop_wins += 1
                        else:
                            message = "Invalid bishop move. Try again."

        if bishop_mode is None:
            # Show prompt and mode buttons only
            screen.fill((240, 240, 240))
            prompt = font.render("Choose Bishop Mode:", True, (0, 0, 0))
            screen.blit(prompt, (TILE_SIZE * 2, TILE_SIZE * 8))
            draw_button(screen, stationary_button, "Stationary Bishop", font, active=False)
            draw_button(screen, human_button, "Human-controlled Bishop", font, active=False)
            pygame.display.flip()
            clock.tick(30)
            continue

        if state == ROOK_MOVE and not game_over:
            direction = random.choice(["up", "right"])
            steps = random.randint(1, 6) + random.randint(1, 6)
            print(f"Round {round_num}: Coin toss -> {direction}, Dice -> {steps}")

            message = f"Round {round_num}: Rook moving {direction} by {steps} steps..."

            # Draw full UI once before animation
            screen.fill((255, 255, 255))
            draw_board(screen, bishop, rook)

            pygame.draw.rect(screen, (200, 200, 200), (0, TILE_SIZE * 8, TILE_SIZE * 8, 40))
            msg_surface = font.render(message, True, (0, 0, 0))
            screen.blit(msg_surface, (10, TILE_SIZE * 8 + 10))

            pygame.draw.rect(screen, (230, 230, 230), (0, TILE_SIZE * 8 + 40, TILE_SIZE * 8, 40))
            score_text = f"Score — Bishop: {bishop_wins} | Rook: {rook_wins}"
            score_surface = font.render(score_text, True, (0, 0, 0))
            screen.blit(score_surface, (10, TILE_SIZE * 8 + 50))

            draw_button(screen, stationary_button, "Stationary Bishop", font, active=(bishop_mode=="stationary"))
            draw_button(screen, human_button, "Human-controlled Bishop", font, active=(bishop_mode=="human"))
            if state == GAME_OVER:
                pygame.draw.rect(screen, (100, 200, 100), restart_button)
                restart_text = big_font.render("Restart", True, (0, 0, 0))
                text_rect = restart_text.get_rect(center=restart_button.center)
                screen.blit(restart_text, text_rect)

            pygame.display.flip()

            # Animate rook move — only redraw board inside animation
            animate_rook_move(screen, rook, direction, steps, bishop)

            print(f"Rook at {coords_to_pos((rook.file, rook.rank))}")

            message = f"Round {round_num}: Rook moved {direction} by {steps} steps to {coords_to_pos((rook.file, rook.rank))}."

            if bishop.can_capture(rook):
                message += " Bishop captures rook! Bishop wins!"
                print(message)
                game_over = True
                state = GAME_OVER
                bishop_wins += 1
            else:
                if bishop_mode == "human":
                    message += " Your turn: Move the bishop."
                    state = BISHOP_MOVE
                else:
                    round_num += 1
                    if round_num > max_rounds:
                        message = f"Rook survives all {max_rounds} rounds — Rook wins!"
                        print(message)
                        game_over = True
                        state = GAME_OVER
                        rook_wins += 1

        # Draw everything every frame outside animation
        if state != ROOK_MOVE:
            screen.fill((255, 255, 255))
            draw_board(screen, bishop, rook)

            pygame.draw.rect(screen, (200, 200, 200), (0, TILE_SIZE * 8, TILE_SIZE * 8, 40))
            msg_surface = font.render(message, True, (0, 0, 0))
            screen.blit(msg_surface, (10, TILE_SIZE * 8 + 10))

            pygame.draw.rect(screen, (230, 230, 230), (0, TILE_SIZE * 8 + 40, TILE_SIZE * 8, 40))
            score_text = f"Score — Bishop: {bishop_wins} | Rook: {rook_wins}"
            score_surface = font.render(score_text, True, (0, 0, 0))
            screen.blit(score_surface, (10, TILE_SIZE * 8 + 50))

            draw_button(screen, stationary_button, "Stationary Bishop", font, active=(bishop_mode=="stationary"))
            draw_button(screen, human_button, "Human-controlled Bishop", font, active=(bishop_mode=="human"))

            if state == GAME_OVER:
                pygame.draw.rect(screen, (100, 200, 100), restart_button)
                restart_text = big_font.render("Restart", True, (0, 0, 0))
                text_rect = restart_text.get_rect(center=restart_button.center)
                screen.blit(restart_text, text_rect)

            pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    play_game()
