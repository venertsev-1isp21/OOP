class Food:
    def __init__(self, name_food, calories, squirrels, fats, carbohydrates):
        self.__name_food = name_food
        self.__calories = calories
        self.__squirrels = squirrels
        self.__fats = fats
        self.__carbohydrates = carbohydrates

class User:
    def __init__(self, name_user, weight, height, years_old):
        self.__name_user = name_user
        self.__weight = weight
        self.__height = height
        self.__years_old = years_old

class BreakFast:
    def __init__(self, list_of_food):
        self.__list_of_food = list_of_food

class Dinner:
    def __init__(self, list_of_food):
        self.__list_of_food = list_of_food

class Lunch:
    def __init__(self, list_of_food):
        self.__list_of_food = list_of_food

class Snack:
    def __init__(self, list_of_food):
        self.__list_of_food = list_of_food
