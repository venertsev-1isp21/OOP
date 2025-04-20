import sys
import logging
from abc import ABC, abstractmethod
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QDialog, QTableWidget, \
    QTableWidgetItem, QCheckBox, QMessageBox

logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Person(ABC):
    def __init__(self, name):
        self._name = name  # защищённый атрибут

    @abstractmethod
    def get_name(self):
        pass

    def show_info(self):  # базовый метод
        print(f"[Person] Name: {self._name}")

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

    def show_info(self):  # переопределение метода
        print(f"[User] Name: {self._name}, Weight: {self.__weight}, Age: {self.__years_old}")

    def dual_info(self, reverse=False):  # использует и свой метод, и метод базового класса
        if reverse:
            super().show_info()  # вызов базового
            self.show_info()
        else:
            self.show_info()
            super().show_info()

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

class Meal:
    def __init__(self):
        self.food_items = []

    def add_food(self, food):
        if isinstance(food, Food):
            self.food_items.append(food)
        else:
            raise TypeError("Можно добавлять только объекты типа Food")

    def get_total_calories(self):
        return sum(food.get_calories() for food in self.food_items)

class Breakfast(Meal):
    pass

class Lunch(Meal):
    pass

class Dinner(Meal):
    pass

class Snack(Meal):
    pass


class ChildWindow(QDialog):
    def __init__(self, user):
        super().__init__()
        self.userC = user
        self.init_ui()
        self.flag_BreakFast = 0
        self.flag_Dinner = 0
        self.flag_Lunch = 0
        self.flag_Snack = 0
        self.breakfast = Breakfast()
        self.lunch = Lunch()
        self.dinner = Dinner()
        self.snack = Snack()

    def checkbox_Breakfast(self, state):
        if state == 2:
            self.flag_BreakFast = 1
            self.Dinner_check.setEnabled(False)
            self.Lunch_check.setEnabled(False)
            self.Snack_check.setEnabled(False)
        else:
            self.flag_BreakFast = 0
            self.Dinner_check.setEnabled(True)
            self.Lunch_check.setEnabled(True)
            self.Snack_check.setEnabled(True)

    def checkbox_Dinner(self, state):
        if state == 2:
            self.flag_Dinner = 1
            self.BreakFast_check.setEnabled(False)
            self.Lunch_check.setEnabled(False)
            self.Snack_check.setEnabled(False)
        else:
            self.flag_Dinner = 0
            self.BreakFast_check.setEnabled(True)
            self.Lunch_check.setEnabled(True)
            self.Snack_check.setEnabled(True)

    def checkbox_Lunch(self, state):
        if state == 2:
            self.flag_Lunch = 1
            self.BreakFast_check.setEnabled(False)
            self.Dinner_check.setEnabled(False)
            self.Snack_check.setEnabled(False)
        else:
            self.flag_Lunch = 0
            self.BreakFast_check.setEnabled(True)
            self.Dinner_check.setEnabled(True)
            self.Snack_check.setEnabled(True)

    def checkbox_Snack(self, state):
        if state == 2:
            self.flag_Snack = 1
            self.BreakFast_check.setEnabled(False)
            self.Dinner_check.setEnabled(False)
            self.Lunch_check.setEnabled(False)
        else:
            self.flag_Snack = 0
            self.BreakFast_check.setEnabled(True)
            self.Dinner_check.setEnabled(True)
            self.Lunch_check.setEnabled(True)

    def add_food(self):
        food_name = self.enterFoodName.text()
        calories = self.enterFood_calories.text()
        proteins = self.enterproteins.text()
        fats = self.enterFats.text()
        carbs = self.enterCarbs.text()

        food_item = Food(food_name, calories, proteins, fats, carbs)

        if self.flag_BreakFast:
            self.breakfast.add_food(food_item)
            self.table.setItem(0, 1, QTableWidgetItem(str(self.breakfast.get_total_calories())))
        elif self.flag_Dinner:
            self.dinner.add_food(food_item)
            self.table.setItem(1, 1, QTableWidgetItem(str(self.dinner.get_total_calories())))
        elif self.flag_Lunch:
            self.lunch.add_food(food_item)
            self.table.setItem(2, 1, QTableWidgetItem(str(self.lunch.get_total_calories())))
        elif self.flag_Snack:
            self.snack.add_food(food_item)
            self.table.setItem(3, 1, QTableWidgetItem(str(self.snack.get_total_calories())))

        self.clear_food_fields()
        logging.info("Добавлена еда: %s (%s ккал)", food_name, calories)

    def clear_food_fields(self):
        self.enterFoodName.clear()
        self.enterFood_calories.clear()
        self.enterproteins.clear()
        self.enterFats.clear()
        self.enterCarbs.clear()

    from PyQt6.QtWidgets import QMessageBox

    def show_top_foods(self):
        meals = [
            ("Завтрак", self.breakfast),
            ("Обед", self.lunch),
            ("Ужин", self.dinner),
            ("Перекус", self.snack)
        ]

        result = ""

        for name, meal in meals:
            if not meal.food_items:
                result += f"{name}: нет данных\n\n"
                continue

            top_foods = sorted(meal.food_items, key=lambda food: food.get_calories(), reverse=True)[:3]
            result += f"{name} (топ по калориям):\n"
            result += "\n".join(f"{i + 1}. {food}" for i, food in enumerate(top_foods)) + "\n\n"

        QMessageBox.information(self, "Топ продукты по калориям", result.strip())

    def init_ui(self):
        self.setWindowTitle(f"CalCulc-user({self.userC.get_name()})")
        self.setGeometry(150, 150, 500, 300)
        self.layout = QVBoxLayout()

        caloriesCount = self.userC.calories_culc()
        self.calories_normal = QLabel(f'Ваша норма калорий: {caloriesCount}')

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

        self.Food_label = QLabel('Food data')

        self.Food_name = QLabel('Food name')
        self.enterFoodName = QLineEdit()

        self.Food_calories = QLabel('Food calories')
        self.enterFood_calories = QLineEdit()

        self.proteins = QLabel('Food proteins')
        self.enterproteins = QLineEdit()

        self.carbs = QLabel('Food carbs')
        self.enterCarbs = QLineEdit()

        self.fats = QLabel('Food fats')
        self.enterFats = QLineEdit()

        self.BreakFast_check = QCheckBox('Breakfast', self)
        self.BreakFast_check.stateChanged.connect(self.checkbox_Breakfast)

        self.Dinner_check = QCheckBox('Dinner', self)
        self.Dinner_check.stateChanged.connect(self.checkbox_Dinner)

        self.Lunch_check = QCheckBox('Lunch', self)
        self.Lunch_check.stateChanged.connect(self.checkbox_Lunch)

        self.Snack_check = QCheckBox('Snack', self)
        self.Snack_check.stateChanged.connect(self.checkbox_Snack)

        self.add_Button = QPushButton('Add food', self)
        self.add_Button.clicked.connect(self.add_food)

        self.top_food_button = QPushButton('Показать топ продуктов по калориям')
        self.top_food_button.clicked.connect(self.show_top_foods)

        for widget in [self.calories_normal, self.table, self.Food_label, self.Food_name, self.enterFoodName, self.Food_calories, self.enterFood_calories,
                       self.proteins, self.enterproteins, self.carbs, self.enterCarbs, self.fats, self.enterFats,
                       self.BreakFast_check, self.Dinner_check, self.Lunch_check, self.Snack_check, self.add_Button, self.top_food_button]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def show_message(self, type):
        if type == 1:
            msg = QMessageBox()
            msg.setWindowTitle("Уведомление")
            msg.setText("Действие выполненно")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        elif type == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Ошибка: не корректные данные")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

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
            self.show_message(0)
            logging.error("Ошибка ввода данных пользователем")
        finally:
            self.show_message(1)
            logging.info("Пользователь создан: %s", self.enterName.text())

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
