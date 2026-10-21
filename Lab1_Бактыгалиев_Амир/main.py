"""
============================================================
  ГЛАВНОЕ МЕНЮ ЛАБОРАТОРНОЙ РАБОТЫ №1
  Дисциплина: Языки и технологии программирования
  Тема: Основы Python. Переменные, типы данных, ввод/вывод и арифметические операции
  Выполнил: Бактыгалиев Амир (ИС-25-22)
  Вариант: 7
============================================================
"""

import os
import sys

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear_console()
    print("=" * 60)
    print(f"  ЛАБОРАТОРНАЯ РАБОТА №1")
    print(f"  {profile.fullName} | Группа: {profile.groupName} | Вар: {profile.variant}")
    print("=" * 60)


def run_task_1():
    print("\n[ЗАПУСК: Задание 2: Площадь и периметр прямоугольника]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 2: Расчет параметров прямоугольника
    def calculate_rectangle(length: float, width: float) -> tuple[float, float]:
        area = length * width
        perimeter = 2.0 * (length + width)
        return area, perimeter
    
    if __name__ == "__main__":
        print("--- Расчет параметров прямоугольника ---")
        length = float(input("Введите длину прямоугольника: "))
        width = float(input("Введите ширину прямоугольника: "))
        area, perimeter = calculate_rectangle(length, width)
        print(f"Площадь прямоугольника: {area:.2f}")
        print(f"Периметр прямоугольника: {perimeter:.2f}")


def run_task_2():
    print("\n[ЗАПУСК: Задание 6: Площадь треугольника]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 6: Площадь треугольника
    def calculate_triangle_area(base: float, height: float) -> float:
        return 0.5 * base * height
    
    if __name__ == "__main__":
        print("--- Расчет площади треугольника ---")
        base = float(input("Введите основание треугольника: "))
        height = float(input("Введите высоту треугольника: "))
        area = calculate_triangle_area(base, height)
        print(f"Площадь треугольника: {area:.2f}")


def run_task_3():
    print("\n[ЗАПУСК: Задание 10: Разложение четырехзначного числа]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 10: Поразрядное разложение 4-значного числа
    def decompose_four_digit(number: int) -> dict:
        num_abs = abs(number)
        thousands = num_abs // 1000
        hundreds = (num_abs // 100) % 10
        tens = (num_abs // 10) % 10
        units = num_abs % 10
        total_sum = thousands + hundreds + tens + units
        return {
            "thousands": thousands,
            "hundreds": hundreds,
            "tens": tens,
            "units": units,
            "sum": total_sum
        }
    
    if __name__ == "__main__":
        print("--- Поразрядный анализ четырехзначного числа ---")
        n = int(input("Введите четырехзначное число: "))
        res = decompose_four_digit(n)
        print(f"Тысячи:  {res['thousands']}")
        print(f"Сотни:   {res['hundreds']}")
        print(f"Десятки: {res['tens']}")
        print(f"Единицы: {res['units']}")
        print(f"Сумма цифр: {res['sum']}")


def run_task_4():
    print("\n[ЗАПУСК: Задание 11: Калькулятор чека покупки]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 11: Расчет стоимости покупки
    def compute_order_cost(unit_price: float, count: int) -> float:
        return unit_price * count
    
    if __name__ == "__main__":
        print("--- Калькулятор стоимости товаров ---")
        price = float(input("Введите цену за единицу (руб): "))
        quantity = int(input("Введите количество единиц: "))
        total = compute_order_cost(price, quantity)
        print(f"Итоговая сумма чека: {total:.2f} руб.")


def run_task_5():
    print("\n[ЗАПУСК: Задание 17: Сложный процент банковского вклада]")
    print("-" * 50)
    # Исполняемый код задачи:
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


def run_task_6():
    print("\n[ЗАПУСК: Задание 18: Анализ трехзначного числа]")
    print("-" * 50)
    # Исполняемый код задачи:
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


def main_menu():
    while True:
        show_banner()
        print("\nДоступные задания:")
        print("  1. Задание 2: Площадь и периметр прямоугольника")
        print("  2. Задание 6: Площадь треугольника")
        print("  3. Задание 10: Разложение четырехзначного числа")
        print("  4. Задание 11: Калькулятор чека покупки")
        print("  5. Задание 17: Сложный процент банковского вклада")
        print("  6. Задание 18: Анализ трехзначного числа")
        print("  0. Выход из программы")
        print("-" * 60)
        
        choice = input("Выберите пункт меню (0-6): ").strip()
        
        if choice == "0":
            print("\nЗавершение работы. До свидания!")
            sys.exit(0)
        elif choice == "1":
            clear_console()
            run_task_1()
            input("\nНажмите Enter для возврата в меню...")
        elif choice == "2":
            clear_console()
            run_task_2()
            input("\nНажмите Enter для возврата в меню...")
        elif choice == "3":
            clear_console()
            run_task_3()
            input("\nНажмите Enter для возврата в меню...")
        elif choice == "4":
            clear_console()
            run_task_4()
            input("\nНажмите Enter для возврата в меню...")
        elif choice == "5":
            clear_console()
            run_task_5()
            input("\nНажмите Enter для возврата в меню...")
        elif choice == "6":
            clear_console()
            run_task_6()
            input("\nНажмите Enter для возврата в меню...")
        else:
            print("\n[!] Неверный выбор. Пожалуйста, введите цифру от 0 до 6.")
            input("Нажмите Enter для повтора...")

if __name__ == "__main__":
    main_menu()
