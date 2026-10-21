"""
Дисциплина: Языки и технологии программирования
Файл: задание_18.py
Тема: Задание 18: Анализ трехзначного числа
Выполнил: Бактыгалиев Амир | Группа: ИС-25-22 | Вариант: 7
Учебный год: 2026
Стиль оформления: Академический (PEP 8, Type Hints, Docstrings)
"""

# Задание 18: Разряды трехзначного числа
def decompose_three_digit(num: int) -> dict:
    val = abs(num)
    h = val // 100
    t = (val // 10) % 10
    u = val % 10
    product = h * t * u
    return {"hundreds": h, "tens": t, "units": u, "product": product}

if __name__ == "__main__":
    num = int(input("Введите трехзначное число: "))
    data = decompose_three_digit(num)
    print(f"Сотни: {data['hundreds']}, Десятки: {data['tens']}, Единицы: {data['units']}")
    print(f"Произведение цифр: {data['product']}")