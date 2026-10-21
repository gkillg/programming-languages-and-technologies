"""
Дисциплина: Языки и технологии программирования
Файл: задание_12.py
Тема: Задание 12: Расчет скидки по ступенчатой шкале
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

from typing import Tuple

def evaluate_discount_policy(gross_amount: float) -> Tuple[float, float, float]:
    """
    Вычисляет процент скидки, величину дисконта и чистую сумму к оплате.
    
    Шкала скидок:
    - до 1000 руб: 0%
    - от 1000 до 5000 руб: 5%
    - свыше 5000 руб: 10%
    """
    if gross_amount < 0.0:
        raise ValueError("Сумма счета не может быть отрицательной.")

    discount_rate: float
    if gross_amount < 1000.0:
        discount_rate = 0.0
    elif gross_amount <= 5000.0:
        discount_rate = 5.0
    else:
        discount_rate = 10.0

    discount_rub: float = gross_amount * (discount_rate / 100.0)
    net_payable: float = gross_amount - discount_rub
    return discount_rate, discount_rub, net_payable


def main() -> None:
    print(f"=== Расчет скидки по ступенчатой шкале (Вар. {profile.variant}) ===")
    try:
        order_sum: float = float(input("Введите базовую сумму покупки (руб): "))
        pct, rub, net = evaluate_discount_policy(order_sum)
        print(f"Примененная скидка: {pct:.1f}%")
        print(f"Сумма экономии:     {rub:.2f} руб.")
        print(f"Итоговая стоимость: {net:.2f} руб.")
    except ValueError as err:
        print(f"Ошибка вычисления: {err}")


if __name__ == "__main__":
    main()