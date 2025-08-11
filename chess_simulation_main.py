# chess_simulation_main.py
import pygame
from graphics import TILE_SIZE, draw_board, draw_button
from pieces import coords_to_pos
from game import GameState

def play_game():
    pygame.init()
    screen = pygame.display.set_mode((TILE_SIZE * 8, TILE_SIZE * 8 + 200), pygame.RESIZABLE)
    pygame.display.set_caption("Rook vs Bishop")

    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 36)

    game = GameState()
    clock = pygame.time.Clock()

    running = True
    while running:
        width, height = screen.get_size()
        board_height = TILE_SIZE * 8
        button_width = width // 3
        button_height = 40
        button_y = board_height + 20

        # Dynamically position buttons based on current window size
        stationary_button = pygame.Rect(width // 8, button_y, button_width, button_height)
        human_button = pygame.Rect(width // 2, button_y, button_width, button_height)
        restart_button = pygame.Rect(width // 3, button_y + 60, button_width, button_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if stationary_button.collidepoint(event.pos):
                    if game.bishop_mode != "stationary":
                        game.bishop_mode = "stationary"
                        game.reset_game()
                elif human_button.collidepoint(event.pos):
                    if game.bishop_mode != "human":
                        game.bishop_mode = "human"
                        game.reset_game()
                elif game.state == GameState.GAME_OVER and restart_button.collidepoint(event.pos):
                    game.reset_game()
                elif (game.state == GameState.BISHOP_MOVE and 
                      game.bishop_mode == "human" and not game.game_over):
                    mouse_x, mouse_y = event.pos
                    if mouse_y <= board_height:
                        file_clicked = mouse_x // TILE_SIZE
                        rank_clicked = 7 - (mouse_y // TILE_SIZE)

                        if game.bishop.is_valid_move(file_clicked, rank_clicked):
                            game.bishop.move(file_clicked, rank_clicked)
                            game.message = f"Bishop moved to {coords_to_pos((file_clicked, rank_clicked))}"
                            game.state = GameState.ROOK_MOVE
                            game.round_num += 1
                            if game.bishop.can_capture(game.rook):
                                game.message = f"🏆 Bishop captures Rook at {coords_to_pos((game.rook.file, game.rook.rank))} — You win!"
                                game.game_over = True
                                game.state = GameState.GAME_OVER
                                game.bishop_wins += 1
                        else:
                            game.message = "Invalid bishop move. Try again."

        if game.bishop_mode is None:
            screen.fill((240, 240, 240))
            prompt = font.render("Choose Bishop Mode:", True, (0, 0, 0))
            screen.blit(prompt, (width // 3, board_height))
            draw_button(screen, stationary_button, "Stationary Bishop", font, active=False)
            draw_button(screen, human_button, "Human-controlled Bishop", font, active=False)
            pygame.display.flip()
            clock.tick(30)
            continue

        if game.state == GameState.ROOK_MOVE and not game.game_over:
            # Draw the board before animation
            screen.fill((255, 255, 255))
            draw_board(screen, game.bishop, game.rook)
            pygame.display.flip()

            # Animate rook move (this will update board internally)
            game.animate_rook_move(screen)

        # Draw UI elements every frame outside animation
        screen.fill((255, 255, 255))
        draw_board(screen, game.bishop, game.rook)

        pygame.draw.rect(screen, (200, 200, 200), (0, board_height, width, 40))
        msg_surface = font.render(game.message, True, (0, 0, 0))
        screen.blit(msg_surface, (10, board_height + 10))

        pygame.draw.rect(screen, (230, 230, 230), (0, board_height + 40, width, 40))
        score_text = f"Score — Bishop: {game.bishop_wins} | Rook: {game.rook_wins}"
        score_surface = font.render(score_text, True, (0, 0, 0))
        screen.blit(score_surface, (10, board_height + 50))

        draw_button(screen, stationary_button, "Stationary Bishop", font, active=(game.bishop_mode == "stationary"))
        draw_button(screen, human_button, "Human-controlled Bishop", font, active=(game.bishop_mode == "human"))

        if game.state == GameState.GAME_OVER:
            pygame.draw.rect(screen, (100, 200, 100), restart_button)
            restart_text = big_font.render("Restart", True, (0, 0, 0))
            text_rect = restart_text.get_rect(center=restart_button.center)
            screen.blit(restart_text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    play_game()
