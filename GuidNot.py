import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QDialog
from PyQt5.QtGui import QPixmap


class CraftTable(QDialog):
    """
    Используется при выборе CraftБазыДанных
    Показывает Craft базу данных с пользовательсой сортировкой
    """
    def __init__(self):
        super().__init__()
        self.search_ansver = None
        uic.loadUi("craft.ui", self)
        self.con = sqlite3.connect('crafting.db')
        self.setWindowTitle("Craft")
        self.executor()

    def executor(self):
        """
        Получение указаний по нажатым кнопкам
        :return: Ничего
        """
        self.pb.clicked.connect(self.create_ansver)
        self.pushButton.clicked.connect(self.exit_dialog)

    def exit_dialog(self):
        """
        Выход из диалогового окна
        :return: Ничего
        """
        self.close()

    def ansver(self):
        """
        Записывает таблицу по SQL запросу
        :return: Ничего
        """
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

    def create_ansver(self):
        """
        собирает большой SQL запрос
        вызывает функцию ansver()
        :return: Ничего
        """
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

    def search_name(self):
        """
        Создание части SQL запроса по названию 1 столбца
        :return: Часть SQL запроса
        """
        ansver = f"((name LIKE '%{self.name.text()}%') OR (name LIKE '%{self.name.text().lower()}%'))"
        return ansver

    def nums_items(self):
        """
        Создание части SQL запроса по количеству уникальных предметов в создании
        :return: Часть SQL запроса
        """
        num = int(self.nums_craft.text())
        # с помощью 'LIKE %, %' будем проверять сколько предметов в создании
        if num == 1:  # часный случай
            ansver = f"(craft NOT LIKE '%, %')"
        else:
            num_item1 = "%".join(num * [", "])
            num_item2 = "%".join((num - 1) * [", "])
            ansver = f"(craft LIKE '%{num_item2}%') AND (craft NOT LIKE '%{num_item1}%')"
        return ansver

    def items_in_creation(self):
        """
        Создание части SQL запроса по названию предметов в создании
        :return: Часть SQL запроса
        """
        if len(self.plainTextEdit.toPlainText().split(";")) == 0:
            ansver = f"(craft LIKE '%{self.plainTextEdit.toPlainText()}%')"
        else:
            search = "%".join(self.plainTextEdit.toPlainText().split(";"))
            ansver = f"(craft LIKE '%{search}%')"
        return ansver

    def placability(self):
        """
        Создание части SQL запроса по размещаемости предмета
        :return: Часть SQL запроса
        """
        if self.radioButton.isChecked():
            ansver = f"(placability LIKE '%Можно%')"
        else:
            ansver = f"(placability LIKE '%Нельзя%')"
        return ansver

    def creation_station(self):
        """
        Создание части SQL запроса по станции создания предмета
        :return: Часть SQL запроса
        """
        ansver = f"(machine LIKE '%{self.comboBox.currentText()}%')"
        return ansver

    def search_tegs(self):
        """
        Создание части SQL запроса по имеющимся тегам
        :return: Часть SQL запроса
        """
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
        """
        Создание части SQL запроса по имеющимся тегам
        :param or_or_and: True или False
        :param tuple tegs: Список
        :return:
        """
        flag = " AND "
        if not or_or_and:
            flag = " OR "
        ansver = []
        for i in tegs:
            ansver.append(f"tags LIKE '%{i}%'")
        ansver = f"{flag}".join(ansver)
        return "(" + ansver + ")"


class MobTable(QDialog):
    """
    Используется при выборе MobБазыДанных
    Показывает Mob базу данных с пользовательсой сортировкой
    """
    def __init__(self):
        super().__init__()
        self.search_ansver = None
        uic.loadUi("mobs.ui", self)
        self.con = sqlite3.connect('crafting.db')
        self.setWindowTitle("Mobs")
        self.executor()

    def executor(self):
        """
        Получение указаний по нажатым кнопкам
        :return: Ничего
        """
        self.choice.clicked.connect(self.create_ansver)
        self.pushButton.clicked.connect(self.exit_dialog)

    def exit_dialog(self):
        """
        Выход из диалогового окна
        :return: Ничего
        """
        self.close()

    def ansver(self):
        """
        Записывает таблицу по SQL запросу
        :return: Ничего
        """
        cur = self.con.cursor()
        result = cur.execute(self.search_ansver).fetchall()
        # Проверка если нет ни одной тредуемой строчки
        if len(result) != 0:
            self.tableWidget.setColumnCount(len(result[0]))
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(result):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
            self.con.close()

    def create_ansver(self):
        """
        собирает большой SQL запрос
        вызывает функцию ansver()
        :return: Ничего
        """
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
            line = self.items_in_drops()
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

        # Поиск по возможности ловли
        if self.lovabilityCB.currentText() != "Не важно":
            line = self.lovability()
            if line != "":
                self.search_ansver.append(line)

        # Создание финального SQL запроса search_tegs
        if len(self.search_ansver) == 1:
            # Вывод базы данных без требований
            self.search_ansver = "SELECT * FROM mobs"
            self.ansver()
        elif len(self.search_ansver) == 2:
            # Вывод базы данных с 1 требованием
            self.search_ansver = self.search_ansver[0] + " WHERE " + self.search_ansver[-1]
            self.ansver()
        elif len(self.search_ansver) > 2:
            # Вывод базы данных с 2 и более требованиями
            self.search_ansver = self.search_ansver[0] + " WHERE " + " AND ".join(self.search_ansver[1::])
            self.ansver()

    def search_name(self):
        """
        Создание части SQL запроса по названию монстра
        :return: Часть SQL запроса
        """
        ansver = f"(name LIKE '%{self.name.text()}%' or name LIKE '%{self.name.text().lower()}%')"
        return ansver

    def nums_items(self):
        """
        Создание части SQL запроса по количеству уникального дропа который выподает
        :return: Часть SQL запроса
        """
        num = int(self.spinBox.text())
        # с помощью 'LIKE %, %' будем проверять сколько предметов выподает
        if num == 1:
            ansver = f"(drops NOT LIKE '%, %')"
        else:
            num_item1 = "%".join(num * [", "])
            num_item2 = "%".join((num - 1) * [", "])
            ansver = f"(drops LIKE '%{num_item2}%') AND (drops NOT LIKE '%{num_item1}%')"
        return ansver

    def items_in_drops(self):
        """
        Создание части SQL запроса по количеству уникального дропа который выподает
        :return: Часть SQL запроса
        """
        # Часный случай если один предмет выпадает
        if len(self.uniqueDrop.text().split(";")) == 0:
            ansver = f"(drops LIKE '%{self.uniqueDrop.text()}%')"
        else:
            search = "%".join(self.uniqueDrop.text().split(";"))
            ansver = f"(drops LIKE '%{search}%')"
        return ansver

    def friendlines(self):
        """
        Создание части SQL запроса по дружелюбности монстра
        :return: Часть SQL запроса
        """
        ansver = f"(friendliness LIKE '%{self.friendliness.currentText()}%')"
        return ansver

    def money_nums(self):
        """
        Создание части SQL запроса по количеству выподаемых монет
        :return: Часть SQL запроса
        """
        ansver = f"(money LIKE '%{self.money_num.text()} {self.money.currentText()}%')"
        return ansver

    def search_location(self):
        """
        Создание части SQL запроса по местонахождении монстри
        :return: Часть SQL запроса
        """
        location1 = []
        location2 = [self.location1.currentText(),
                     self.location2.currentText(),
                     self.location3.currentText()]
        for i in range(3):
            # Проверяем местонахождение если "-" то не используем
            if location2[i] != "-":
                location1.append(location2[i])
        if not self.loc_or.isChecked():
            ansver = self.or_and(True, location1)
        else:
            ansver = self.or_and(False, location1)
        return ansver

    def or_and(self, or_or_and, location):
        """
        Создание части SQL запроса по местонахождении монстри
        :param or_or_and: True или False
        :param tuple location: Список
        :return: Часть SQL запроса
        """
        flag = " AND "
        # Проверяем по какому типу создавать часть SQL запроса
        if not or_or_and:
            flag = " OR "
        ansver = []
        for i in location:
            ansver.append(f"location LIKE '%{i}%'")
        ansver = f"{flag}".join(ansver)
        return "(" + ansver + ")"

    def golden1(self):
        """
        Создание части SQL запроса по золотой разновидности монстра
        :return: Часть SQL запроса
        """
        ansver = f"(golden LIKE '%{self.golden.currentText()}%')"
        return ansver

    def lovability(self):
        """
        Создание части SQL запроса по ловибельности монстра
        :return: Часть SQL запроса
        """
        if self.lovabilityCB.currentText() == "Можно":
            ansver = f"(fishing LIKE '%можно%')"
        else:
            ansver = f"(fishing LIKE '%нельзя%')"
        return ansver


class Menu(QWidget):
    """
    Окно которое выводится в начале программы
    позволяет выбртать по каой базе данных делать поиск
    """
    def __init__(self):
        super().__init__()
        self.search_ansver = None
        uic.loadUi("choice.ui", self)
        self.setWindowTitle("Menu")
        self.picture()
        self.executor()

    def executor(self):
        """
        Реагирует на нажатие кнопки
        Вызывает функуию смены картинок
        :return: Ничего
        """
        self.choice.clicked.connect(self.go_to_table)
        self.dial.valueChanged.connect(self.picture)

    def picture(self):
        """
        Интерактивный dial
        Меняет картинки
        :return: Ничего
        """
        pixmap = QPixmap("pic/img_3.png")
        self.picture2.setPixmap(pixmap)
        # Картинка "Выход"
        if self.dial.value() == 1:
            pixmap = QPixmap("pic/img_1.png")
            self.picture1.setPixmap(pixmap)
        # Картинка "Создание"
        elif self.dial.value() == 2:
            pixmap = QPixmap("pic/img.png")
            self.picture1.setPixmap(pixmap)
        # Картинка "Монстр"
        elif self.dial.value() == 0:
            pixmap = QPixmap("pic/img_2.png")
            self.picture1.setPixmap(pixmap)

    def go_to_table(self):
        """
        Проверка действия кнопки
        :return: Ничего
        смысл функции: Выход или диалоговое окно
        """
        self.picture()
        if self.dial.value() == 1:
            # Выход
            exit()
        elif self.dial.value() == 0:
            # Активация Mobs-базы_данных
            dlg = MobTable()
            dlg.exec()
        elif self.dial.value() == 2:
            # Активация Craft-базы_данных
            dlg = CraftTable()
            dlg.exec()


def except_hook(cls, exception, traceback):
    """
    Для просмотра ошибок
    :param cls:
    :param exception:
    :param traceback:
    :return: вывод ошибок
    """
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
