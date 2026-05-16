class Board:
    def __init__(self, size=9):
        self.size = size
        self.grid = [['.' for _ in range(size)] for _ in range(size)]

    def display(self):
        print("   " + " ".join(f"{i:2}" for i in range(self.size)))
        for r in range(self.size):
            row_str = " ".join(f"{cell:>2}" for cell in self.grid[r])
            print(f"{r:2} {row_str}")
        print()

    def get_valid_moves(self, radius=2):
        """
        Sinh nước đi hợp lệ: chỉ các ô trống trong bán kính `radius`
        xung quanh các quân đã đánh. Bán kính 2 giúp AI nhìn xa hơn.
        """
        if not self._has_pieces():
            return [(self.size // 2, self.size // 2)]

        candidates = set()
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != '.':
                    for dr in range(-radius, radius + 1):
                        for dc in range(-radius, radius + 1):
                            nr, nc = r + dr, c + dc
                            if (0 <= nr < self.size and 0 <= nc < self.size
                                    and self.grid[nr][nc] == '.'):
                                candidates.add((nr, nc))
        return list(candidates)

    def _has_pieces(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != '.':
                    return True
        return False

    def is_full(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == '.':
                    return False
        return True

    def make_move(self, r, c, player):
        if 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == '.':
            self.grid[r][c] = player
            return True
        return False

    def undo_move(self, r, c):
        self.grid[r][c] = '.'

    def check_win(self, player):
        """Kiểm tra 4 quân liên tiếp theo 4 hướng."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == player:
                    for dr, dc in directions:
                        count = 1
                        for i in range(1, 4):
                            nr, nc = r + dr * i, c + dc * i
                            if (0 <= nr < self.size and 0 <= nc < self.size
                                    and self.grid[nr][nc] == player):
                                count += 1
                            else:
                                break
                        if count >= 4:
                            return True
        return False

    def is_game_over(self):
        """
        Trả về: 'X' | 'O' | 'Draw' | None
        BUG FIX: dùng is_full() thay vì get_valid_moves() để kiểm tra hòa.
        """
        if self.check_win('X'):
            return 'X'
        if self.check_win('O'):
            return 'O'
        if self.is_full():
            return 'Draw'
        return None
