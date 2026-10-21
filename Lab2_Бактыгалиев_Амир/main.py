"""
============================================================
  ГЛАВНОЕ МЕНЮ ЛАБОРАТОРНОЙ РАБОТЫ №2
  Дисциплина: Языки и технологии программирования
  Тема: Управляющие конструкции и типы данных. Ветвления, валидация и скидки
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
    print(f"  ЛАБОРАТОРНАЯ РАБОТА №2")
    print(f"  {profile.fullName} | Группа: {profile.groupName} | Вар: {profile.variant}")
    print("=" * 60)


def run_task_1():
    print("\n[ЗАПУСК: Задание 1: Геометрическая валидация треугольника]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 1: Проверка и классификация треугольника
    def check_triangle(a: float, b: float, c: float) -> str:
        if a <= 0 or b <= 0 or c <= 0:
            return "Ошибка: стороны должны быть строго положительными числами."
        if a + b <= c or a + c <= b or b + c <= a:
            return "Треугольник с такими сторонами не существует."
        if a == b == c:
            return "Треугольник существует: Равносторонний"
        elif a == b or b == c or a == c:
            return "Треугольник существует: Равнобедренный"
        else:
            return "Треугольник существует: Разносторонний"
    
    if __name__ == "__main__":
        a = float(input("Сторона A: "))
        b = float(input("Сторона B: "))
        c = float(input("Сторона C: "))
        print(check_triangle(a, b, c))


def run_task_2():
    print("\n[ЗАПУСК: Задание 3: Валидация измерений прямоугольника]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 3: Прямоугольник с валидацией ввода
    def process_rectangle(length: float, width: float):
        if length <= 0 or width <= 0:
            print("Ошибка: длина и ширина должны быть строго больше нуля!")
            return
        area = length * width
        perimeter = 2 * (length + width)
        print(f"Площадь: {area:.2f}")
        print(f"Периметр: {perimeter:.2f}")
    
    if __name__ == "__main__":
        l = float(input("Введите длину: "))
        w = float(input("Введите ширину: "))
        process_rectangle(l, w)


def run_task_3():
    print("\n[ЗАПУСК: Задание 8: Экстремумы трех чисел]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 8: Экстремумы трех чисел
    def find_min_max(n1: float, n2: float, n3: float) -> tuple[float, float]:
        maximum = n1
        if n2 > maximum: maximum = n2
        if n3 > maximum: maximum = n3
        
        minimum = n1
        if n2 < minimum: minimum = n2
        if n3 < minimum: minimum = n3
        return minimum, maximum
    
    if __name__ == "__main__":
        a = float(input("Число 1: "))
        b = float(input("Число 2: "))
        c = float(input("Число 3: "))
        mn, mx = find_min_max(a, b, c)
        print(f"Минимальное число: {mn}")
        print(f"Максимальное число: {mx}")


def run_task_4():
    print("\n[ЗАПУСК: Задание 12: Расчет скидки по ступенчатой шкале]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 12: Дифференцированная скидка
    def calculate_discount(amount: float) -> tuple[float, float, float]:
        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
        if amount < 1000:
            pct = 0.0
        elif amount <= 5000:
            pct = 5.0
        else:
            pct = 10.0
        discount_sum = amount * (pct / 100.0)
        final_amount = amount - discount_sum
        return pct, discount_sum, final_amount
    
    if __name__ == "__main__":
        val = float(input("Введите сумму покупки: "))
        p, d, total = calculate_discount(val)
        print(f"Процент скидки: {p}%")
        print(f"Сумма скидки: {d:.2f} руб.")
        print(f"Итого к оплате: {total:.2f} руб.")


def run_task_5():
    print("\n[ЗАПУСК: Задание 16: Определение возрастной группы]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 16: Возрастная классификация
    def classify_age(age: int) -> str:
        if age < 0 or age > 130:
            return "Недопустимый возраст"
        if age <= 12:
            return "Ребенок (0-12 лет)"
        elif age <= 17:
            return "Подросток (13-17 лет)"
        elif age <= 64:
            return "Взрослый (18-64 года)"
        else:
            return "Пожилой человек (65+ лет)"
    
    if __name__ == "__main__":
        user_age = int(input("Введите возраст: "))
        print(f"Категория: {classify_age(user_age)}")


def run_task_6():
    print("\n[ЗАПУСК: Задание 18: Тарификатор стоимости поездки]")
    print("-" * 50)
    # Исполняемый код задачи:
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


def main_menu():
    while True:
        show_banner()
        print("\nДоступные задания:")
        print("  1. Задание 1: Геометрическая валидация треугольника")
        print("  2. Задание 3: Валидация измерений прямоугольника")
        print("  3. Задание 8: Экстремумы трех чисел")
        print("  4. Задание 12: Расчет скидки по ступенчатой шкале")
        print("  5. Задание 16: Определение возрастной группы")
        print("  6. Задание 18: Тарификатор стоимости поездки")
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
