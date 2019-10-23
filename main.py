import sys
from functools import partial
from random import random

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QLabel, QTableWidget,
                             QTableWidgetItem)

EXPERT_AMOUNT = 10
RISK_TYPES = ('tech', 'money', 'plan', 'manage')

class RiskDecreasing:
    riskDecreasingEvents = (
        "попереднє навчання членів проектного колективу",
        "узгодження детального переліку вимог до ПЗ із замовником",
        "внесення узгодженого переліку вимог до ПЗ замовника в договір",
        "точне слідування вимогам замовника з узгодженого переліку вимог до ПЗ",
        "попередні дослідження ринку",
        "експертна оцінка програмного проекту досвідченим стороннім консультантом",
        "консультації досвідченого стороннього консультанта",
        "тренінг з вивчення необхідних інструментів розроблення ПЗ",
        "укладання договору страхування",
        "використання \"шаблонних\" рішень з вдалих попередніх проектів при управлінні програмним проектом",
        "підготовка документів, які показують важливість даного проекту для досягнення фінансових цілей компанії-розробника",
        "реорганізація роботи проектного колективу так, щоб обов'язки та робота членів колективу перекривали один одного",
        "придбання (замовлення) частини компонент розроблюваного ПЗ",
        "заміна потенційно дефектних компонент розроблюваного ПЗ придбаними компонентами, які гарантують якість виконання роботи",
        "придбання більш продуктивної бази даних",
        "використання генератора програмного коду",
        "реорганізація роботи проектного колективу залежно від рівня труднощів виконання завдань та професійних рівнів розробників",
        "повторне використання придатних компонент ПЗ, які були розроблені для інших програмних проектів",
        "аналіз доцільності розроблення даного ПЗ"
    )

class RiskEvents:
    def __init__(self):
        self.dict = {
                    "tech": (
                                "Затримки у постачанні обладнання, необхідного для підтримки процесу розроблення ПЗ",
                                "Затримки у постачанні інструментальних засобів, необхідних для підтримки процесу розроблення ПЗ",
                                "Небажання команди виконавців ПЗ використовувати інструментальні засоби для підтримки процесу розроблення ПЗ",
                                "Відмова команди виконавців від CASE-засобів розроблення ПЗ",
                                "Формування запитів на більш потужні інструментальні засоби розроблення ПЗ",
                                "Недостатня продуктивність баз(и) даних для підтримки процесу розроблення ПЗ",
                                "Програмні компоненти, які використовують повторно в ПЗ, мають дефекти та обмежені функціональні можливості",
                                "Неефективність програмного коду, згенерованого CASE-засобами розроблення ПЗ",
                                "Hеможливість інтеграції CASE-засобів з іншими інструментальними засобами для підтримки процесу розроблення ПЗ",
                                "Швидкість виявлення дефектів у програмному коді є нижчою від раніше запланованих термінів",
                                "Поява дефектних системних компонент, які використовують для розроблення ПЗ"
                            ),
                    "money": (
                                "Hедооцінювання витрат на реалізацію програмного проекту (надмірно низька вартість)",
                                "Переоцінювання витрат на реалізацію програмного проекту (надмірно висока вартість)",
                                "Фінансові ускладнення у компанії-замовника ПЗ",
                                "Фінансові ускладнення у компанії-розробника ПЗ",
                                "Збільшення бюджету програмного проекта з ініціативи компанії-розробника ПЗ під час його реалізації",
                                "Зменшення бюджету програмного проекта з ініціативи компанії-замовника ПЗ під час його реалізації",
                                "Висока вартість виконання повторних робіт, необхідних для зміни вимог до ПЗ",
                                "Pеорганізація структурних підрозділів у компанії-замовника ПЗ",
                                "Pеорганізація команди виконавців у компанії-розробника ПЗ",
                            ),
                    "plan": (
                                "Зміни графіка виконання робіт з боку замовника чи виконавця",
                                "Порушення графіка виконання робіт у компанії-розробника ПЗ",
                                "Потреба зміни користувацьких вимог до ПЗ з боку компанії-замовника ПЗ",
                                "Потреба зміни функціональних вимог до ПЗ з боку компанії-розробника ПЗ",
                                "Потреба виконання великої кількості повторних робіт, необхідних для зміни вимог до ПЗ",
                                "Hедооцінювання тривалості етапів реалізації програмного проекту з боку компанії-розробника ПЗ",
                                "Переоцінювання тривалості етапів реалізації програмного проекту",
                                "Остаточний розмір ПЗ перевищує заплановані його характеристики",
                                "Остаточний розмір ПЗ значно менший за планові його характеристики",
                                "Поява на ринку аналогічного ПЗ до виходу замовленого",
                                "Поява на ринку більш конкурентоздатного ПЗ",
                            ),
                    "manage":(
                                "Hизький моральний стан персоналу команди виконавців ПЗ",
                                "Hизька взаємодія між членами команди виконавців ПЗ",
                                "Пасивність керівника (менеджера) програмного проекту",
                                "Недостатня компетентність керівника (менеджера) програмного проекту",
                                "Незадоволеність замовника результатами етапів реалізації програмного проекту",
                                "Hедостатня кількість фахівців у команді виконавців ПЗ з необхідним професійним рівнем",
                                "Xвороба провідного виконавця в найкритичніший момент розроблення ПЗ",
                                "Oдночасна хвороба декількох виконавців підчас розроблення ПЗ",
                                "Hеможливість організації необхідного навчання персоналу команди виконавців ПЗ",
                                "Hедооцінювання необхідної кількості розробників (підрядників і субпідрядників) на етапах життєвого циклу розроблення ПЗ",
                                "Переоцінювання необхідної кількості розробників (підрядників і субпідрядників) на етапах життєвого циклу розроблення ПЗ",
                                "Hадмірне документування результатів на етапах реалізації програмного проекту",
                                "Hедостатнє документування результатів на етапах реалізації програмного проекту",
                                "Hереалістичне прогнозування результатів на етапах реалізації програмного проекту",
                                "Hедостатній професійний рівень представників від компанії-замовника ПЗ",
                                "Зміна пріоритетів у процесі управління програмним проектом",
                            )
    }
        self.vrer = []
        self.vrer2 = []
        self.loss = []
        self.loss2 = []
        self.expert_estimating = []
        self.expert_monitoring = []

    @property
    def list(self):
        return self.dict['tech'] + self.dict['money'] + self.dict['plan'] + self.dict['manage'] 

    @property
    def min_vrer(self):
        return min(self.vrer)

    @property
    def max_vrer(self):
        return max(self.vrer)
    
    @property
    def min_vrer2(self):
        return min(self.vrer2)

    @property
    def max_vrer2(self):
        return max(self.vrer2)

    @property
    def vrer_step(self):
        return round((self.max_vrer - self.min_vrer) / 3, 2)
    @property
    def low_priority_limit(self):
        return round(self.min_vrer + self.vrer_step, 2)
    @property
    def middle_priority_limit(self):
        return round(self.max_vrer - self.vrer_step, 2)
    
    @property
    def vrer_step2(self):
        return round((self.max_vrer2 - self.min_vrer2) / 3, 2)
    @property
    def low_priority_limit2(self):
        return round(self.min_vrer2 + self.vrer_step2, 2)
    @property
    def middle_priority_limit2(self):
        return round(self.max_vrer2 - self.vrer_step2, 2)

class RiskSources:
    def __init__(self):
        self.dict = {
                    "tech": (
                                "Наявні нереалістичні чи неоціненні функціональні характеристики ПЗ",
                                "Наявні нереалістичні чи неоціненні характеристики якості ПЗ",
                                "Наявні нереалістичні чи неоціненні характеристики надійності ПЗ",
                                "Наявні нереалістичні рекомендації щодо майбутньої застосовності ПЗ",
                                "Наявні нереалістичні характеристики часової продуктивності ПЗ",
                                "Наявні нереалістичні рекомендації щодо майбутньої супроводжуваності ПЗ",
                                "Наявні нереалістичні пропозиції щодо повторного використання ПЗ"
                            ),
                    "money": (
                                "Наявні обмеження щодо сумарного бюджету на реалізацію ПЗ",
                                "Вказана недоступна вартість реалізації програмного проекту",
                                "Присутній низький ступінь реалізму при оцінюванні витрат на ПЗ"
                            ),
                    "plan": (
                                "Наявні нереалістичні властивості та можливості гнучкості внесення змін до планів життєвого циклу розроблення ПЗ",
                                "Відсутні нереалістичні можливості порушення встановлених термінів реалізації етапів життєвого циклу розроблення ПЗ",
                                "Присутній низький ступінь реалізму при встановленні планів і етапів життєвого циклу розроблення ПЗ"
                            ),
                    "manage":(
                                "Наявні нереалістичні стратегії реалізації програмного проекту",
                                "Наявні нереалістичні методики планування проекту розроблення ПЗ",
                                "Наявні нереалістичні методики оцінювання програмного проекту",
                                "Наявне неналежне документування етапів реалізації ПЗ",
                                "Наявні нереалістичні методики прогнозування результатів реалізації ПЗ",
                            )
    }

    @property
    def list(self):
        return self.dict['tech'] + self.dict['money'] + self.dict['plan'] + self.dict['manage'] 

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.init_Data()
        self.init_UI()
        
    def init_Data(self):
        self.risk_events = RiskEvents()
        self.risk_sources = RiskSources()

    def init_UI(self):
        self.UI_init_tables()
        self.UI_init_button_handlers()
        self.UI_set_risk_solution_comboboxes()

    def UI_init_tables(self):
        self.risk_analysys_table.setColumnWidth(0, 370)
        self.risk_monitoring_table.setColumnWidth(0, 370)

        self.risk_priority_table.setColumnWidth(0, 370)
        self.risk_analysys_table.setColumnWidth(11, 200)
        self.risk_priority_table.setColumnWidth(1, 20)
        self.risk_priority_table.setColumnWidth(2, 95)
        self.risk_priority_table.setColumnWidth(3, 35)
        self.risk_priority_table.setColumnWidth(4, 80)

        self.risk_priority_table2.setColumnWidth(0, 370)
        self.risk_priority_table2.setColumnWidth(1, 20)
        self.risk_priority_table2.setColumnWidth(2, 95)
        self.risk_priority_table2.setColumnWidth(3, 35)
        self.risk_priority_table2.setColumnWidth(4, 80)
        for i in range(1, EXPERT_AMOUNT + 1):
            self.risk_analysys_table.setColumnWidth(i, 20)
            self.risk_monitoring_table.setColumnWidth(i, 20)
        
        for i in range(len(self.risk_events.list)):
            previous_text = self.risk_analysys_table.item(i, 0).text()
            self.risk_analysys_table.setItem(i , 0, QTableWidgetItem(previous_text + ', ' + self.risk_events.list[i]))
            self.risk_monitoring_table.setItem(i, 0, QTableWidgetItem(previous_text + ', ' + self.risk_events.list[i]))
            self.risk_priority_table.setItem(i, 0, QTableWidgetItem(previous_text + ', ' + self.risk_events.list[i]))
            self.risk_priority_table2.setItem(i, 0, QTableWidgetItem(previous_text + ', ' + self.risk_events.list[i]))
            self.risk_solution_table.setItem(i, 0, QTableWidgetItem(previous_text + ', ' + self.risk_events.list[i]))

    def UI_init_button_handlers(self):
        self.calculateRiskProbability.clicked.connect(partial(self.risk_probability, "source"))
        self.calculateEventProbability.clicked.connect(partial(self.risk_probability, "event"))
        
        # risk analysys page
        self.generate_marks_button.clicked.connect(partial(self.generate_expert_risk_estimates, "analysys"))
        self.event_analysys_button.clicked.connect(partial(self.event_analysys, "analysys"))
        self.group_result_button.clicked.connect(partial(self.group_priority_result, "analysys"))
        
        # risk monitoring page
        self.generate_marks_button2.clicked.connect(partial(self.generate_expert_risk_estimates, "monitoring"))
        self.event_analysys_button2.clicked.connect(partial(self.event_analysys, "monitoring"))
        self.group_result_button2.clicked.connect(partial(self.group_priority_result, "monitoring")) 
        
        # calculate risk page
        self.generate_loss_button.clicked.connect(partial(self.generate_loss, "analysys"))
        self.calculate_vrer_button.clicked.connect(partial(self.calculate_vrer, "analysys"))
        self.risk_priority_button.clicked.connect(partial(self.risk_priority, "analysys"))
        
        # calculate monitoring risk page
        self.generate_loss_button2.clicked.connect(partial(self.generate_loss, "monitoring"))
        self.calculate_evrer_button.clicked.connect(partial(self.calculate_vrer, "monitoring"))
        self.risk_priority_button2.clicked.connect(partial(self.risk_priority, "monitoring"))

        # risk solution page
        self.show_risk_decrease_table_button.clicked.connect(self.UI_solution_box_to_table)

        self.risk_source_back_button.clicked.connect(self.UI_risk_source_back)
        self.risk_event_back_button.clicked.connect(self.UI_risk_event_back)
        self.risk_analysys_back_button.clicked.connect(self.UI_risk_analysys_back)
        self.risk_analysys_back_button2.clicked.connect(self.UI_risk_analysys_back2)
        self.risk_solution_back_button.clicked.connect(self.UI_risk_solution_back)

    def UI_risk_source_back(self):
        self.riskSourcesWidget.setCurrentIndex(1)
    
    def UI_risk_event_back(self):
        self.riskEventsWidget.setCurrentIndex(1)
    
    def UI_risk_analysys_back(self):
        self.analysysWidget.setCurrentIndex(0)
    
    def UI_risk_analysys_back2(self):
        self.monitoringWidget.setCurrentIndex(0)

    def UI_risk_solution_back(self):
        self.riskSolutionWidget.setCurrentIndex(0)

    def UI_solution_box_to_table(self):
        for i in range(len(self.risk_events.list)):
            combobox = self.findChild(QComboBox, f"riskSolutionBox{i+1}")
            choosen_solution = combobox.currentText()
            self.risk_solution_table.setItem(i, 1, QTableWidgetItem(choosen_solution))
        self.riskSolutionWidget.setCurrentIndex(1)

    def UI_init_vrer_page(self, type_):
        if type_ == "analysys":
            min_vrer_box = self.min_vrer_box
            max_vrer_box = self.max_vrer_box

            min_vrer = self.risk_events.min_vrer
            max_vrer = self.risk_events.max_vrer

            low_interval_box = self.low_interval_box
            middle_interval_box = self.middle_interval_box
            high_interval_box = self.high_interval_box

            low_priority_limit = self.risk_events.low_priority_limit
            middle_priority_limit = self.risk_events.middle_priority_limit

        elif type_ == "monitoring":
            min_vrer_box = self.min_evrer_box
            max_vrer_box = self.max_evrer_box

            min_vrer = self.risk_events.min_vrer2
            max_vrer = self.risk_events.max_vrer2

            low_interval_box = self.low_interval_box2
            middle_interval_box = self.middle_interval_box2
            high_interval_box = self.high_interval_box2

            low_priority_limit = self.risk_events.low_priority_limit2
            middle_priority_limit = self.risk_events.middle_priority_limit2

        min_vrer_box.setText(str(min_vrer))
        max_vrer_box.setText(str(max_vrer))

        low_interval_box.setText(f"[{min_vrer}; {low_priority_limit})")
        middle_interval_box.setText(f"[{low_priority_limit}; {middle_priority_limit})")
        high_interval_box.setText(f"[{low_priority_limit}; {max_vrer}]")

    def UI_group_priority(self, total_sum, result_label, result_status_label):
        result_label.setText(str(round(total_sum, 2)))

        result = "Ймовірність виникнення ризикової події є "
        if total_sum < 0.1:
            result += "дуже низькою"
        elif total_sum < 0.25:
            result += "низькою"
        elif total_sum < 0.5:
            result += "середньою"
        elif total_sum < 0.75:
            result += "високою"
        else:
            result += "дуже високою"
        
        result_status_label.setText(result)
        self.analysysWidget.setCurrentIndex(1)
        self.monitoringWidget.setCurrentIndex(1)

    def UI_write_table(self, table, col, row, value):
        table.setItem(col, row, QTableWidgetItem(str(value)))

    def UI_probabilities_to_table(self, type_, probabilities):
        table = self.findChild(QTableWidget, f"risk_{type_}_table")
        for index, risk_type in enumerate(RISK_TYPES):
            self.UI_write_table(table, 0, index, probabilities[risk_type])
        self.UI_write_table(table, 0, 4, sum(probabilities.values()))
    
    def UI_set_risk_page(self, type_):
        if type_ == "source":
            self.riskSourcesWidget.setCurrentIndex(0)
        elif type_ == "event":
            self.riskEventsWidget.setCurrentIndex(0)

    def UI_set_risk_solution_comboboxes(self):
        for i, v in enumerate(self.risk_events.list):
            combobox = self.findChild(QComboBox, f"riskSolutionBox{i+1}")
            combobox.addItems(RiskDecreasing.riskDecreasingEvents)
            label = self.findChild(QLabel, f"riskLabel{i+1}")
            label.setText(label.text() + ' ' + v)

    def generate_expert_risk_estimates(self, type_):
        if type_ == "analysys":
            table = self.risk_analysys_table
            correlation = 0
        elif type_ == "monitoring":
            table = self.risk_monitoring_table
            correlation = -0.15
            
        for i in range(len(self.risk_events.list)):
            for j in range(1, EXPERT_AMOUNT+1):
                table.setItem(i, j, QTableWidgetItem(str(round(random() + correlation, 2))))
    
    def generate_loss(self, type_):
        if type_ == "analysys":
            loss = self.risk_events.loss
            table = self.risk_priority_table
        elif type_ == "monitoring":
            loss = self.risk_events.loss2
            table = self.risk_priority_table2
        
        loss.clear()
        for i in range(len(self.risk_events.list)):
            value = round(random(), 2)
            loss.append(value)
            table.setItem(i, 2, QTableWidgetItem(str(value)))

    def risk_priority(self, type_):
        if type_ == "analysys":
            table = self.risk_priority_table
            vrer_list = self.risk_events.vrer
            low_priority_limit = self.risk_events.low_priority_limit
            middle_priority_limit = self.risk_events.middle_priority_limit
        elif type_ == "monitoring":
            table = self.risk_priority_table2
            vrer_list = self.risk_events.vrer2
            low_priority_limit = self.risk_events.low_priority_limit2
            middle_priority_limit = self.risk_events.middle_priority_limit2

        self.UI_init_vrer_page(type_)

        for i in range(len(self.risk_events.list)):
            if vrer_list[i] < low_priority_limit:
                priority = "НИЗЬКИЙ"
            elif vrer_list[i] < middle_priority_limit:
                priority = "СЕРЕДНІЙ"
            else:
                priority = "ВИСОКИЙ"

            table.setItem(i, 4, QTableWidgetItem(priority))

    def calculate_vrer(self, type_):
        if type_ == "analysys":
            table = self.risk_priority_table
            expert_marks = self.risk_events.expert_estimating
            loss = self.risk_events.loss
            vrer_list = self.risk_events.vrer
        elif type_ == "monitoring":
            table = self.risk_priority_table2
            expert_marks = self.risk_events.expert_monitoring
            loss = self.risk_events.loss2
            vrer_list = self.risk_events.vrer2

        vrer_list.clear()
        for i in range(len(self.risk_events.list)):
            vrer = round(expert_marks[i] * loss[i], 2)
            vrer_list.append(vrer)

            table.setItem(i, 3, QTableWidgetItem(str(vrer)))

    def event_analysys(self, type_):
        if type_ == "analysys":
            table = self.risk_analysys_table
            result_table = self.risk_priority_table
            expert_marks = self.risk_events.expert_estimating
        elif type_ == "monitoring":
            table = self.risk_monitoring_table
            result_table = self.risk_priority_table2
            expert_marks = self.risk_events.expert_monitoring

        expert_marks.clear()
        for i in range(len(self.risk_events.list)):
            row_sum = 0
            for j in range(1, EXPERT_AMOUNT+1):
                row_sum += float(table.item(i, j).text())
            expert_marks.append(round(row_sum / EXPERT_AMOUNT, 2))
            table.setItem(i, 11, QTableWidgetItem(str(round(row_sum / EXPERT_AMOUNT, 2))))
            result_table.setItem(i, 1, QTableWidgetItem(str(round(row_sum / EXPERT_AMOUNT, 2))))

    def calculate_group_risk(self, table, result_table, offset, group_size, row_index):
        group_estimates_sum = 0
        for i in range(offset + 1, offset + group_size + 1):
            event_estimates_sum = float(table.item(i-1, 11).text())
            group_estimates_sum += event_estimates_sum

        result_table.setItem(0, row_index, QTableWidgetItem(str(round(group_estimates_sum / len(self.risk_events.list), 2))))

        return group_estimates_sum / len(self.risk_events.list)

    def group_priority_result(self, type_):
        if type_ == "analysys":
            table = self.risk_analysys_table
            result_table = self.group_result_table
            result_label = self.total_result
            result_status_label = self.label_result
        elif type_ == "monitoring":
            table = self.risk_monitoring_table
            result_table = self.group_result_table2
            result_label = self.total_result2
            result_status_label = self.label_result2

        total_sum = 0
        offset = 0
        for row_index, risk_type in enumerate(RISK_TYPES):
            total_sum += self.calculate_group_risk(table, result_table, offset, len(self.risk_events.dict[risk_type]), row_index)
            offset += len(self.risk_events.dict[risk_type])
        
        self.UI_group_priority(total_sum, result_label, result_status_label)
        
    def calculate_checked_box(self, type_):
        risks = dict.fromkeys(RISK_TYPES, 0)
        for risk_type in RISK_TYPES:
            number = 1
            checkbox = self.findChild(QCheckBox, f"{risk_type}_{type_}{number}")
            while checkbox:
                if checkbox.isChecked():
                    risks[risk_type] += 1
                number += 1
                checkbox = self.findChild(QCheckBox, f"{risk_type}_{type_}{number}")
        return risks

    def calculate_probability(self, amount, risks):
        probabilities = dict.fromkeys(RISK_TYPES, 0)
        for risk_type in RISK_TYPES:
            probabilities[risk_type] = round((risks[risk_type] / amount) * 100, 2)
        return probabilities 
    
    def risk_probability(self, type_):
        if type_ == "source":
            risk_count = len(self.risk_sources.list)
        elif type_ == "event":
            risk_count = len(self.risk_events.list)

        risks = self.calculate_checked_box(type_)
        probabilities = self.calculate_probability(risk_count, risks)
        
        self.UI_probabilities_to_table(type_, probabilities)
        self.UI_set_risk_page(type_)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
