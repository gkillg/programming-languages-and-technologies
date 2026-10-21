"""
Дисциплина: Языки и технологии программирования
Файл: задание_18.py
Тема: Задание 18: Тарификатор стоимости поездки
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 18: Калькулятор тарифа такси
def calculate_trip_fare(distance_km: float, is_night: bool) -> float:
    base_fare = 150.0  # Базовая посадка
    per_km_rate = 25.0  # За каждый километр
    total = base_fare + distance_km * per_km_rate
    if is_night:
        total *= 1.25  # Ночной коэффициент +25%
    return total

if __name__ == "__main__":
    dist = float(input("Расстояние поездки (км): "))
    night_choice = input("Ночное время? (1 - да, 0 - нет): ").strip()
    is_night = (night_choice == "1")
    fare = calculate_trip_fare(dist, is_night)
    print(f"Расчетная стоимость поездки: {fare:.2f} руб.")