"""
Project: HABBY - 8-Bit Pixel Habit Tracker
Discipline: Programming Languages and Technologies
Style: Retro RPG / Virtual Pet
"""

import json
import os
from datetime import date, timedelta

DATA_FILE = "habby_save.json"

HABBY_HAPPY = r"""
      (\__/)
      ( ^.^)   < [ HABBY: "Ура! Ты прокачиваешь свои навыки!" ]
     c(") (")
"""

HABBY_IDLE = r"""
      (\__/)
      ( o.o)   < [ HABBY: "Пип-боп! Готов закрывать квесты?" ]
     c(") (")
"""

HABBY_SAD = r"""
      (\__/)
      ( T.T)   < [ HABBY: "О нет... Серия сгорела, но не сдавайся!" ]
     c(") (")
"""

HABBY_PROUD = r"""
      (\__/)   * LEVEL UP! *
      ( ★.★) / < [ HABBY: "НЕВЕРОЯТНО! Новый рекорд!" ]
     c(") (")
"""

BANNER = r"""
 ___________________________________________________________
|  _   _    _    ____  ______   __  ____  _____ _____ ____  |
| | | | |  / \  | __ )| __ ) \ / / |  _ \| ____|_   _|  _ \ |
| | |_| | / _ \ |  _ \|  _ \\ V /  | |_) |  _|   | | | |_) ||
| |  _  |/ ___ \| |_) | |_) || |   |  _ <| |___  | | |  _ < |
| |_| |_/_/   \_\____/|____/ |_|   |_| \_\_____| |_| |_| \_\|
|___________________________________________________________|
"""


def pause() -> None:
    input("\n[Нажмите ENTER, чтобы продолжить путь...]")


def load_game(filepath: str) -> dict:
    default_state = {
        "player": {"xp": 0, "level": 1},
        "habits": []
    }
    if not os.path.exists(filepath):
        return default_state
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "habits" in data and "player" in data:
                return data
            return default_state
    except (json.JSONDecodeError, OSError):
        print("\n[!] Картридж поврежден! Habby начинает новую игру...")
        return default_state


def save_game(filepath: str, game_state: dict) -> None:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(game_state, f, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"\n[!] Ошибка записи на картридж: {e}")


def update_streaks_on_startup(habits: list) -> bool:
    today = date.today()
    yesterday_str = (today - timedelta(days=1)).isoformat()
    today_str = today.isoformat()
    lost_any = False

    for habit in habits:
        last = habit.get("last_completed")
        if last and last != today_str and last != yesterday_str:
            if habit.get("streak", 0) > 0:
                habit["streak"] = 0
                lost_any = True
    return lost_any


def add_xp(player: dict, amount: int) -> None:
    player["xp"] += amount
    req_xp = player["level"] * 50
    if player["xp"] >= req_xp:
        player["level"] += 1
        player["xp"] -= req_xp
        print(HABBY_PROUD)
        print(f"★ ПОВЫШЕНИЕ УРОВНЯ! Теперь твой уровень: Lv.{player['level']}! ★")


def get_safe_int(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        raw_val = input(prompt).strip()
        try:
            val = int(raw_val)
            if min_val <= val <= max_val:
                return val
            print(f"[!] Введи команду от {min_val} до {max_val}!")
        except ValueError:
            print("[!] Ошибка! Habby понимает только цифры клавиатуры.")


def show_hud(player: dict) -> None:
    lvl = player.get("level", 1)
    xp = player.get("xp", 0)
    req_xp = lvl * 50
    bar_len = 10
    filled = int(bar_len * (xp / req_xp)) if req_xp else 0
    xp_bar = "■" * filled + "·" * (bar_len - filled)

    print(f"+---------------------------------------------------------+")
    print(f"|  ГЕРОЙ: Lv.{lvl:<2} | EXP: [{xp_bar}] {xp}/{req_xp} XP               |")
    print(f"+---------------------------------------------------------+")


def view_habits(game_state: dict) -> None:
    habits = game_state["habits"]
    if not habits:
        print(HABBY_IDLE)
        print("[ Твой журнал квестов пуст. Добавь первую цель! ]")
        return

    today_str = date.today().isoformat()
    print("\n.------------------ ЖУРНАЛ КВЕСТОВ -------------------.")
    print(f"| {'№':<2} | {'СТАТУС':<12} | {'НАЗВАНИЕ':<18} | {'КОМБО':<8} | {'МАКС'}")
    print("|----+--------------+--------------------+----------+-----|")

    completed_today = 0
    for idx, h in enumerate(habits, start=1):
        is_done = (h.get("last_completed") == today_str)
        if is_done:
            completed_today += 1
            status = "[★ ВЫПОЛНЕНО]"
        else:
            status = "[· В ПРОЦЕССЕ]"

        name = h["name"][:16] + ".." if len(h["name"]) > 18 else h["name"]
        streak = f"x{h.get('streak', 0)}"
        best = f"{h.get('best_streak', 0)}"

        print(f"| {idx:<2} | {status:<12} | {name:<18} | {streak:<8} | {best:<4}|")

    print("'-----------------------------------------------------'")

    percent = int((completed_today / len(habits)) * 100)
    print(f">> Завершено сегодня: {completed_today}/{len(habits)} [{percent}%]")


def add_habit(game_state: dict) -> None:
    print("\n--- СОЗДАНИЕ НОВОГО КВЕСТА ---")
    while True:
        name = input("Введи имя квеста (или '0' для отмены): ").strip()
        if name == "0":
            return
        if not name:
            print("[!] Имя квеста не может быть пустым!")
            continue
        if any(h["name"].lower() == name.lower() for h in game_state["habits"]):
            print("[!] Такой квест уже записан в свитке!")
            continue

        game_state["habits"].append({
            "name": name,
            "streak": 0,
            "best_streak": 0,
            "last_completed": None
        })
        print(HABBY_HAPPY)
        print(f"[ Habby принял квест «{name}» к исполнению! (+10 XP) ]")
        add_xp(game_state["player"], 10)
        break


def mark_habit_done(game_state: dict) -> None:
    habits = game_state["habits"]
    if not habits:
        print("\n[ В журнале нет квестов для выполнения! ]")
        return

    view_habits(game_state)
    choice = get_safe_int("\nВыбери номер закрытого квеста (0 для отмены): ", 0, len(habits))
    if choice == 0:
        return

    habit = habits[choice - 1]
    today = date.today()
    today_str = today.isoformat()
    yesterday_str = (today - timedelta(days=1)).isoformat()
    last = habit.get("last_completed")

    if last == today_str:
        print(HABBY_IDLE)
        print(f"[ «{habit['name']}» уже закрыт сегодня! Habby советует отдохнуть. ]")
        return

    if last == yesterday_str:
        habit["streak"] += 1
    else:
        habit["streak"] = 1

    if habit["streak"] > habit.get("best_streak", 0):
        habit["best_streak"] = habit["streak"]

    habit["last_completed"] = today_str
    
    reward = 25 + (habit["streak"] * 5)
    print(HABBY_HAPPY)
    print(f"[ ПОБЕДА! Квест «{habit['name']}» выполнен! Комбо: x{habit['streak']} ]")
    print(f"[ Награда: +{reward} XP ]")
    add_xp(game_state["player"], reward)


def manage_habit(game_state: dict) -> None:
    habits = game_state["habits"]
    if not habits:
        print("\n[ Журнал пуст. ]")
        return

    view_habits(game_state)
    choice = get_safe_int("\nВыбери номер квеста для настройки (0 для отмены): ", 0, len(habits))
    if choice == 0:
        return

    habit = habits[choice - 1]
    print(f"\nДействия над «{habit['name']}»:")
    print("1. Сбросить счетчик комбо")
    print("2. Сжечь свиток квеста (Удалить)")
    print("0. Назад")

    act = get_safe_int("Выбор: ", 0, 2)
    if act == 1:
        habit["streak"] = 0
        habit["last_completed"] = None
        print(HABBY_SAD)
        print(f"[ Комбо квеста «{habit['name']}» обнулено. ]")
    elif act == 2:
        confirm = input(f"Точно удалить «{habit['name']}»? (y/n): ").strip().lower()
        if confirm in ("y", "yes", "да", "д"):
            habits.pop(choice - 1)
            print("\n[ Квест стерт из памяти картриджа. ]")


def main():
    print(BANNER)
    game_state = load_game(DATA_FILE)

    if update_streaks_on_startup(game_state["habits"]):
        print(HABBY_SAD)
        print("[ Habby заметил, что вчера были пропуски. Комбо сгорело, но ты справишься! ]")
    else:
        print(HABBY_IDLE)

    while True:
        show_hud(game_state["player"])
        print(" [1] 📜 Посмотреть журнал квестов")
        print(" [2] ⚔️  Засчитать выполнение квеста")
        print(" [3] ➕ Добавить новую цель")
        print(" [4] ⚙️  Сбросить / Удалить квест")
        print(" [0] 💾 Сохранить и выйти")
        print("+---------------------------------------------------------+")

        choice = get_safe_int("Команда > ", 0, 4)

        if choice == 1:
            view_habits(game_state)
            pause()
        elif choice == 2:
            mark_habit_done(game_state)
            save_game(DATA_FILE, game_state)
            pause()
        elif choice == 3:
            add_habit(game_state)
            save_game(DATA_FILE, game_state)
            pause()
        elif choice == 4:
            manage_habit(game_state)
            save_game(DATA_FILE, game_state)
            pause()
        elif choice == 0:
            save_game(DATA_FILE, game_state)
            print("\n[ Прогресс записан на картридж. Habby ждет тебя завтра! ]\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Экстренное выключение консоли. Данные защищены.")
