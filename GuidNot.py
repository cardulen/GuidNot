import sys
import io
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem


template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>715</width>
    <height>830</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>SQL-запрос к базе данных</string>
  </property>
  <layout class="QHBoxLayout" name="horizontalLayout">
   <item>
    <widget class="QWidget" name="widget" native="true">
     <widget class="QPushButton" name="pb">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>280</y>
        <width>651</width>
        <height>51</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <pointsize>12</pointsize>
        <weight>75</weight>
        <bold>true</bold>
       </font>
      </property>
      <property name="text">
       <string>Поиск</string>
      </property>
     </widget>
     <widget class="QTableWidget" name="tw">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>350</y>
        <width>671</width>
        <height>451</height>
       </rect>
      </property>
     </widget>
     <widget class="QLabel" name="label">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>330</y>
        <width>101</width>
        <height>16</height>
       </rect>
      </property>
      <property name="text">
       <string>Ответ</string>
      </property>
     </widget>
     <widget class="QComboBox" name="teg1">
      <property name="geometry">
       <rect>
        <x>510</x>
        <y>30</y>
        <width>161</width>
        <height>31</height>
       </rect>
      </property>
      <item>
       <property name="text">
        <string>Ничего</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Блок</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Еда</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Наживка</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Валюта</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Броня</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Маг</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Существо</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Фоновая стена</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Воин</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Призыв босса</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Боеприпасы</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Осветительный прибор</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Станок</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Оружие</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Заражение</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Аксессуар</string>
       </property>
      </item>
     </widget>
     <widget class="QLineEdit" name="name">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>30</y>
        <width>291</width>
        <height>20</height>
       </rect>
      </property>
     </widget>
     <widget class="QLabel" name="label_2">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>10</y>
        <width>111</width>
        <height>21</height>
       </rect>
      </property>
      <property name="text">
       <string>Название</string>
      </property>
     </widget>
     <widget class="QComboBox" name="teg2">
      <property name="geometry">
       <rect>
        <x>510</x>
        <y>70</y>
        <width>161</width>
        <height>31</height>
       </rect>
      </property>
      <item>
       <property name="text">
        <string>Ничего</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Блок</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Еда</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Наживка</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Валюта</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Броня</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Маг</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Существо</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Фоновая стена</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Воин</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Призыв босса</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Боеприпасы</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Осветительный прибор</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Станок</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Оружие</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Заражение</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Аксессуар</string>
       </property>
      </item>
     </widget>
     <widget class="QComboBox" name="teg3">
      <property name="geometry">
       <rect>
        <x>510</x>
        <y>110</y>
        <width>161</width>
        <height>31</height>
       </rect>
      </property>
      <item>
       <property name="text">
        <string>Ничего</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Блок</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Еда</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Наживка</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Валюта</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Броня</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Маг</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Существо</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Фоновая стена</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Воин</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Призыв босса</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Боеприпасы</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Осветительный прибор</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Станок</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Оружие</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Заражение</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Аксессуар</string>
       </property>
      </item>
     </widget>
     <widget class="QLabel" name="label_3">
      <property name="geometry">
       <rect>
        <x>510</x>
        <y>10</y>
        <width>47</width>
        <height>13</height>
       </rect>
      </property>
      <property name="text">
       <string>Теги</string>
      </property>
     </widget>
     <widget class="QWidget" name="verticalLayoutWidget">
      <property name="geometry">
       <rect>
        <x>510</x>
        <y>159</y>
        <width>176</width>
        <height>101</height>
       </rect>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout">
       <item>
        <widget class="QRadioButton" name="b_or">
         <property name="text">
          <string>Теги работают как и</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QRadioButton" name="b_and">
         <property name="text">
          <string>Теги работают как или</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
     <widget class="QSpinBox" name="nums_craft">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>90</y>
        <width>291</width>
        <height>22</height>
       </rect>
      </property>
     </widget>
     <widget class="QLabel" name="label_4">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>70</y>
        <width>281</width>
        <height>21</height>
       </rect>
      </property>
      <property name="text">
       <string>Количество предметов в создании</string>
      </property>
     </widget>
     <widget class="QLabel" name="label_5">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>130</y>
        <width>241</width>
        <height>16</height>
       </rect>
      </property>
      <property name="text">
       <string>Название прдметов в создании</string>
      </property>
     </widget>
     <widget class="QPlainTextEdit" name="plainTextEdit">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>180</y>
        <width>291</width>
        <height>91</height>
       </rect>
      </property>
     </widget>
     <widget class="QLabel" name="label_6">
      <property name="geometry">
       <rect>
        <x>10</x>
        <y>153</y>
        <width>161</width>
        <height>20</height>
       </rect>
      </property>
      <property name="text">
       <string>Писать через &quot;;&quot;</string>
      </property>
     </widget>
     <widget class="QWidget" name="verticalLayoutWidget_2">
      <property name="geometry">
       <rect>
        <x>320</x>
        <y>40</y>
        <width>207</width>
        <height>131</height>
       </rect>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout_2">
       <item>
        <widget class="QRadioButton" name="radioButton">
         <property name="text">
          <string>Предмет можно разместить</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QRadioButton" name="radioButton_2">
         <property name="text">
          <string>Предмет нельзя разместить</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QRadioButton" name="radioButton_3">
         <property name="text">
          <string>Не важно можно или нет</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
     <widget class="QLabel" name="label_7">
      <property name="geometry">
       <rect>
        <x>320</x>
        <y>10</y>
        <width>171</width>
        <height>16</height>
       </rect>
      </property>
      <property name="text">
       <string>Размещаемость</string>
      </property>
     </widget>
     <widget class="QLabel" name="label_8">
      <property name="geometry">
       <rect>
        <x>320</x>
        <y>190</y>
        <width>161</width>
        <height>21</height>
       </rect>
      </property>
      <property name="text">
       <string>Станция создания</string>
      </property>
     </widget>
     <widget class="QComboBox" name="comboBox">
      <property name="geometry">
       <rect>
        <x>320</x>
        <y>220</y>
        <width>151</width>
        <height>41</height>
       </rect>
      </property>
      <item>
       <property name="text">
        <string>Не имеет значения</string>
       </property>
      </item>
      <item>
       <property name="text">
        <string>Инвентарь</string>
       </property>
      </item>
     </widget>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.search_ansver = None
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.setWindowTitle("Guide't")
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
        if self.comboBox.currentText() != "Не имеет значения":
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
            self.search_ansver = "".join(self.search_ansver)
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


def except_hook(cls, exception, traceback):
    # Просматриватель ошибок
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
