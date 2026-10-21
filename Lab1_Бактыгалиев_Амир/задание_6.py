"""
Дисциплина: Языки и технологии программирования
Файл: задание_6.py
Тема: Задание 6: Площадь треугольника
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 6: Площадь треугольника
def calculate_triangle_area(base: float, height: float) -> float:
    return 0.5 * base * height

if __name__ == "__main__":
    print("--- Расчет площади треугольника ---")
    base = float(input("Введите основание треугольника: "))
    height = float(input("Введите высоту треугольника: "))
    area = calculate_triangle_area(base, height)
    print(f"Площадь треугольника: {area:.2f}")