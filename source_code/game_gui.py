import pygame
import sys
from board import Board
from ai import AI

BOARD_SIZE   = 9
CELL         = 64
MARGIN       = 48
PANEL_W      = 220
WIN_W        = MARGIN * 2 + CELL * BOARD_SIZE + PANEL_W
WIN_H        = MARGIN * 2 + CELL * BOARD_SIZE

BG           = (18,  18,  24)
GRID_COLOR   = (50,  50,  65)
GRID_BOLD    = (80,  80, 100)
X_COLOR      = (100, 180, 255)
O_COLOR      = (255, 120,  80)
WIN_LINE_CLR = (255, 215,   0)
PANEL_BG     = (26,  26,  36)
TEXT_COLOR   = (210, 210, 225)
MUTED        = (110, 110, 130)
HOVER_COLOR  = (255, 255, 255, 30)
BTN_BG       = (50,  50,  70)
BTN_HOVER    = (70,  70, 100)
BTN_TEXT     = (210, 210, 225)

def draw_board(surface, board, hover, win_cells):
    gx = MARGIN
    gy = MARGIN
    bw = CELL * BOARD_SIZE
    bh = CELL * BOARD_SIZE

    pygame.draw.rect(surface, (25, 25, 35), (gx, gy, bw, bh), border_radius=4)

    for i in range(BOARD_SIZE + 1):
        color = GRID_BOLD if i == 0 or i == BOARD_SIZE else GRID_COLOR
        width = 2 if i == 0 or i == BOARD_SIZE else 1
        pygame.draw.line(surface, color, (gx + i*CELL, gy), (gx + i*CELL, gy + bh), width)
        pygame.draw.line(surface, color, (gx, gy + i*CELL), (gx + bw, gy + i*CELL), width)

    if hover:
        hr, hc = hover
        hx = gx + hc * CELL
        hy = gy + hr * CELL
        hover_surf = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
        hover_surf.fill((255, 255, 255, 18))
        surface.blit(hover_surf, (hx, hy))

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            cx = gx + c * CELL + CELL // 2
            cy = gy + r * CELL + CELL // 2
            cell = board.grid[r][c]
            if cell == 'X':
                draw_x(surface, cx, cy, win_cells and (r, c) in win_cells)
            elif cell == 'O':
                draw_o(surface, cx, cy, win_cells and (r, c) in win_cells)

def draw_x(surface, cx, cy, highlight=False):
    color = WIN_LINE_CLR if highlight else X_COLOR
    pad = 18
    pygame.draw.line(surface, color, (cx-pad, cy-pad), (cx+pad, cy+pad), 3)
    pygame.draw.line(surface, color, (cx+pad, cy-pad), (cx-pad, cy+pad), 3)

def draw_o(surface, cx, cy, highlight=False):
    color = WIN_LINE_CLR if highlight else O_COLOR
    pygame.draw.circle(surface, color, (cx, cy), 20, 3)

def get_win_cells(board, player):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(board.size):
        for c in range(board.size):
            if board.grid[r][c] == player:
                for dr, dc in directions:
                    cells = []
                    for i in range(4):
                        nr, nc = r+dr*i, c+dc*i
                        if 0<=nr<board.size and 0<=nc<board.size and board.grid[nr][nc]==player:
                            cells.append((nr,nc))
                        else:
                            break
                    if len(cells) == 4:
                        return set(cells)
    return None

def draw_panel(surface, font_big, font_med, font_sm, status, turn, move_log, result):
    px = MARGIN * 2 + CELL * BOARD_SIZE
    py = 0
    pygame.draw.rect(surface, PANEL_BG, (px, py, PANEL_W, WIN_H))
    pygame.draw.line(surface, GRID_BOLD, (px, 0), (px, WIN_H), 1)

    y = 28

    title = font_big.render("CARO", True, TEXT_COLOR)
    surface.blit(title, (px + PANEL_W//2 - title.get_width()//2, y))
    y += 38

    sub = font_sm.render("4 quan lien tiep", True, MUTED)
    surface.blit(sub, (px + PANEL_W//2 - sub.get_width()//2, y))
    y += 36

    pygame.draw.line(surface, GRID_COLOR, (px+16, y), (px+PANEL_W-16, y), 1)
    y += 16

    if not result:
        if turn == 'X':
            label = font_med.render("Luot cua ban (X)", True, X_COLOR)
        else:
            label = font_med.render("Nanh suy nghi...", True, O_COLOR)
        surface.blit(label, (px + PANEL_W//2 - label.get_width()//2, y))
    else:
        if result == 'Draw':
            label = font_med.render("HOA!", True, TEXT_COLOR)
        elif result == 'X':
            label = font_med.render("Ban thang! (X)", True, X_COLOR)
        else:
            label = font_med.render("Nanh thang! (O)", True, O_COLOR)
        surface.blit(label, (px + PANEL_W//2 - label.get_width()//2, y))
    y += 36

    pygame.draw.line(surface, GRID_COLOR, (px+16, y), (px+PANEL_W-16, y), 1)
    y += 14

    log_title = font_sm.render("Lich su nuoc di", True, MUTED)
    surface.blit(log_title, (px+16, y))
    y += 22

    for entry in move_log[-12:]:
        txt = font_sm.render(entry, True, MUTED)
        surface.blit(txt, (px+16, y))
        y += 18

    btn_y = WIN_H - 56
    return draw_button(surface, font_sm, px+20, btn_y, PANEL_W-40, 36, "Choi lai")

def draw_button(surface, font, x, y, w, h, text):
    rect = pygame.Rect(x, y, w, h)
    mx, my = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mx, my)
    color = BTN_HOVER if hovered else BTN_BG
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, GRID_BOLD, rect, 1, border_radius=6)
    label = font.render(text, True, BTN_TEXT)
    surface.blit(label, (x + w//2 - label.get_width()//2, y + h//2 - label.get_height()//2))
    return rect

def get_cell(mx, my):
    c = (mx - MARGIN) // CELL
    r = (my - MARGIN) // CELL
    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
        return r, c
    return None

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Co Caro — vs Nanh")
    clock = pygame.time.Clock()

    try:
        font_big = pygame.font.SysFont("consolas", 26, bold=True)
        font_med = pygame.font.SysFont("consolas", 15, bold=True)
        font_sm  = pygame.font.SysFont("consolas", 13)
    except:
        font_big = pygame.font.SysFont(None, 28, bold=True)
        font_med = pygame.font.SysFont(None, 18, bold=True)
        font_sm  = pygame.font.SysFont(None, 15)

    def reset():
        # Người = X đi trước, máy = O
        return Board(BOARD_SIZE), AI(player='O', max_depth=8), 'X', [], None, None, False

    board, ai, turn, move_log, result, win_cells, ai_thinking = reset()

    AI_MOVE_EVENT = pygame.USEREVENT + 1
    hover = None

    running = True
    while running:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()
        cell = get_cell(mx, my)
        # Hover chỉ hiện khi đến lượt người (X)
        hover = cell if cell and board.grid[cell[0]][cell[1]] == '.' and not result and turn == 'X' else None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_rect = draw_panel(screen, font_big, font_med, font_sm, "", turn, move_log, result)
                if btn_rect.collidepoint(mx, my):
                    board, ai, turn, move_log, result, win_cells, ai_thinking = reset()
                    continue

                # Chỉ cho người (X) click khi đến lượt X
                if result or turn != 'X' or ai_thinking:
                    continue

                if cell and board.make_move(cell[0], cell[1], 'X'):
                    move_log.append(f"Ban   ({cell[0]},{cell[1]})")
                    result = board.is_game_over()
                    if result:
                        win_cells = get_win_cells(board, result) if result != 'Draw' else None
                    else:
                        turn = 'O'
                        ai_thinking = True
                        pygame.time.set_timer(AI_MOVE_EVENT, 80)

            if event.type == AI_MOVE_EVENT:
                pygame.time.set_timer(AI_MOVE_EVENT, 0)
                if not result and turn == 'O':
                    move, score, stats = ai.get_best_move(board, use_alphabeta=True)
                    if move:
                        board.make_move(move[0], move[1], 'O')
                        move_log.append(f"Nanh  ({move[0]},{move[1]})")
                        result = board.is_game_over()
                        if result:
                            win_cells = get_win_cells(board, result) if result != 'Draw' else None
                        turn = 'X'
                ai_thinking = False

        screen.fill(BG)
        draw_board(screen, board, hover, win_cells)
        btn = draw_panel(screen, font_big, font_med, font_sm, "", turn, move_log, result)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
