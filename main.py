from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
import sys

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("lab3/design.ui", self)

        self.init_UI()
        
    def init_UI(self):
        self.views.setCurrentIndex(0)
        output.trigger.connect(self.print_to_output)
        self.start_button.clicked.connect(self.start_game)
        
    @pyqtSlot(str)
    def print_to_output(self, text):
        self.register_result_label.setText(text)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()