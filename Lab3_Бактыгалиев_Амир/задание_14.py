"""
Дисциплина: Языки и технологии программирования
Файл: задание_14.py
Тема: Задание 14: Генерация чисел Фибоначчи
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 14: Ряд Фибоначчи
def generate_fibonacci(n: int) -> list[int]:
    if n <= 0: return []
    if n == 1: return [0]
    fib = [0, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib

if __name__ == "__main__":
    count = int(input("Сколько чисел Фибоначчи сгенерировать? "))
    seq = generate_fibonacci(count)
    print("Последовательность:", seq)