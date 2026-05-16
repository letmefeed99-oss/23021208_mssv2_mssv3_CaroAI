from board import Board
from ai import AI

def print_banner():
    print("=" * 45)
    print("       TRÒ CHƠI CỜ CARO  (4 quân liên tiếp)")
    print("       Người: X   |   Nanh: O")
    print("=" * 45)

def choose_settings():
    # ── Chọn thuật toán ──────────────────────────────
    print("\nChọn thuật toán AI:")
    print("  1. Minimax")
    print("  2. Alpha-Beta (khuyên dùng)")
    while True:
        choice = input("Nhập 1 hoặc 2: ").strip()
        if choice in ('1', '2'):
            use_alphabeta = (choice == '2')
            break
        print("Vui lòng nhập 1 hoặc 2.")

    # ── Chọn độ sâu ──────────────────────────────────
    print("\nChọn độ sâu tìm kiếm (càng cao AI càng mạnh nhưng chậm hơn):")
    print("  Gợi ý: 2–3 cho Minimax, 4–6 cho Alpha-Beta")
    while True:
        try:
            depth = int(input("Nhập độ sâu (1-8): ").strip())
            if 1 <= depth <= 8:
                break
            print("Độ sâu phải từ 1 đến 8.")
        except ValueError:
            print("Vui lòng nhập một số nguyên.")

    return depth, use_alphabeta

def play_game():
    print_banner()
    depth, use_alphabeta = choose_settings()

    board = Board(size=9)
    ai = AI(player='O', max_depth=depth)
    algo_label = "Alpha-Beta" if use_alphabeta else "Minimax"
    print(f"\n✔ Chế độ: {algo_label} | Độ sâu: {depth}\n")
    board.display()

    while True:

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

        print("Nanh (O) đang suy nghĩ...")
        best_move, best_score, stats = ai.get_best_move(board, use_alphabeta=use_alphabeta)

        if best_move is None:
            print("Nanh không tìm được nước đi hợp lệ!")
            break

        board.make_move(best_move[0], best_move[1], 'O')
        print(f"\n=> Nanh đánh tại: {best_move}\n")
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
        print("  🤖 Nanh (O) đã THẮNG! Chúc bạn may mắn lần sau.")
    print("=" * 45)

if __name__ == "__main__":
    play_game()
