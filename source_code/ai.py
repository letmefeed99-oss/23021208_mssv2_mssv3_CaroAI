import time

SCORE_TABLE = {
    (4, 2): 10_000_000,
    (4, 1): 10_000_000,
    (4, 0): 10_000_000,
    (3, 2): 500_000,
    (3, 1): 10_000,
    (3, 0): 0,
    (2, 2): 500,
    (2, 1): 50,
    (2, 0): 0,
}

TIME_LIMIT = 2.8
MAX_CAND   = 12
MAX_DEPTH  = 8

THREAT_URGENT = 400_000


class AI:
    def __init__(self, player='O', max_depth=MAX_DEPTH):
        self.player         = player
        self.opponent       = 'X' if player == 'O' else 'O'
        self.max_depth      = max_depth
        self.states_visited = 0
        self._start_time    = 0
        self._timeout       = False
        self._killers       = [[None, None] for _ in range(MAX_DEPTH + 2)]

    def _check_time(self):
        if time.time() - self._start_time >= TIME_LIMIT:
            self._timeout = True

    def evaluate(self, board):
        my_s  = self._score_board(board, self.player)
        opp_s = self._score_board(board, self.opponent)

        my_s  += self._double_threat_bonus(board, self.player)
        opp_s += self._double_threat_bonus(board, self.opponent)

        return my_s - int(opp_s * 1.5)

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
                        continue

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

    def _double_threat_bonus(self, board, player):
        threats = 0
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
                        continue

                    count = 0
                    for i in range(4):
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < size and 0 <= nc < size and grid[nr][nc] == player:
                            count += 1
                        else:
                            break

                    if count < 3:
                        continue

                    open_ends = 0
                    br, bc = r - dr, c - dc
                    er, ec = r + dr * count, c + dc * count
                    if 0 <= br < size and 0 <= bc < size and grid[br][bc] == '.':
                        open_ends += 1
                    if 0 <= er < size and 0 <= ec < size and grid[er][ec] == '.':
                        open_ends += 1

                    if count >= 4 or (count == 3 and open_ends == 2):
                        threats += 1

        if threats >= 2:
            return 800_000
        return 0

    def _quick_score(self, board, r, c, player):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        size = board.size
        grid = board.grid

        for dr, dc in directions:
            count    = 1
            open_ends = 0

            for i in range(1, 5):
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

            for i in range(1, 5):
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

    def _count_threats(self, board, player, threshold=THREAT_URGENT):
        threats = []
        for r, c in board.get_valid_moves():
            board.grid[r][c] = player
            s = self._quick_score(board, r, c, player)
            board.grid[r][c] = '.'
            if s >= threshold:
                threats.append((r, c, s))
        return threats

    def _find_urgent_move(self, board):
        moves = board.get_valid_moves()

        for r, c in moves:
            board.grid[r][c] = self.player
            win = board.check_win(self.player)
            board.grid[r][c] = '.'
            if win:
                return (r, c)

        for r, c in moves:
            board.grid[r][c] = self.opponent
            win = board.check_win(self.opponent)
            board.grid[r][c] = '.'
            if win:
                return (r, c)

        opp_threats = self._count_threats(board, self.opponent, threshold=THREAT_URGENT)
        if len(opp_threats) >= 1:
            best_block = None
            best_val   = -1
            for r, c in moves:
                board.grid[r][c] = self.player
                atk = self._quick_score(board, r, c, self.player)
                board.grid[r][c] = '.'

                board.grid[r][c] = self.opponent
                dfn = self._quick_score(board, r, c, self.opponent)
                board.grid[r][c] = '.'

                val = dfn * 2.0 + atk
                if val > best_val:
                    best_val   = val
                    best_block = (r, c)

            if len(opp_threats) >= 2 or opp_threats[0][2] >= 400_000:
                return best_block

        return None

    def _order_and_limit(self, board, moves, is_maximizing, depth):
        player   = self.player   if is_maximizing else self.opponent
        opponent = self.opponent if is_maximizing else self.player

        killer_a, killer_b = self._killers[depth]

        def score_move(move):
            if move == killer_a:
                return 999_999_999
            if move == killer_b:
                return 999_999_998

            r, c = move
            board.grid[r][c] = player
            atk = self._quick_score(board, r, c, player)
            board.grid[r][c] = '.'

            board.grid[r][c] = opponent
            dfn = self._quick_score(board, r, c, opponent)
            board.grid[r][c] = '.'

            return atk * 1.0 + dfn * 1.5

        scored = sorted(moves, key=score_move, reverse=True)
        return scored[:MAX_CAND]

    def _store_killer(self, move, depth):
        k = self._killers[depth]
        if move != k[0]:
            k[1] = k[0]
            k[0] = move

    def minimax(self, board, depth, is_maximizing):
        self.states_visited += 1

        result = board.is_game_over()
        if result == self.player:   return 10_000_000 + depth
        if result == self.opponent: return -10_000_000 - depth
        if result == 'Draw':        return 0
        if depth == 0:              return self.evaluate(board)

        moves = board.get_valid_moves()
        moves = self._order_and_limit(board, moves, is_maximizing, depth)

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

    def alphabeta(self, board, depth, alpha, beta, is_maximizing):
        self.states_visited += 1

        if self.states_visited % 500 == 0:
            self._check_time()
        if self._timeout:
            return self.evaluate(board)

        result = board.is_game_over()
        if result == self.player:   return 10_000_000 + depth
        if result == self.opponent: return -10_000_000 - depth
        if result == 'Draw':        return 0
        if depth == 0:              return self.evaluate(board)

        moves = board.get_valid_moves()
        moves = self._order_and_limit(board, moves, is_maximizing, depth)

        if is_maximizing:
            best = -float('inf')
            for r, c in moves:
                board.make_move(r, c, self.player)
                val = self.alphabeta(board, depth - 1, alpha, beta, False)
                board.undo_move(r, c)
                if val > best:
                    best = val
                alpha = max(alpha, best)
                if beta <= alpha:
                    self._store_killer((r, c), depth)
                    break
        else:
            best = float('inf')
            for r, c in moves:
                board.make_move(r, c, self.opponent)
                val = self.alphabeta(board, depth - 1, alpha, beta, True)
                board.undo_move(r, c)
                if val < best:
                    best = val
                beta = min(beta, best)
                if beta <= alpha:
                    self._store_killer((r, c), depth)
                    break

        return best

    def get_best_move(self, board, use_alphabeta=True):
        self.states_visited = 0
        self._start_time    = time.time()
        self._timeout       = False
        self._killers       = [[None, None] for _ in range(MAX_DEPTH + 2)]

        moves = board.get_valid_moves()
        if not moves:
            return None, 0, {}

        urgent = self._find_urgent_move(board)
        if urgent:
            execution_time = time.time() - self._start_time
            algo_name = "Urgent Move"
            stats = {
                'algorithm': algo_name,
                'depth': 0,
                'states': 1,
                'time': execution_time,
                'move': urgent,
                'score': 10_000_000,
            }
            print(f"[{algo_name}] Nước đi khẩn cấp: {urgent} | "
                  f"Thời gian: {execution_time:.3f}s")
            return urgent, 10_000_000, stats

        best_move   = None
        best_score  = -float('inf')
        final_depth = 1

        for depth in range(1, self.max_depth + 1):
            if self._timeout:
                break

            self._timeout      = False
            candidate_move     = None
            candidate_score    = -float('inf')

            ordered = self._order_and_limit(board, moves, is_maximizing=True, depth=depth)

            for r, c in ordered:
                if self._timeout:
                    break
                board.make_move(r, c, self.player)
                if use_alphabeta:
                    score = self.alphabeta(board, depth - 1,
                                           -float('inf'), float('inf'), False)
                else:
                    score = self.minimax(board, depth - 1, False)
                board.undo_move(r, c)

                if score > candidate_score:
                    candidate_score = score
                    candidate_move  = (r, c)

            if not self._timeout and candidate_move is not None:
                best_move   = candidate_move
                best_score  = candidate_score
                final_depth = depth

        execution_time = time.time() - self._start_time
        algo_name = "Alpha-Beta (ID)" if use_alphabeta else "Minimax (ID)"

        stats = {
            'algorithm': algo_name,
            'depth': final_depth,
            'states': self.states_visited,
            'time': execution_time,
            'move': best_move,
            'score': best_score,
        }

        print(f"[{algo_name}] Depth đạt được: {final_depth} | "
              f"Trạng thái: {self.states_visited:,} | "
              f"Thời gian: {execution_time:.3f}s | "
              f"Nước đi: {best_move} | Điểm: {best_score}")

        return best_move, best_score, stats
