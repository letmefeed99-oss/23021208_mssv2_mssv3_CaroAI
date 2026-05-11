import time

class AI:
    def __init__(self, player='O', max_depth=2):
        self.player = player # Máy tính mặc định là O
        self.opponent = 'X'  # Người chơi là X
        self.max_depth = max_depth # Giới hạn độ sâu tìm kiếm
        self.states_visited = 0

    def evaluate(self, board):
        # Hàm đánh giá trạng thái bàn cờ (cơ bản)
        score = 0
        if board.check_win(self.player): return 100000  # Máy có 4 quân: điểm rất lớn
        if board.check_win(self.opponent): return -100000 # Người có 4 quân: điểm rất nhỏ
        return score

    def minimax(self, board, depth, is_maximizing):
        self.states_visited += 1
        
        # Kiểm tra trạng thái kết thúc hoặc đạt độ sâu giới hạn
        result = board.is_game_over()
        if result == self.player: return 100000
        elif result == self.opponent: return -100000
        elif result == 'Draw': return 0
        
        if depth == 0:
            return self.evaluate(board)

        valid_moves = board.get_valid_moves()
        
        if is_maximizing:
            # Lượt của máy (MAX): Chọn giá trị lớn nhất
            best_score = -float('inf')
            for move in valid_moves:
                board.make_move(move[0], move[1], self.player)
                score = self.minimax(board, depth - 1, False)
                board.undo_move(move[0], move[1])
                best_score = max(score, best_score)
            return best_score
        else:
            # Lượt của người (MIN): Chọn giá trị nhỏ nhất
            best_score = float('inf')
            for move in valid_moves:
                board.make_move(move[0], move[1], self.opponent)
                score = self.minimax(board, depth - 1, True)
                board.undo_move(move[0], move[1])
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self, board):
        # Hàm tính toán và trả về nước đi tốt nhất
        self.states_visited = 0
        start_time = time.time()
        
        best_score = -float('inf')
        best_move = None
        
        valid_moves = board.get_valid_moves()
        
        for move in valid_moves:
            board.make_move(move[0], move[1], self.player)
            score = self.minimax(board, self.max_depth - 1, False)
            board.undo_move(move[0], move[1])
            
            if score > best_score:
                best_score = score
                best_move = move
                
        execution_time = time.time() - start_time
        
        # Ghi nhận các thông số theo yêu cầu của đề bài
        print(f"[Log AI] Độ sâu: {self.max_depth} | Số trạng thái đã xét: {self.states_visited} | Thời gian chạy: {execution_time:.4f}s")
        if best_move:
            print(f"[Log AI] Giá trị đánh giá cho nước đi {best_move} là: {best_score}")
        
        return best_move, best_score
