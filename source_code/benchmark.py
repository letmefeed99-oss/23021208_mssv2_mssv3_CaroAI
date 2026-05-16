

from board import Board
from ai   import AI

TEST_STATES = [
    {
        "name": "Trạng thái 1 — Đầu ván (chỉ 2 quân)",
        "moves": [
            (4, 4, 'X'),
            (4, 5, 'O'),
        ],
    },
    {

        "name": "Trạng thái 2 — Giữa ván cân bằng (hai bên có chuỗi 2)",
        "moves": [
            (4, 4, 'X'), (5, 5, 'O'),
            (4, 3, 'X'), (5, 6, 'O'),
            (3, 5, 'X'), (6, 4, 'O'),
            (3, 6, 'X'), (6, 3, 'O'),
        ],
    },
    {

        "name": "Trạng thái 3 — AI (O) có lợi thế tấn công nhẹ",
        "moves": [
            (4, 4, 'O'), (4, 5, 'O'),
            (5, 4, 'X'), (5, 5, 'X'),
            (3, 3, 'O'), (6, 6, 'X'),
            (2, 7, 'X'), (7, 2, 'O'),
        ],
    },
    {

        "name": "Trạng thái 4 — Người chơi (X) gây áp lực, AI cần phòng thủ",
        "moves": [
            (4, 3, 'X'), (4, 6, 'O'),
            (4, 4, 'X'), (5, 6, 'O'),
            (3, 4, 'X'), (3, 6, 'O'),
            (3, 3, 'X'), (6, 5, 'O'),
        ],
    },
    {
     
        "name": "Trạng thái 5 — Bàn cờ phức tạp (nhiều quân, nhiều hướng tấn công)",
        "moves": [
            (4, 4, 'X'), (4, 5, 'O'),
            (3, 4, 'X'), (3, 5, 'O'),
            (5, 3, 'X'), (5, 6, 'O'),
            (2, 4, 'X'), (2, 5, 'O'),
            (6, 3, 'X'), (6, 6, 'O'),
            (4, 3, 'X'), (4, 6, 'O'),
            (3, 3, 'X'), (3, 6, 'O'),
            (5, 4, 'X'), (5, 5, 'O'),
        ],
    },
]

DEPTHS = [2, 3, 4]  

# ─────────────────────────────────────────────────────────────────────────────

def build_board(moves):
    """Tạo bàn cờ từ danh sách nước đi."""
    board = Board(size=9)
    for r, c, player in moves:
        board.grid[r][c] = player
    return board


def run_one(board, depth, use_alphabeta):

    import time as _time
    ai = AI(player='O', max_depth=depth)
    ai.states_visited = 0
    ai._start_time    = _time.time()
    ai._timeout       = False
    ai._killers       = [[None, None] for _ in range(10 + 2)]

    moves = board.get_valid_moves()
    if not moves:
        return None, {'states': 0, 'time': 0, 'depth': 0}

    best_move   = None
    best_score  = -float('inf')
    final_depth = 1

    for d in range(1, depth + 1):
        candidate_move  = None
        candidate_score = -float('inf')
        ordered = ai._order_and_limit(board, moves, is_maximizing=True, depth=d)
        for r, c in ordered:
            board.make_move(r, c, ai.player)
            if use_alphabeta:
                score = ai.alphabeta(board, d - 1, -float('inf'), float('inf'), False)
            else:
                score = ai.minimax(board, d - 1, False)
            board.undo_move(r, c)
            if score > candidate_score:
                candidate_score = score
                candidate_move  = (r, c)
        if candidate_move is not None:
            best_move   = candidate_move
            final_depth = d

    elapsed = _time.time() - ai._start_time
    stats = {'states': ai.states_visited, 'time': elapsed, 'depth': final_depth}
    return best_move, stats


def compare(state, depth):

    board_mm = build_board(state["moves"])
    board_ab = build_board(state["moves"])

    move_mm, stats_mm = run_one(board_mm, depth, use_alphabeta=False)
    move_ab, stats_ab = run_one(board_ab, depth, use_alphabeta=True)

    same_move = (move_mm == move_ab)
    states_saved = stats_mm['states'] - stats_ab['states']
    pct_saved    = (states_saved / stats_mm['states'] * 100) if stats_mm['states'] else 0

    return {
        "depth":        depth,
        "move_mm":      move_mm,
        "move_ab":      move_ab,
        "same_move":    same_move,
        "states_mm":    stats_mm['states'],
        "states_ab":    stats_ab['states'],
        "states_saved": states_saved,
        "pct_saved":    pct_saved,
        "time_mm":      stats_mm['time'],
        "time_ab":      stats_ab['time'],
        "depth_mm":     stats_mm['depth'],
        "depth_ab":     stats_ab['depth'],
    }


def print_result(res, file=None):
    def p(text=""):
        print(text)
        if file:
            file.write(text + "\n")

    move_mm_str = str(res['move_mm']) if res['move_mm'] else "None"
    move_ab_str = str(res['move_ab']) if res['move_ab'] else "None"

    p(f"  Độ sâu {res['depth']}:")
    p(f"    Minimax    — nước đi: {move_mm_str:<12s}  "
      f"trạng thái: {res['states_mm']:>8,}  "
      f"thời gian: {res['time_mm']:.3f}s  "
      f"depth thực: {res['depth_mm']}")
    p(f"    Alpha-Beta — nước đi: {move_ab_str:<12s}  "
      f"trạng thái: {res['states_ab']:>8,}  "
      f"thời gian: {res['time_ab']:.3f}s  "
      f"depth thực: {res['depth_ab']}")
    p(f"    Cùng nước đi: {'✓ Có' if res['same_move'] else '✗ Khác'}  |  "
      f"Alpha-Beta tiết kiệm: {res['states_saved']:,} trạng thái ({res['pct_saved']:.1f}%)")


def run_benchmark():
    lines = []
    header = "=" * 70
    separator = "-" * 70

    with open("benchmark_results.txt", "w", encoding="utf-8") as f:

        def p(text=""):
            print(text)
            f.write(text + "\n")

        p(header)
        p("  BENCHMARK: So sánh Minimax vs Alpha-Beta")
        p("  Caro 4 quân liên tiếp, bàn 9x9, AI = O (MAX)")
        p(header)

        for state in TEST_STATES:
            p()
            p(f"{'━' * 70}")
            p(f"  {state['name']}")
            p(f"{'━' * 70}")
            board_display = build_board(state["moves"])
            p("  Bàn cờ:")
            import io, sys
            buf = io.StringIO()
            old = sys.stdout; sys.stdout = buf
            board_display.display()
            sys.stdout = old
            for line in buf.getvalue().splitlines():
                p("    " + line)

            for depth in DEPTHS:
                res = compare(state, depth)
                print_result(res, file=f)

        p()
        p(header)
        p("  Kết thúc benchmark. Kết quả đã lưu vào benchmark_results.txt")
        p(header)


if __name__ == "__main__":
    run_benchmark()
