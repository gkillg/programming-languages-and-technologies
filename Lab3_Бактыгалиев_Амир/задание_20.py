"""
Дисциплина: Языки и технологии программирования
Файл: задание_20.py
Тема: Задание 20: Статистика числовой последовательности
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 20: Фильтрация и агрегация в диапазоне
def analyze_divisible_by_three(start: int, end: int):
    items = [x for x in range(start, end + 1) if x % 3 == 0]
    if not items:
        print("В данном диапазоне нет чисел, кратных 3.")
        return
    avg = sum(items) / len(items)
    print(f"Найдено чисел: {len(items)}")
    print(f"Числа: {items}")
    print(f"Минимум: {min(items)}, Максимум: {max(items)}")
    print(f"Среднее арифметическое: {avg:.2f}")

if __name__ == "__main__":
    s = int(input("Начало диапазона: "))
    e = int(input("Конец диапазона: "))
    analyze_divisible_by_three(s, e)