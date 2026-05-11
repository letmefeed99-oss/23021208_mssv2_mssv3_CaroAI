from board import Board
from ai import AI


def print_banner():
    print("=" * 45)
    print("       TRÒ CHƠI CỜ CARO  (4 quân liên tiếp)")
    print("       Người: X   |   Máy: O")
    print("=" * 45)


def choose_settings():
    """Cho người chơi chọn độ khó và thuật toán."""
    print("\nChọn độ khó:")
    print("  1. Dễ   (depth=2, Minimax)")
    print("  2. Vừa  (depth=3, Alpha-Beta)")
    print("  3. Khó  (depth=4, Alpha-Beta)  ← khuyến nghị")
    print("  4. Siêu khó (depth=5, Alpha-Beta, chậm hơn)")

    choice = input("Nhập lựa chọn (1-4, mặc định 3): ").strip()
    settings = {
        '1': (2, False),
        '2': (3, True),
        '3': (4, True),
        '4': (5, True),
    }
    depth, use_ab = settings.get(choice, (4, True))
    return depth, use_ab


def play_game():
    print_banner()
    depth, use_alphabeta = choose_settings()

    board = Board(size=9)
    ai = AI(player='O', max_depth=depth)
    algo_label = "Alpha-Beta" if use_alphabeta else "Minimax"
    print(f"\n✔ Chế độ: {algo_label} | Độ sâu: {depth}\n")
    board.display()

    while True:
        # ── LƯỢT NGƯỜI (X) ──────────────────────────────────────────
        print("Lượt của bạn (X).")
        while True:
            try:
                inp = input("Nhập hàng cột (vd: 4 4), hoặc 'q' để thoát: ").strip()
                if inp.lower() == 'q':
                    print("Thoát game.")
                    return
                r, c = map(int, inp.split())
                if board.make_move(r, c, 'X'):
                    break
                else:
                    print("Ô đã có quân hoặc ngoài bàn cờ. Thử lại.")
            except ValueError:
                print("Nhập sai định dạng. Vui lòng nhập 2 số cách nhau bằng dấu cách.")

        board.display()
        result = board.is_game_over()
        if result:
            _print_result(result)
            break

        # ── LƯỢT MÁY (O) ────────────────────────────────────────────
        print("Máy (O) đang suy nghĩ...")
        best_move, best_score, stats = ai.get_best_move(board, use_alphabeta=use_alphabeta)

        if best_move is None:
            print("Máy không tìm được nước đi hợp lệ!")
            break

        board.make_move(best_move[0], best_move[1], 'O')
        print(f"\n=> Máy đánh tại: {best_move}\n")
        board.display()

        result = board.is_game_over()
        if result:
            _print_result(result)
            break


def _print_result(result):
    print("=" * 45)
    if result == 'Draw':
        print("  Bàn cờ đầy — KẾT QUẢ: HÒA!")
    elif result == 'X':
        print("  🎉 Chúc mừng! Bạn (X) đã THẮNG!")
    elif result == 'O':
        print("  🤖 Máy (O) đã THẮNG! Chúc bạn may mắn lần sau.")
    print("=" * 45)


if __name__ == "__main__":
    play_game()
