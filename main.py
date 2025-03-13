import sys
from abc import ABC, abstractmethod
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QDialog, QTableWidget, \
    QTableWidgetItem


class Person(ABC):
    def __init__(self, name):
        self._name = name

    @abstractmethod
    def get_name(self):
        pass


class User(Person):
    users_count = 0

    def __init__(self, name_user, weight, height, years_old, gender):
        super().__init__(name_user)
        self.__weight = int(weight)
        self.__height = int(height)
        self.__years_old = int(years_old)
        self.__gender = gender.lower()
        User.users_count += 1

    def show_data(self):
        return [self._name, self.__weight, self.__height, self.__years_old]

    def get_name(self):
        return self._name

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

    def __repr__(self):
        return f"Food('{self.__name_food}', {self.__calories}, {self.__proteins}, {self.__fats}, {self.__carbohydrates})"

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

    def get_calories(self):
        return self.__calories


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


class FoodManager:
    @staticmethod
    def find_max_calories(food_list):
        if not food_list or not any(row for row in food_list):
            return None

        max_food = None
        max_calories = -1

        for row in food_list:
            for food in row:
                if food and food.get_calories() > max_calories:
                    max_calories = food.get_calories()
                    max_food = food

        return max_food


class BreakFast:
    def __init__(self, list_of_meal):
        self.__list_of_meal = list_of_meal

    def get_list(self):
        return self.__list_of_meal


class Dinner(BreakFast):
    def __init__(self, list_of_meal):
        super().__init__(list_of_meal)

    def show_meals(self):
        return self.get_list()


class Lunch(Dinner):
    def __init__(self, list_of_meal, extra_meal):
        super().__init__(list_of_meal)
        self._extra_meal = extra_meal

    def get_extra_meal(self):
        return self._extra_meal


class Snack(Lunch):
    def __init__(self, list_of_meal, extra_meal):
        super().__init__(list_of_meal, extra_meal)

    def show_all_meals(self):
        return self.get_list() + [self.get_extra_meal()]


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

        for widget in [self.user_label, self.user_name, self.enterName, self.user_Weight, self.enterWeight,
                       self.user_Height, self.enterHeight, self.user_Age, self.enterAge, self.user_Gender,
                       self.enterGender, self.button]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)
        self.show()


app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())
