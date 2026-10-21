"""
Дисциплина: Языки и технологии программирования
Файл: задание_2.py
Тема: Задание 2: Площадь и периметр прямоугольника
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

from typing import Tuple

def compute_rectangle_geometry(rect_length: float, rect_width: float) -> Tuple[float, float]:
    """
    Вычисляет площадь и периметр прямоугольника по заданным размерам.
    
    Args:
        rect_length: Положительная длина прямоугольника.
        rect_width: Положительная ширина прямоугольника.
        
    Returns:
        Кортеж (площадь, периметр).
    """
    if rect_length <= 0 or rect_width <= 0:
        raise ValueError("Размеры прямоугольника должны быть положительными.")
        
    calculated_area: float = rect_length * rect_width
    calculated_perimeter: float = 2.0 * (rect_length + rect_width)
    return calculated_area, calculated_perimeter


def main() -> None:
    print(f"=== Расчет геометрии прямоугольника (Студент: {profile.fullName}) ===")
    try:
        user_length: float = float(input("Введите длину стороны A: "))
        user_width: float = float(input("Введите ширину стороны B: "))
        area, perimeter = compute_rectangle_geometry(user_length, user_width)
        print(f"-> Площадь прямоугольника S = {area:.2f}")
        print(f"-> Периметр прямоугольника P = {perimeter:.2f}")
    except ValueError as err:
        print(f"Ошибка ввода данных: {err}")


if __name__ == "__main__":
    main()