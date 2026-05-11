import time

SCORE_TABLE = {
    (4, 2): 1_000_000,
    (4, 1): 1_000_000,
    (4, 0): 1_000_000,
    (3, 2): 50_000,
    (3, 1): 1_000,
    (3, 0): 0,
    (2, 2): 100,
    (2, 1): 10,
    (2, 0): 0,
}

# Giới hạn số nước đi xét mỗi tầng — đây là tối ưu quan trọng nhất
MAX_CANDIDATES = 15


class AI:
    def __init__(self, player='O', max_depth=4):
        self.player = player
        self.opponent = 'X'
        self.max_depth = max_depth
        self.states_visited = 0

    # ------------------------------------------------------------------
    # HÀM ĐÁNH GIÁ TOÀN BÀN (dùng ở leaf node)
    # ------------------------------------------------------------------

    def evaluate(self, board):
        my_score = self._score_board(board, self.player)
        opp_score = self._score_board(board, self.opponent)
        return my_score - int(opp_score * 1.2)

    def _score_board(self, board, player):
        total = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        size = board.size
        grid = board.grid

        for r in range(size):
            for c in range(size):
                if grid[r][c] != player:
                    continue
                for dr, dc in directions:
                    pr, pc = r - dr, c - dc
                    if 0 <= pr < size and 0 <= pc < size and grid[pr][pc] == player:
                        continue  # Không phải đầu chuỗi

                    count = 0
                    for i in range(4):
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < size and 0 <= nc < size and grid[nr][nc] == player:
                            count += 1
                        else:
                            break

                    if count == 0:
                        continue

                    open_ends = 0
                    br, bc = r - dr, c - dc
                    er, ec = r + dr * count, c + dc * count
                    if 0 <= br < size and 0 <= bc < size and grid[br][bc] == '.':
                        open_ends += 1
                    if 0 <= er < size and 0 <= ec < size and grid[er][ec] == '.':
                        open_ends += 1

                    total += SCORE_TABLE.get((count, open_ends), 0)

        return total

    # ------------------------------------------------------------------
    # QUICK SCORE — chỉ xét các chuỗi đi qua ô (r,c)
    # Nhanh hơn ~10x so với _score_board đầy đủ, dùng để sắp xếp moves
    # ------------------------------------------------------------------

    def _quick_score(self, board, r, c, player):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        size = board.size
        grid = board.grid

        for dr, dc in directions:
            count = 1
            open_ends = 0

            for i in range(1, 4):
                nr, nc = r - dr * i, c - dc * i
                if 0 <= nr < size and 0 <= nc < size:
                    if grid[nr][nc] == player:
                        count += 1
                    elif grid[nr][nc] == '.':
                        open_ends += 1
                        break
                    else:
                        break
                else:
                    break

            for i in range(1, 4):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < size and 0 <= nc < size:
                    if grid[nr][nc] == player:
                        count += 1
                    elif grid[nr][nc] == '.':
                        open_ends += 1
                        break
                    else:
                        break
                else:
                    break

            score += SCORE_TABLE.get((min(count, 4), open_ends), 0)

        return score

    # ------------------------------------------------------------------
    # MOVE ORDERING + GIỚI HẠN CANDIDATES
    # Kết hợp điểm tấn công + điểm phòng thủ, chỉ giữ top MAX_CANDIDATES
    # ------------------------------------------------------------------

    def _order_and_limit(self, board, moves, is_maximizing):
        player   = self.player   if is_maximizing else self.opponent
        opponent = self.opponent if is_maximizing else self.player

        def score_move(move):
            r, c = move
            board.grid[r][c] = player
            atk = self._quick_score(board, r, c, player)
            board.grid[r][c] = '.'

            board.grid[r][c] = opponent
            dfn = self._quick_score(board, r, c, opponent)
            board.grid[r][c] = '.'

            return atk + dfn

        scored = sorted(moves, key=score_move, reverse=True)
        return scored[:MAX_CANDIDATES]

    # ------------------------------------------------------------------
    # MINIMAX (không giới hạn candidates — để so sánh công bằng)
    # ------------------------------------------------------------------

    def minimax(self, board, depth, is_maximizing):
        self.states_visited += 1

        result = board.is_game_over()
        if result == self.player:   return 1_000_000 + depth
        if result == self.opponent: return -1_000_000 - depth
        if result == 'Draw':        return 0
        if depth == 0:              return self.evaluate(board)

        moves = board.get_valid_moves()

        if is_maximizing:
            best = -float('inf')
            for r, c in moves:
                board.make_move(r, c, self.player)
                best = max(best, self.minimax(board, depth - 1, False))
                board.undo_move(r, c)
            return best
        else:
            best = float('inf')
            for r, c in moves:
                board.make_move(r, c, self.opponent)
                best = min(best, self.minimax(board, depth - 1, True))
                board.undo_move(r, c)
            return best

    # ------------------------------------------------------------------
    # ALPHA-BETA + MOVE ORDERING + GIỚI HẠN CANDIDATES
    # ------------------------------------------------------------------

    def alphabeta(self, board, depth, alpha, beta, is_maximizing):
        self.states_visited += 1

        result = board.is_game_over()
        if result == self.player:   return 1_000_000 + depth
        if result == self.opponent: return -1_000_000 - depth
        if result == 'Draw':        return 0
        if depth == 0:              return self.evaluate(board)

        moves = board.get_valid_moves()
        moves = self._order_and_limit(board, moves, is_maximizing)  # ← Then chốt

        if is_maximizing:
            best = -float('inf')
            for r, c in moves:
                board.make_move(r, c, self.player)
                best = max(best, self.alphabeta(board, depth - 1, alpha, beta, False))
                board.undo_move(r, c)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        else:
            best = float('inf')
            for r, c in moves:
                board.make_move(r, c, self.opponent)
                best = min(best, self.alphabeta(board, depth - 1, alpha, beta, True))
                board.undo_move(r, c)
                beta = min(beta, best)
                if beta <= alpha:
                    break

        return best

    # ------------------------------------------------------------------
    # CHỌN NƯỚC ĐI TỐT NHẤT
    # ------------------------------------------------------------------

    def get_best_move(self, board, use_alphabeta=True):
        self.states_visited = 0
        start_time = time.time()

        best_score = -float('inf')
        best_move  = None

        moves = board.get_valid_moves()
        moves = self._order_and_limit(board, moves, is_maximizing=True)

        for r, c in moves:
            board.make_move(r, c, self.player)
            if use_alphabeta:
                score = self.alphabeta(board, self.max_depth - 1,
                                       -float('inf'), float('inf'), False)
            else:
                score = self.minimax(board, self.max_depth - 1, False)
            board.undo_move(r, c)

            if score > best_score:
                best_score = score
                best_move  = (r, c)

        execution_time = time.time() - start_time
        algo_name = "Alpha-Beta" if use_alphabeta else "Minimax"

        stats = {
            'algorithm': algo_name,
            'depth': self.max_depth,
            'states': self.states_visited,
            'time': execution_time,
            'move': best_move,
            'score': best_score,
        }

        print(f"\n[{algo_name}] Độ sâu: {self.max_depth} | "
              f"Trạng thái đã xét: {self.states_visited:,} | "
              f"Thời gian: {execution_time:.4f}s | "
              f"Nước đi: {best_move} | Điểm: {best_score}")

        return best_move, best_score, stats
