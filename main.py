import sys
from abc import ABC, abstractmethod
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QDialog, QTableWidget, \
    QTableWidgetItem


class Person(ABC):
    @abstractmethod
    def get_name(self):
        pass


class User(Person):
    users_count = 0

    def __init__(self, name_user, weight, height, years_old, gender):
        self.__name_user = name_user
        self.__weight = int(weight)
        self.__height = int(height)
        self.__years_old = int(years_old)
        self.__gender = gender.lower()
        User.users_count += 1

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
        if self.__gender == 'male':
            return (10 * self.__weight) + (6.25 * self.__height) - (5 * self.__years_old) + 5
        elif self.__gender == 'female':
            return (10 * self.__weight) + (6.25 * self.__height) - (5 * self.__years_old) - 161
        return 0

    @staticmethod
    def get_users_count():
        return User.users_count


class Food:
    def __init__(self, name_food, calories, proteins, fats, carbohydrates):
        self.__name_food = name_food
        self.__calories = int(calories)
        self.__proteins = int(proteins)
        self.__fats = int(fats)
        self.__carbohydrates = int(carbohydrates)

    def __str__(self):
        return f"{self.__name_food}: {self.__calories} ккал, {self.__proteins} г белков, {self.__fats} г жиров, {self.__carbohydrates} г углеводов"

    def __add__(self, other):
        if isinstance(other, Food):
            return Food(
                "Смешанное блюдо",
                self.__calories + other.__calories,
                self.__proteins + other.__proteins,
                self.__fats + other.__fats,
                self.__carbohydrates + other.__carbohydrates
            )
        raise TypeError("Можно складывать только объекты типа Food")


class Meal:
    def __init__(self):
        self.food_items = []

    def add_food(self, food):
        if isinstance(food, Food):
            self.food_items.append(food)
        else:
            raise TypeError("Можно добавлять только объекты типа Food")

    def __str__(self):
        return "\n".join(str(food) for food in self.food_items)

class BreakFast:
    def __init__(self, list_of_meal):
        self.__list_of_meal = list_of_meal

    def get_list(self):
        return self.__list_of_meal

class Dinner:
    def __init__(self, list_of_meal):
        self.__list_of_meal = list_of_meal

    def get_list(self):
        return self.__list_of_meal

class Lunch:
    def __init__(self, list_of_meal):
        self.__list_of_meal = list_of_meal

    def get_list(self):
        return self.__list_of_meal

class Snack:
    def __init__(self, list_of_meal):
        self.__list_of_meal = list_of_meal

    def get_list(self):
        return self.__list_of_meal

class ChildWindow(QDialog):
    def __init__(self, user):
        super().__init__()
        self.userC = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"CalCulc-user({self.userC.get_name()})")
        self.setGeometry(150, 150, 500, 300)
        self.layout = QVBoxLayout()

        caloriesCount = self.userC.calories_culc()
        self.calories_normal = QLabel(f'Ваша норма калорий: {caloriesCount}')
        self.layout.addWidget(self.calories_normal)

        self.table = QTableWidget(4, 3)
        self.table.setHorizontalHeaderLabels(["Приём пищи", "Сколько съедено", "Цель"])
        data = [
            ["Завтрак", "", str(caloriesCount / 4)],
            ["Обед", "", str(caloriesCount / 4)],
            ["Ужин", "", str(caloriesCount / 4)],
            ["Перекус", "", str(caloriesCount / 4)]
        ]

        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                self.table.setItem(row, col, QTableWidgetItem(value))

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def set_user_data(self):
        try:
            self.user_data = User(
                self.enterName.text(),
                self.enterWeight.text(),
                self.enterHeight.text(),
                self.enterAge.text(),
                self.enterGender.text()
            )
            self.child_window = ChildWindow(self.user_data)
            self.child_window.exec()
        except ValueError:
            self.user_label.setText("Ошибка: не корректные данные")

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
sys.exit(app.exec())
