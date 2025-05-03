import sys
import logging
from abc import ABC, abstractmethod
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QDialog,
                             QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox, QComboBox)

logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Person(ABC):
    def __init__(self, name):
        self._name = name

    @abstractmethod
    def get_name(self):
        pass

    def show_info(self):
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

    def show_info(self):
        print(f"[User] Name: {self._name}, Weight: {self.__weight}, Age: {self.__years_old}")

    def dual_info(self, reverse=False):
        if reverse:
            super().show_info()
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

class Breakfast(Meal): pass
class Lunch(Meal): pass
class Dinner(Meal): pass
class Snack(Meal): pass

class ChildWindow(QDialog):
    def __init__(self, user):
        super().__init__()
        self.userC = user
        self.product_list = ["Яблоко", "Хлеб", "Молоко"]
        self.init_ui()
        self.flag_BreakFast = self.flag_Dinner = self.flag_Lunch = self.flag_Snack = 0
        self.breakfast = Breakfast()
        self.lunch = Lunch()
        self.dinner = Dinner()
        self.snack = Snack()

    def checkbox_Breakfast(self, state):
        self.flag_BreakFast = state == Qt.CheckState.Checked
        self._set_enabled_except(self.BreakFast_check, not self.flag_BreakFast)

    def checkbox_Dinner(self, state):
        self.flag_Dinner = state == Qt.CheckState.Checked
        self._set_enabled_except(self.Dinner_check, not self.flag_Dinner)

    def checkbox_Lunch(self, state):
        self.flag_Lunch = state == Qt.CheckState.Checked
        self._set_enabled_except(self.Lunch_check, not self.flag_Lunch)

    def checkbox_Snack(self, state):
        self.flag_Snack = state == Qt.CheckState.Checked
        self._set_enabled_except(self.Snack_check, not self.flag_Snack)

    def _set_enabled_except(self, checkbox, enabled):
        for cb in [self.BreakFast_check, self.Dinner_check, self.Lunch_check, self.Snack_check]:
            if cb != checkbox:
                cb.setEnabled(enabled)

    def add_food(self):
        food_name = self.enterFoodName.currentText()
        calories = self.enterFood_calories.text()
        proteins = self.enterproteins.text()
        fats = self.enterFats.text()
        carbs = self.enterCarbs.text()

        if food_name not in self.product_list:
            self.product_list.append(food_name)
            self.enterFoodName.addItem(food_name)

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
        self.enterFood_calories.clear()
        self.enterproteins.clear()
        self.enterFats.clear()
        self.enterCarbs.clear()

    def show_top_foods(self):
        meals = [("Завтрак", self.breakfast), ("Обед", self.lunch), ("Ужин", self.dinner), ("Перекус", self.snack)]
        result = ""
        for name, meal in meals:
            if not meal.food_items:
                result += f"{name}: нет данных\n\n"
                continue
            top_foods = sorted(meal.food_items, key=lambda f: f.get_calories(), reverse=True)[:3]
            result += f"{name} (топ по калориям):\n" + "\n".join(f"{i+1}. {food}" for i, food in enumerate(top_foods)) + "\n\n"
        QMessageBox.information(self, "Топ продукты по калориям", result.strip())

    def init_ui(self):
        self.setWindowTitle(f"CalCulc-user({self.userC.get_name()})")
        self.setGeometry(150, 150, 500, 300)
        self.setStyleSheet(open("style.qss", "r").read())
        layout = QVBoxLayout()

        self.calories_normal = QLabel(f'Ваша норма калорий: {self.userC.calories_culc()}')

        self.table = QTableWidget(4, 3)
        self.table.setColumnWidth(0, 123)
        self.table.setColumnWidth(1, 205)
        self.table.setColumnWidth(2, 123)
        self.table.setFixedHeight(156)

        self.table.setObjectName("foodTable")
        self.table.setHorizontalHeaderLabels(["Приём пищи", "Сколько съедено", "Цель"])
        for i, name in enumerate(["Завтрак", "Обед", "Ужин", "Перекус"]):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.userC.calories_culc() / 4)))

        self.enterFoodName = QComboBox()
        self.enterFoodName.addItems(self.product_list)

        self.enterFood_calories = QLineEdit()
        self.enterproteins = QLineEdit()
        self.enterFats = QLineEdit()
        self.enterCarbs = QLineEdit()

        self.BreakFast_check = QCheckBox('Завтрак')
        self.Dinner_check = QCheckBox('Ужин')
        self.Lunch_check = QCheckBox('Обед')
        self.Snack_check = QCheckBox('Перекус')

        self.BreakFast_check.stateChanged.connect(self.checkbox_Breakfast)
        self.Dinner_check.stateChanged.connect(self.checkbox_Dinner)
        self.Lunch_check.stateChanged.connect(self.checkbox_Lunch)
        self.Snack_check.stateChanged.connect(self.checkbox_Snack)

        self.add_Button = QPushButton('Добавить еду')
        self.add_Button.clicked.connect(self.add_food)

        self.top_food_button = QPushButton('Топ продукты по калориям')
        self.top_food_button.clicked.connect(self.show_top_foods)

        for w in [self.calories_normal, self.table, QLabel('Название еды:'), self.enterFoodName,
                  QLabel('Калории:'), self.enterFood_calories, QLabel('Белки:'), self.enterproteins,
                  QLabel('Жиры:'), self.enterFats, QLabel('Углеводы:'), self.enterCarbs,
                  self.BreakFast_check, self.Dinner_check, self.Lunch_check, self.Snack_check,
                  self.add_Button, self.top_food_button]:
            layout.addWidget(w)

        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def show_message(self, type):
        msg = QMessageBox()
        msg.setWindowTitle("Уведомление" if type else "Ошибка")
        msg.setText("Действие выполнено" if type else "Ошибка: некорректные данные")
        msg.setIcon(QMessageBox.Icon.Information if type else QMessageBox.Icon.Critical)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def set_user_data(self):
        try:
            self.user_data = User(
                self.enterName.text(), self.enterWeight.text(), self.enterHeight.text(),
                self.enterAge.text(), self.enterGender.text()
            )
            ChildWindow(self.user_data).exec()
        except ValueError:
            self.show_message(0)
            logging.error("Ошибка ввода данных пользователем")
        else:
            self.show_message(1)
            logging.info("Пользователь создан: %s", self.enterName.text())

    def init_ui(self):
        self.setWindowTitle("CalCucl")
        self.setStyleSheet(open("style.qss", "r").read())
        layout = QVBoxLayout()

        self.enterName = QLineEdit()
        self.enterWeight = QLineEdit()
        self.enterHeight = QLineEdit()
        self.enterAge = QLineEdit()
        self.enterGender = QLineEdit()
        button = QPushButton("Ввести")
        button.clicked.connect(self.set_user_data)

        for w in [QLabel('Данные пользователя'), QLabel('Имя'), self.enterName, QLabel('Вес'), self.enterWeight,
                  QLabel('Рост'), self.enterHeight, QLabel('Возраст'), self.enterAge,
                  QLabel('Пол (male/female)'), self.enterGender, button]:
            layout.addWidget(w)

        self.setLayout(layout)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
