from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QCheckBox
import sys

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.init_UI()
        self.init_Data()
        
    def init_UI(self):
        #self.views.setCurrentIndex(0)
        #output.trigger.connect(self.print_to_output)
        #self.riskSourcesWidget.calculateRiskProbability.clicked.connect(self.risk_probability)

        self.calculateRiskProbability.clicked.connect(self.risk_probability)

    def init_Data(self):
        self.risk_types = ('tech', 'money', 'plan', 'manage')
        self.risks = dict.fromkeys(self.risk_types, 0)
        self.risks_probability = dict.fromkeys(self.risk_types, 0)
        

    def calculate_risks(self):
        for risk_type in self.risk_types:
            number = 1
            checkbox = self.findChild(QCheckBox, f"{risk_type}_risk{number}")
            while checkbox:
                if checkbox.isChecked():
                    self.risks[risk_type] += 1
                number += 1
                checkbox = self.findChild(QCheckBox, f"{risk_type}_risk{number}")

    def calculate_probability(self):
        for risk_type in self.risk_types:
            self.risks_probability[risk_type] = (self.risks[risk_type] / 18) * 100
    
    def write_risks_table(self):
        for index, risk_type in enumerate(self.risk_types):
            self.risk_prob_table.setItem(0, index, QTableWidgetItem(str(round(self.risks_probability[risk_type], 2))))

    def risk_probability(self):
        self.calculate_risks()
        self.calculate_probability()
        self.write_risks_table()
        self.risk_prob_table.setItem(0, 4, QTableWidgetItem(str(round(sum(self.risks_probability.values()), 2))))
        self.riskSourcesWidget.setCurrentIndex(0)

    @pyqtSlot(str)
    def print_to_output(self, text):
        self.register_result_label.setText(text)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())