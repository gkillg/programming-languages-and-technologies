"""
Дисциплина: Языки и технологии программирования
Файл: задание_3.py
Тема: Задание 3: Сумма положительных чисел
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 3: Суммирование положительных чисел
def sum_positive_stream():
    total = 0
    count = 0
    print("Вводите целые числа (0 для завершения):")
    while True:
        val = int(input("> "))
        if val == 0:
            break
        if val > 0:
            total += val
            count += 1
    return total, count

if __name__ == "__main__":
    t, c = sum_positive_stream()
    print(f"Количество положительных: {c}")
    print(f"Сумма положительных: {t}")