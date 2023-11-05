import sys
import io
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem


class CraftTable(QWidget):
    def __init__(self):
        super().__init__()
        self.search_ansver = None
        uic.loadUi("craft.ui", self)
        self.setWindowTitle("Craft")
        self.executor()

    def executor(self):
        self.pb.clicked.connect(self.create_ansver)

    def search_name(self):
        ansver = f"(name LIKE '%{self.name.text()}%')"
        return ansver

    def ansver(self):
        self.con = sqlite3.connect('crafting.db')
        cur = self.con.cursor()
        result = cur.execute(self.search_ansver).fetchall()
        if len(result) != 0:
            self.tw.setColumnCount(len(result[0]))
            self.tw.setRowCount(0)
            for i, row in enumerate(result):
                self.tw.setRowCount(self.tw.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tw.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tw.resizeColumnsToContents()
            self.con.close()

    def nums_items(self):
        # смотрим сколько ввели предметов в создании
        num = int(self.nums_craft.text())
        # с помощью 'LIKE %, %' будем проверять сколько предметов в создании
        if num == 1:
            ansver = f"(craft NOT LIKE '%, %')"
        else:
            num_item1 = "%".join(num * [", "])
            num_item2 = "%".join((num - 1) * [", "])
            ansver = f"(craft LIKE '%{num_item2}%') AND (craft NOT LIKE '%{num_item1}%')"
        return ansver

    def create_ansver(self):
        self.search_ansver = ["""SELECT * FROM Сraft"""]
        # Поиск по названию
        if self.name.text() != "":
            line = self.search_name()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по количеству уникальных предметов
        if int(self.nums_craft.text()) > 0:
            line = self.nums_items()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по названию предметов в создании
        if self.plainTextEdit.toPlainText() != "":
            line = self.items_in_creation()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по размещаемости
        if self.radioButton.isChecked() or self.radioButton_2.isChecked():
            line = self.placability()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по станции создания
        if self.comboBox.currentText() != "Любая":
            line = self.creation_station()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по тегам
        if (self.teg1.currentText() != "Ничего" or
                self.teg2.currentText() != "Ничего" or
                self.teg3.currentText() != "Ничего"):
            line = self.search_tegs()
            if line != "":
                self.search_ansver.append(line)

        # Создание финального SQL запроса search_tegs
        if len(self.search_ansver) == 1:
            self.search_ansver = "SELECT * FROM Сraft"
            self.ansver()
        elif len(self.search_ansver) == 2:
            self.search_ansver = self.search_ansver[0] + " WHERE " + self.search_ansver[-1]
            self.ansver()
        elif len(self.search_ansver) > 2:
            self.search_ansver = self.search_ansver[0] + " WHERE " + " AND ".join(self.search_ansver[1::])
            self.ansver()

    def items_in_creation(self):
        if len(self.plainTextEdit.toPlainText().split(";")) == 0:
            ansver = f"(craft LIKE '%{self.plainTextEdit.toPlainText()}%')"
        else:
            search = "%".join(self.plainTextEdit.toPlainText().split(";"))
            ansver = f"(craft LIKE '%{search}%')"
        return ansver

    def placability(self):
        if self.radioButton.isChecked():
            ansver = f"(placability LIKE '%Можно%')"
        else:
            ansver = f"(placability LIKE '%Нельзя%')"
        return ansver

    def creation_station(self):
        ansver = f"(machine LIKE '%{self.comboBox.currentText()}%')"
        return ansver

    def search_tegs(self):
        tegs1 = []
        tegs2 = [self.teg1.currentText(), self.teg2.currentText(), self.teg3.currentText()]
        for i in range(3):
            if tegs2[i] != "Ничего":
                tegs1.append(tegs2[i])
        if self.b_or.isChecked():
            ansver = self.or_and(True, tegs1)
        else:
            ansver = self.or_and(False, tegs1)
        return ansver

    def or_and(self, or_or_and, tegs):
        flag = " AND "
        if not or_or_and:
            flag = " OR "
        ansver = []
        for i in tegs:
            ansver.append(f"tags LIKE '%{i}%'")
        ansver = f"{flag}".join(ansver)
        return "(" + ansver + ")"


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.search_ansver = None
        uic.loadUi("choice.ui", self)
        self.setWindowTitle("Menu")


class MobTable(QWidget):
    def __init__(self):
        super().__init__()
        self.search_ansver = None
        uic.loadUi("mobs.ui", self)
        self.setWindowTitle("Craft")
        self.executor()

    def executor(self):
        self.choice.clicked.connect(self.create_ansver)

    def search_name(self):
        ansver = f"(name LIKE '%{self.name.text()}%')"
        return ansver

    def ansver(self):
        self.con = sqlite3.connect('crafting.db')
        cur = self.con.cursor()
        result = cur.execute(self.search_ansver).fetchall()
        if len(result) != 0:
            self.tableWidget.setColumnCount(len(result[0]))
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(result):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
            self.con.close()

    def nums_items(self):
        # смотрим сколько ввели предметов в создании
        num = int(self.spinBox.text())
        # с помощью 'LIKE %, %' будем проверять сколько предметов в создании
        if num == 1:
            ansver = f"(drops NOT LIKE '%, %')"
        else:
            num_item1 = "%".join(num * [", "])
            num_item2 = "%".join((num - 1) * [", "])
            ansver = f"(drops LIKE '%{num_item2}%') AND (drops NOT LIKE '%{num_item1}%')"
        return ansver

    def create_ansver(self):
        self.search_ansver = ["""SELECT * FROM mobs"""]
        # Поиск по названию
        if self.name.text() != "":
            line = self.search_name()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по количеству уникальных предметов
        if int(self.spinBox.text()) > 0:
            line = self.nums_items()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по названию предметов в создании
        if self.uniqueDrop.text() != "":
            line = self.items_in_creation()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по агресивности
        if self.friendliness.currentText() != "любая":
            line = self.friendlines()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по количеству выподаемой валюты
        if int(self.money_num.text()) > 0:
            line = self.money_nums()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по местанохождению
        if (self.location1.currentText() != "-" or
                self.location2.currentText() != "-" or
                self.location3.currentText() != "-"):
            line = self.search_location()
            if line != "":
                self.search_ansver.append(line)

        # Поиск по золотой вариации
        if self.golden.currentText() != "любая":
            line = self.golden1()
            if line != "":
                self.search_ansver.append(line)

        # Создание финального SQL запроса search_tegs
        if len(self.search_ansver) == 1:
            self.search_ansver = "SELECT * FROM mobs"
            self.ansver()
        elif len(self.search_ansver) == 2:
            self.search_ansver = self.search_ansver[0] + " WHERE " + self.search_ansver[-1]
            self.ansver()
        elif len(self.search_ansver) > 2:
            self.search_ansver = self.search_ansver[0] + " WHERE " + " AND ".join(self.search_ansver[1::])
            self.ansver()

    def items_in_creation(self):
        if len(self.uniqueDrop.text().split(";")) == 0:
            ansver = f"(drops LIKE '%{self.uniqueDrop.text()}%')"
        else:
            search = "%".join(self.uniqueDrop.text().split(";"))
            ansver = f"(drops LIKE '%{search}%')"
        return ansver

    def friendlines(self):
        ansver = f"(friendliness LIKE '%{self.friendliness.currentText()}%')"
        return ansver

    def money_nums(self):
        ansver = f"(money LIKE '%{self.money_num.text()} {self.money.currentText()}%')"
        return ansver

    def search_location(self):
        location1 = []
        location2 = [self.location1.currentText(),
                     self.location2.currentText(),
                     self.location3.currentText()]
        for i in range(3):
            if location2[i] != "Ничего":
                location1.append(location2[i])
        if not self.loc_or.isChecked():
            ansver = self.or_and(True, location1)
        else:
            ansver = self.or_and(False, location1)
        return ansver

    def or_and(self, or_or_and, tegs):
        flag = " AND "
        if not or_or_and:
            flag = " OR "
        ansver = []
        for i in tegs:
            ansver.append(f"location LIKE '%{i}%'")
        ansver = f"{flag}".join(ansver)
        return "(" + ansver + ")"

    def golden1(self):
        ansver = f"(golden LIKE '%{self.golden.currentText()}%')"
        return ansver


def except_hook(cls, exception, traceback):
    # Просматриватель ошибок
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MobTable()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
