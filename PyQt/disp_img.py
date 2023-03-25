import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
import numpy as np;

# Example matrix representing a grayscale image
matrix = np.random.rand(400,400).round()
matrix = matrix.astype(int)
matrix = matrix.tolist()

class MatrixImageWindow(QWidget):
    def __init__(self, matrix):
        super().__init__()

        self.matrix = matrix
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        image_label = QLabel()
        image_label.setPixmap(self.matrix_to_qpixmap(self.matrix))
        layout.addWidget(image_label)

        self.setLayout(layout)
        self.setWindowTitle('Matrix as Image')
        self.show()

    def matrix_to_qpixmap(self, matrix):
        height, width = len(matrix), len(matrix[0])
        image = QImage(width, height, QImage.Format_Grayscale8)

        for y in range(height):
            for x in range(width):
                gray_value = matrix[y][x]
                image.setPixel(x, y, gray_value)

        return QPixmap.fromImage(image)

def main():
    app = QApplication(sys.argv)
    matrix_image_window = MatrixImageWindow(matrix)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
