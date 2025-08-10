import pygame

TILE_SIZE = 80
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
TEXT_COLOR = (0, 0, 0)

def draw_board(screen, bishop, rook):
    # Draw board squares
    for rank in range(8):
        for file in range(8):
            color = LIGHT_COLOR if (file + rank) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, (file * TILE_SIZE, (7 - rank) * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Load a font that supports chess symbols
    try:
        font = pygame.font.SysFont("symbola", 72)  # DejaVu Sans supports chess symbols
    except:
        font = pygame.font.SysFont(None, 72)  # fallback

    # Render bishop and rook unicode characters
    bishop_surf = font.render("B", True, TEXT_COLOR)
    bishop_pos = (bishop.file * TILE_SIZE + TILE_SIZE // 8, (7 - bishop.rank) * TILE_SIZE + TILE_SIZE // 10)
    screen.blit(bishop_surf, bishop_pos)

    rook_surf = font.render("R", True, TEXT_COLOR)
    rook_pos = (rook.file * TILE_SIZE + TILE_SIZE // 8, (7 - rook.rank) * TILE_SIZE + TILE_SIZE // 10)
    screen.blit(rook_surf, rook_pos)

    pygame.display.flip()
