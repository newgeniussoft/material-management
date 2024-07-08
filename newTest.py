import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton

class GridView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # Creating buttons in a 3x3 grid
        positions = [(i, j) for i in range(3) for j in range(3)]
        for pos in positions:
            button = QPushButton(f'Button {pos[0]},{pos[1]}', self)
            grid.addWidget(button, *pos)

        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Grid View Example')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    grid_view = GridView()
    sys.exit(app.exec_())
