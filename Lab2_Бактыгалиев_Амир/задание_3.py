"""
Дисциплина: Языки и технологии программирования
Файл: задание_3.py
Тема: Задание 3: Валидация измерений прямоугольника
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 3: Прямоугольник с валидацией ввода
def process_rectangle(length: float, width: float):
    if length <= 0 or width <= 0:
        print("Ошибка: длина и ширина должны быть строго больше нуля!")
        return
    area = length * width
    perimeter = 2 * (length + width)
    print(f"Площадь: {area:.2f}")
    print(f"Периметр: {perimeter:.2f}")

if __name__ == "__main__":
    l = float(input("Введите длину: "))
    w = float(input("Введите ширину: "))
    process_rectangle(l, w)