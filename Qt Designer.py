# 导入需要的模块
from PyQt6.QtWidgets import QApplication, QWidget
import sys

# 1. 创建APP实例
app = QApplication(sys.argv)

# 2. 创建主窗口
win = QWidget()
win.setWindowTitle("我的第一个PyQt6窗口")  # 窗口标题
win.resize(400,300)# 窗口大小

# 3. 显示窗口
win.show()

# 4. 循环运行窗口
sys.exit(app.exec())