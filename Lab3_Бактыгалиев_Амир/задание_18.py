"""
Дисциплина: Языки и технологии программирования
Файл: задание_18.py
Тема: Задание 18: Приближенное вычисление суммы ряда
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 18: Вычисление суммы знакочередующегося ряда 1 - 1/2 + 1/3 - 1/4...
def approximate_series(epsilon: float = 0.0001) -> tuple[float, int]:
    total = 0.0
    term = 1.0
    n = 1
    sign = 1
    while abs(term) >= epsilon:
        term = sign * (1.0 / n)
        total += term
        n += 1
        sign = -sign
    return total, n - 1

if __name__ == "__main__":
    eps = float(input("Введите требуемую точность (например, 0.001): "))
    res, steps = approximate_series(eps)
    print(f"Сумма ряда: {res:.6f} (ln(2) ≈ 0.693147)")
    print(f"Количество выполненных шагов: {steps}")