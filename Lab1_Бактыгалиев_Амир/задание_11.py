"""
Дисциплина: Языки и технологии программирования
Файл: задание_11.py
Тема: Задание 11: Калькулятор чека покупки
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 11: Расчет стоимости покупки
def compute_order_cost(unit_price: float, count: int) -> float:
    return unit_price * count

if __name__ == "__main__":
    print("--- Калькулятор стоимости товаров ---")
    price = float(input("Введите цену за единицу (руб): "))
    quantity = int(input("Введите количество единиц: "))
    total = compute_order_cost(price, quantity)
    print(f"Итоговая сумма чека: {total:.2f} руб.")