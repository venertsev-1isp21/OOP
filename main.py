import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QDialog, QTableWidget, QTableWidgetItem

class ChildWindow(QDialog):
    def __init__(self, user):
        super().__init__()
        self.userC = user
        self.init_ui(self.userC)

    def init_ui(self, user):
        self.setWindowTitle(f"CalCulc-user({user.get_name()})")
        self.setGeometry(150, 150, 200, 150)

        self.caloriesCount = user.calories_culc()

        self.layout = QVBoxLayout()

        self.calories_normal = QLabel('Ваша норма калорий: ' + str(self.caloriesCount))

        self.table = QTableWidget()
        self.table.setRowCount(4)
        self.table.setColumnCount(3)
        self.table.setFixedSize(460, 250)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 100)
        self.table.setHorizontalHeaderLabels(["Приём пищи", "Сколько съедено", "Цель"])

        data = [
            ["Завтарк", "", str(self.caloriesCount / 4)],
            ["Обед", "", str(self.caloriesCount / 4)],
            ["Ужин", "", str(self.caloriesCount / 4)],
            ["Перекус", "", str(self.caloriesCount / 4)],
        ]

        for row in range(4):
            for col in range(3):
                item = QTableWidgetItem(data[row][col])
                self.table.setItem(row, col, item)

        self.layout.addWidget(self.calories_normal)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def set_user_data(self):
        self.user_data = User(self.enterName.text(), self.enterWeight.text(), self.enterHeight.text(), self.enterAge.text(), self.enterGender.text())
        self.child_window = ChildWindow(self.user_data)  # Создаем экземпляр дочернего окна
        self.child_window.exec()  # Показываем дочернее окно

    def init_ui(self):
        self.setWindowTitle("CalCucl")
        self.resize(200, 230)
        self.layout = QVBoxLayout()

        self.user_label = QLabel('User data')

        self.user_name = QLabel('User name')
        self.enterName = QLineEdit()

        self.user_Weight = QLabel('User weight')
        self.enterWeight = QLineEdit()

        self.user_Height = QLabel('User height')
        self.enterHeight = QLineEdit()

        self.user_Age = QLabel('User age')
        self.enterAge = QLineEdit()

        self.user_Gender = QLabel('User gender(male/female)')
        self.enterGender = QLineEdit()

        self.button = QPushButton("Enter")
        self.button.setFixedSize(100, 30)
        self.button.clicked.connect(self.set_user_data)


        self.layout.addWidget(self.user_label)
        self.layout.setAlignment(self.user_label, Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.user_name)
        self.layout.addWidget(self.enterName)

        self.layout.addWidget(self.user_Weight)
        self.layout.addWidget(self.enterWeight)

        self.layout.addWidget(self.user_Height)
        self.layout.addWidget(self.enterHeight)

        self.layout.addWidget(self.user_Age)
        self.layout.addWidget(self.enterAge)

        self.layout.addWidget(self.user_Gender)
        self.layout.addWidget(self.enterGender)

        self.layout.addWidget(self.button)
        self.layout.setAlignment(self.button, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        self.show()

app = QApplication(sys.argv)
window = MainWindow()

class Food:
    def __init__(self, name_food, calories, squirrels, fats, carbohydrates):
        self.__name_food = name_food
        self.__calories = calories
        self.__squirrels = squirrels
        self.__fats = fats
        self.__carbohydrates = carbohydrates

class User:
    def __init__(self, name_user, weight, height, years_old, gender):
        self.__name_user = name_user
        self.__weight = weight
        self.__height = height
        self.__years_old = years_old
        self.__gender = gender

    def show_data(self):
        return [self.__name_user, self.__weight, self.__height, self.__years_old]

    def get_name(self):
        return self.__name_user

    def get_weight(self):
        return self.__weight

    def get_height(self):
        return self.__height

    def get_age(self):
        return self.__years_old

    def get_gender(self):
        return self.__gender

    def calories_culc(self):
        if self.__gender.lower() == 'male':
            calories = (10 * int(self.__weight)) + (6.25 * int(self.__height)) - (5 * int(self.__years_old)) + 5
            return calories
        elif self.__gender.lower() == 'female':
            calories = (10 * int(self.__weight)) + (6.25 * int(self.__height)) - (5 * int(self.__years_old)) - 161
            return float(calories)

class BreakFast:
    def __init__(self, list_of_food):
        self.__list_of_food = list_of_food

    def get_list(self):
        return self.__list_of_food

class Dinner:
    def __init__(self, list_of_food):
        self.__list_of_food = list_of_food

    def get_list(self):
        return self.__list_of_food

class Lunch:
    def __init__(self, list_of_food):
        self.__list_of_food = list_of_food

    def get_list(self):
        return self.__list_of_food

class Snack:
    def __init__(self, list_of_food):
        self.__list_of_food = list_of_food

    def get_list(self):
        return self.__list_of_food


sys.exit(app.exec())
