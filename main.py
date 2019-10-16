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
        self.calculateRiskProbability.clicked.connect(self.risk_probability)
        self.calculateEventProbability.clicked.connect(self.event_probability)
        self.actionMain_menu.triggered.connect(self.back)
    
    def back(self):
        self.riskEventsWidget.setCurrentIndex(1)
        self.riskSourcesWidget.setCurrentIndex(1)
        
    def init_Data(self):
        self.risk_types = ('tech', 'money', 'plan', 'manage')
        self.risks = dict.fromkeys(self.risk_types, 0)
        self.risks_probability = dict.fromkeys(self.risk_types, 0)
        
    def calculate(self, type_):
        for risk_type in self.risk_types:
            number = 1
            checkbox = self.findChild(QCheckBox, f"{risk_type}_{type_}{number}")
            while checkbox:
                if checkbox.isChecked():
                    self.risks[risk_type] += 1
                number += 1
                checkbox = self.findChild(QCheckBox, f"{risk_type}_{type_}{number}")

    def calculate_probability(self, amount):
        for risk_type in self.risk_types:
            self.risks_probability[risk_type] = (self.risks[risk_type] / amount) * 100
    
    def write_risks_table(self, table):
        for index, risk_type in enumerate(self.risk_types):
            table.setItem(0, index, QTableWidgetItem(str(round(self.risks_probability[risk_type], 2))))

    def risk_probability(self):
        self.calculate('risk')
        self.calculate_probability(18)
        table = self.risk_prob_table
        self.write_risks_table(table)
        table.setItem(0, 4, QTableWidgetItem(str(round(sum(self.risks_probability.values()), 2))))
        self.init_Data()
        self.riskSourcesWidget.setCurrentIndex(0)

    def event_probability(self):
        self.calculate('event')
        self.calculate_probability(46)
        table = self.event_prob_table
        self.write_risks_table(table)
        table.setItem(0, 4, QTableWidgetItem(str(round(sum(self.risks_probability.values()), 2))))
        self.init_Data()
        self.riskEventsWidget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())