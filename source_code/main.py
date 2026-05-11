from board import Board
from ai import AI

def play_game():
    board = Board(size=9)
    # Khởi tạo máy đánh 'O', độ sâu là 2 (tăng lên 3 sẽ thông minh hơn nhưng tính toán chậm hơn)
    ai = AI(player='O', max_depth=2) 
    
    print("--- TRÒ CHƠI CỜ CARO (AI MINIMAX) ---")
    board.display()
    
    while True:
        # LƯỢT CỦA NGƯỜI (X)
        print("Lượt của bạn (X).")
        try:
            # Nhập tọa độ, ví dụ nhập: 4 4
            r, c = map(int, input("Nhập hàng và cột (cách nhau bởi dấu cách): ").split())
        except ValueError:
            print("Vui lòng nhập 2 số cách nhau bằng dấu cách!")
            continue
            
        if not board.make_move(r, c, 'X'):
            print("Nước đi không hợp lệ (ô đã có quân hoặc ngoài bàn cờ). Vui lòng đi lại.")
            continue
            
        board.display()
        if board.is_game_over():
            break
            
        # LƯỢT CỦA MÁY (O)
        print("Máy (O) đang suy nghĩ...")
        best_move, best_score = ai.get_best_move(board)
        
        if best_move:
            board.make_move(best_move[0], best_move[1], 'O')
            print(f"\n=> Máy quyết định đánh tại ô: {best_move}\n")
        
        board.display()
        if board.is_game_over():
            break
            
    # KẾT THÚC GAME
    result = board.is_game_over()
    if result == 'Draw':
        print("Bàn cờ đã đầy. Kết quả: HÒA!")
    else:
        print(f"Trò chơi kết thúc! Người chơi {result} đã chiến thắng!")

if __name__ == "__main__":
    play_game()
