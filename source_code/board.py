class Board:
    def __init__(self, size=9):
        # Cài đặt bàn cờ kích thước tối thiểu 9x9
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]

    def display(self):
        print("  " + " ".join([str(i) for i in range(self.size)]))
        for r in range(self.size):
            print(f"{r} " + " ".join(self.grid[r]))
        print()

    def get_valid_moves(self):
        moves = []
        has_pieces = False
        
        # Kiểm tra xem bàn cờ đã có quân nào chưa
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != '.':
                    has_pieces = True
                    break
            if has_pieces: break

        # Nếu bàn cờ trống, ưu tiên đánh vào giữa bàn cờ
        if not has_pieces:
            return [(self.size // 2, self.size // 2)]

        # Nếu đã có quân, chỉ sinh các nước đi ở ô trống sát cạnh các quân đã đánh (bán kính 1 ô)
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == '.':
                    is_near = False
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.size and 0 <= nc < self.size:
                                if self.grid[nr][nc] != '.':
                                    is_near = True
                                    break
                        if is_near: break
                    
                    if is_near:
                        moves.append((r, c))
        return moves

    def make_move(self, r, c, player):
        if 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == '.':
            self.grid[r][c] = player
            return True
        return False

    def undo_move(self, r, c):
        # Rất quan trọng cho thuật toán đệ quy Minimax
        self.grid[r][c] = '.'

    def check_win(self, player):
        # Kiểm tra 4 quân liên tiếp (ngang, dọc, chéo), không xét chặn 2 đầu
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == player:
                    for dr, dc in directions:
                        count = 1
                        for i in range(1, 4):
                            nr, nc = r + dr * i, c + dc * i
                            if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == player:
                                count += 1
                            else:
                                break
                        if count >= 4:
                            return True
        return False

    def is_game_over(self):
        # Trạng thái kết thúc: X thắng, O thắng hoặc Hòa
        if self.check_win('X'): return 'X'
        if self.check_win('O'): return 'O'
        if len(self.get_valid_moves()) == 0: return 'Draw'
        return None
