"""
Дисциплина: Языки и технологии программирования
Файл: задание_8.py
Тема: Задание 8: Экстремумы трех чисел
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 8: Экстремумы трех чисел
def find_min_max(n1: float, n2: float, n3: float) -> tuple[float, float]:
    maximum = n1
    if n2 > maximum: maximum = n2
    if n3 > maximum: maximum = n3
    
    minimum = n1
    if n2 < minimum: minimum = n2
    if n3 < minimum: minimum = n3
    return minimum, maximum

if __name__ == "__main__":
    a = float(input("Число 1: "))
    b = float(input("Число 2: "))
    c = float(input("Число 3: "))
    mn, mx = find_min_max(a, b, c)
    print(f"Минимальное число: {mn}")
    print(f"Максимальное число: {mx}")