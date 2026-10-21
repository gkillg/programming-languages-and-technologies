"""
Дисциплина: Языки и технологии программирования
Файл: задание_17.py
Тема: Задание 17: Сложный процент банковского вклада
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 17: Сложные проценты по депозиту
def compound_interest(principal: float, rate_pct: float, years: int) -> float:
    return principal * ((1.0 + rate_pct / 100.0) ** years)

if __name__ == "__main__":
    print("--- Банковский депозитный калькулятор ---")
    deposit = float(input("Введите начальную сумму вклада: "))
    rate = float(input("Введите годовую процентную ставку (%): "))
    period = int(input("Введите срок вклада (лет): "))
    final_amount = compound_interest(deposit, rate, period)
    profit = final_amount - deposit
    print(f"Итоговая сумма на счете: {final_amount:.2f}")
    print(f"Чистый доход: {profit:.2f}")