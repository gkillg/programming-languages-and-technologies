"""
============================================================
  ГЛАВНОЕ МЕНЮ ЛАБОРАТОРНОЙ РАБОТЫ №3
  Дисциплина: Языки и технологии программирования
  Тема: Циклические алгоритмы и основы объектного моделирования
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
    print(f"  ЛАБОРАТОРНАЯ РАБОТА №3")
    print(f"  {profile.fullName} | Группа: {profile.groupName} | Вар: {profile.variant}")
    print("=" * 60)


def run_task_1():
    print("\n[ЗАПУСК: Задание 3: Сумма положительных чисел]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 3: Суммирование положительных чисел
    def sum_positive_stream():
        total = 0
        count = 0
        print("Вводите целые числа (0 для завершения):")
        while True:
            val = int(input("> "))
            if val == 0:
                break
            if val > 0:
                total += val
                count += 1
        return total, count
    
    if __name__ == "__main__":
        t, c = sum_positive_stream()
        print(f"Количество положительных: {c}")
        print(f"Сумма положительных: {t}")


def run_task_2():
    print("\n[ЗАПУСК: Задание 12: Проверка числа на простоту]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 12: Проверка числа на простоту (O(sqrt(N)))
    import math
    
    def is_prime(n: int) -> bool:
        if n <= 1:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        limit = int(math.isqrt(n))
        for i in range(5, limit + 1, 6):
            if n % i == 0 or n % (i + 2) == 0:
                return False
        return True
    
    if __name__ == "__main__":
        num = int(input("Введите натуральное число: "))
        result = "простое" if is_prime(num) else "составное"
        print(f"Число {num} — {result}.")


def run_task_3():
    print("\n[ЗАПУСК: Задание 14: Генерация чисел Фибоначчи]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 14: Ряд Фибоначчи
    def generate_fibonacci(n: int) -> list[int]:
        if n <= 0: return []
        if n == 1: return [0]
        fib = [0, 1]
        for _ in range(2, n):
            fib.append(fib[-1] + fib[-2])
        return fib
    
    if __name__ == "__main__":
        count = int(input("Сколько чисел Фибоначчи сгенерировать? "))
        seq = generate_fibonacci(count)
        print("Последовательность:", seq)


def run_task_4():
    print("\n[ЗАПУСК: Задание 18: Приближенное вычисление суммы ряда]")
    print("-" * 50)
    # Исполняемый код задачи:
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


def run_task_5():
    print("\n[ЗАПУСК: Задание 20: Статистика числовой последовательности]")
    print("-" * 50)
    # Исполняемый код задачи:
    # Задание 20: Фильтрация и агрегация в диапазоне
    def analyze_divisible_by_three(start: int, end: int):
        items = [x for x in range(start, end + 1) if x % 3 == 0]
        if not items:
            print("В данном диапазоне нет чисел, кратных 3.")
            return
        avg = sum(items) / len(items)
        print(f"Найдено чисел: {len(items)}")
        print(f"Числа: {items}")
        print(f"Минимум: {min(items)}, Максимум: {max(items)}")
        print(f"Среднее арифметическое: {avg:.2f}")
    
    if __name__ == "__main__":
        s = int(input("Начало диапазона: "))
        e = int(input("Конец диапазона: "))
        analyze_divisible_by_three(s, e)


def main_menu():
    while True:
        show_banner()
        print("\nДоступные задания:")
        print("  1. Задание 3: Сумма положительных чисел")
        print("  2. Задание 12: Проверка числа на простоту")
        print("  3. Задание 14: Генерация чисел Фибоначчи")
        print("  4. Задание 18: Приближенное вычисление суммы ряда")
        print("  5. Задание 20: Статистика числовой последовательности")
        print("  0. Выход из программы")
        print("-" * 60)
        
        choice = input("Выберите пункт меню (0-5): ").strip()
        
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
        else:
            print("\n[!] Неверный выбор. Пожалуйста, введите цифру от 0 до 5.")
            input("Нажмите Enter для повтора...")

if __name__ == "__main__":
    main_menu()
