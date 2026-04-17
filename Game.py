import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGridLayout, 
                             QPushButton, QWidget, QLabel, QMessageBox)
from PyQt6.QtCore import Qt

# 游戏配置
ROW = 8
COL = 8
TYPE_COUNT = 5
MAX_STEP = 30   # 总步数
BASE_SCORE = 10 # 每消一个分数

# 开心消消乐小动物emoji
ICONS = ["🐱", "🐰", "🐻", "🐼", "🦊"]
COLORS = [
    "#FFE8E8",
    "#E8F4FF",
    "#F0FFF0",
    "#FFF8E8",
    "#F8E8FF"
]

class EliminateGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("开心消消乐")
        self.setFixedSize(520, 580)

        # 游戏数据
        self.board = [[0]*COL for _ in range(ROW)]
        self.selected = None
        self.btns = [[None]*COL for _ in range(ROW)]
        self.score = 0
        self.step = MAX_STEP

        self.init_ui()
        self.init_board()
        self.update_status()

    def init_ui(self):
        # 顶部状态栏
        self.score_label = QLabel(f"得分：{self.score}")
        self.step_label = QLabel(f"剩余步数：{self.step}")
        self.score_label.setStyleSheet("font-size:16px; padding:5px;")
        self.step_label.setStyleSheet("font-size:16px; padding:5px;")

        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        from PyQt6.QtWidgets import QVBoxLayout
        main_layout = QVBoxLayout(central_widget)

        # 顶部信息行
        info_layout = QGridLayout()
        info_layout.addWidget(self.score_label, 0, 0)
        info_layout.addWidget(self.step_label, 0, 1)
        main_layout.addLayout(info_layout)

        # 游戏棋盘
        grid = QGridLayout()
        grid.setSpacing(3)
        main_layout.addLayout(grid)

        for r in range(ROW):
            for c in range(COL):
                btn = QPushButton(ICONS[0])
                btn.setFixedSize(55, 55)
                btn.setStyleSheet("font-size:22px; border-radius:8px;")
                btn.clicked.connect(lambda checked, row=r, col=c: self.click_cell(row, col))
                self.btns[r][c] = btn
                grid.addWidget(btn, r, c)

    def init_board(self):
        for r in range(ROW):
            for c in range(COL):
                self.board[r][c] = random.randint(0, TYPE_COUNT-1)
        self.update_ui()

    def update_ui(self):
        for r in range(ROW):
            for c in range(COL):
                idx = self.board[r][c]
                icon = ICONS[idx]
                color = COLORS[idx]
                self.btns[r][c].setText(icon)
                self.btns[r][c].setStyleSheet(f"""
                    font-size:22px;
                    background-color:{color};
                    border-radius:8px;
                """)

    def update_status(self):
        self.score_label.setText(f"得分：{self.score}")
        self.step_label.setText(f"剩余步数：{self.step}")

    def click_cell(self, r, c):
        if self.step <= 0:
            self.game_over()
            return

        if self.selected is None:
            # 选中第一个
            self.selected = (r, c)
            self.btns[r][c].setStyleSheet("""
                font-size:22px;
                border:3px solid #ff4444;
                border-radius:8px;
            """)
        else:
            r1, c1 = self.selected
            # 判断是否上下左右相邻
            if abs(r1 - r) + abs(c1 - c) == 1:
                # 交换
                self.swap_cell(r1, c1, r, c)
                # 能消除才有效，消耗步数
                if self.check_eliminate():
                    self.step -= 1
                    self.auto_drop_fill()
                else:
                    # 不能消除，换回原位
                    self.swap_cell(r1, c1, r, c)

            self.selected = None
            self.update_ui()
            self.update_status()

            # 步数用完结束游戏
            if self.step <= 0:
                self.game_over()

    def swap_cell(self, r1, c1, r2, c2):
        self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]

    def check_eliminate(self):
        eliminate = set()
        # 横向三连
        for r in range(ROW):
            for c in range(COL-2):
                t = self.board[r][c]
                if t == -1:
                    continue
                if t == self.board[r][c+1] == self.board[r][c+2]:
                    eliminate.update({(r,c), (r,c+1), (r,c+2)})
        # 纵向三连
        for c in range(COL):
            for r in range(ROW-2):
                t = self.board[r][c]
                if t == -1:
                    continue
                if t == self.board[r+1][c] == self.board[r+2][c]:
                    eliminate.update({(r,c), (r+1,c), (r+2,c)})

        # 加分 + 标记消除
        if eliminate:
            self.score += len(eliminate) * BASE_SCORE
            for r,c in eliminate:
                self.board[r][c] = -1
        return len(eliminate) > 0

    def auto_drop_fill(self):
        # 每列下落
        for c in range(COL):
            col_data = []
            for r in range(ROW-1, -1, -1):
                if self.board[r][c] != -1:
                    col_data.append(self.board[r][c])
            # 顶部补新
            fill_num = ROW - len(col_data)
            for _ in range(fill_num):
                col_data.append(random.randint(0, TYPE_COUNT-1))
            # 写回棋盘
            for r in range(ROW-1, -1, -1):
                self.board[r][c] = col_data[ROW-1 - r]

        self.update_ui()
        self.update_status()

        # 连锁消除
        if self.check_eliminate():
            self.auto_drop_fill()

    def game_over(self):
        QMessageBox.information(self, "游戏结束", 
                                f"步数用完啦！\n最终得分：{self.score}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = EliminateGame()
    win.show()
    sys.exit(app.exec())