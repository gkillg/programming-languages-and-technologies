"""
Дисциплина: Языки и технологии программирования
Файл: задание_12.py
Тема: Задание 12: Проверка числа на простоту
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 12: Проверка числа на простоту (O(sqrt(N)))
import math

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    limit = int(math.isqrt(n))
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

if __name__ == "__main__":
    num = int(input("Введите натуральное число: "))
    result = "простое" if is_prime(num) else "составное"
    print(f"Число {num} — {result}.")