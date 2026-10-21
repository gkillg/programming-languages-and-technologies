"""
Дисциплина: Языки и технологии программирования
Файл: задание_10.py
Тема: Задание 10: Разложение четырехзначного числа
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

from typing import Dict, Any

def analyze_four_digit_number(target_value: int) -> Dict[str, Any]:
    """
    Выполняет поразрядный анализ 4-значного натурального числа.
    
    Returns:
        Словарь с разрядами (thousands, hundreds, tens, units) и суммой цифр.
    """
    magnitude = abs(target_value)
    if magnitude < 1000 or magnitude > 9999:
        raise ValueError(f"Число {target_value} не является четырехзначным.")

    d_thousands: int = magnitude // 1000
    d_hundreds: int = (magnitude // 100) % 10
    d_tens: int = (magnitude // 10) % 10
    d_units: int = magnitude % 10
    digits_sum: int = d_thousands + d_hundreds + d_tens + d_units

    return {
        "thousands": d_thousands,
        "hundreds": d_hundreds,
        "tens": d_tens,
        "units": d_units,
        "sum": digits_sum,
        "is_palindrome": (d_thousands == d_units and d_hundreds == d_tens)
    }


def main() -> None:
    print("=== Лабораторная 1: Поразрядное разложение числа ===")
    try:
        raw_input_num: int = int(input("Введите 4-значное число: "))
        stats = analyze_four_digit_number(raw_input_num)
        print(f"Разряд тысяч:    {stats['thousands']}")
        print(f"Разряд сотен:    {stats['hundreds']}")
        print(f"Разряд десятков: {stats['tens']}")
        print(f"Разряд единиц:   {stats['units']}")
        print(f"Сумма цифр:      {stats['sum']}")
    except ValueError as ex:
        print(f"Входная ошибка: {ex}")


if __name__ == "__main__":
    main()