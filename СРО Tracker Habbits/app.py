"""
Веб-трекер привычек "Habby" (Ретро-консоль)
Дисциплина: Языки и технология программирования (СРО)
"""

import json
import os
from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = "habby_retro_secret_key"
DATA_FILE = "habby_save.json"


def load_game() -> dict:
    """Загрузка данных игры из JSON с обработкой исключений (Лекция: Работа с файлами и исключения)."""
    default_state = {
        "player": {"xp": 0, "level": 1, "completed_total": 0},
        "habits": []
    }
    if not os.path.exists(DATA_FILE):
        return default_state
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return default_state
    except (json.JSONDecodeError, OSError):
        return default_state


def save_game(game_state: dict) -> None:
    """Сохранение состояния игры в JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(game_state, f, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"Ошибка сохранения: {e}")


def update_streaks_on_load(habits: list) -> None:
    """Проверка пропущенных дней (обнуление серий)."""
    today = date.today()
    yesterday_str = (today - timedelta(days=1)).isoformat()
    today_str = today.isoformat()

    for habit in habits:
        last = habit.get("last_completed")
        if last and last != today_str and last != yesterday_str:
            habit["streak"] = 0


def add_xp(player: dict, amount: int) -> bool:
    """Расчет опыта и повышение уровня."""
    player["xp"] += amount
    req_xp = player["level"] * 60
    leveled_up = False
    while player["xp"] >= req_xp:
        player["level"] += 1
        player["xp"] -= req_xp
        req_xp = player["level"] * 60
        leveled_up = True
    return leveled_up


@app.route("/")
def index():
    game_state = load_game()
    update_streaks_on_load(game_state["habits"])
    save_game(game_state)

    today_str = date.today().isoformat()
    filter_type = request.args.get("filter", "all")
    
    habits = game_state["habits"]
    completed_today = sum(1 for h in habits if h.get("last_completed") == today_str)
    total_habits = len(habits)

    # Фильтрация
    if filter_type == "active":
        filtered_habits = [h for h in habits if h.get("last_completed") != today_str]
    elif filter_type == "done":
        filtered_habits = [h for h in habits if h.get("last_completed") == today_str]
    else:
        filtered_habits = habits

    progress_percent = int((completed_today / total_habits) * 100) if total_habits > 0 else 0

    return render_template(
        "index.html",
        player=game_state["player"],
        habits=filtered_habits,
        raw_habits=habits,
        today=today_str,
        progress_percent=progress_percent,
        completed_today=completed_today,
        total_habits=total_habits,
        current_filter=filter_type
    )


@app.route("/add", methods=["POST"])
def add_habit():
    name = request.form.get("name", "").strip()
    if not name:
        flash("Имя квеста не может быть пустым!", "error")
        return redirect(url_for("index"))

    game_state = load_game()
    if any(h["name"].lower() == name.lower() for h in game_state["habits"]):
        flash("Такой квест уже записан!", "error")
        return redirect(url_for("index"))

    game_state["habits"].append({
        "name": name,
        "streak": 0,
        "best_streak": 0,
        "last_completed": None
    })

    if add_xp(game_state["player"], 15):
        flash(f"Квест создан! (+15 XP). LEVEL UP! Твой уровень: Lv.{game_state['player']['level']}!", "levelup")
    else:
        flash(f"Квест «{name}» добавлен в свиток! (+15 XP)", "success")

    save_game(game_state)
    return redirect(url_for("index"))


@app.route("/complete/<int:habit_id>")
def complete_habit(habit_id: int):
    game_state = load_game()
    habits = game_state["habits"]

    if 0 <= habit_id < len(habits):
        h = habits[habit_id]
        today_str = date.today().isoformat()
        yesterday_str = (date.today() - timedelta(days=1)).isoformat()

        if h.get("last_completed") == today_str:
            flash("Квест уже выполнен сегодня!", "info")
            return redirect(url_for("index"))

        if h.get("last_completed") == yesterday_str:
            h["streak"] += 1
        else:
            h["streak"] = 1

        if h["streak"] > h.get("best_streak", 0):
            h["best_streak"] = h["streak"]

        h["last_completed"] = today_str
        game_state["player"]["completed_total"] = game_state["player"].get("completed_total", 0) + 1

        reward = 30 + (h["streak"] * 5)
        lvl_up = add_xp(game_state["player"], reward)
        save_game(game_state)

        if lvl_up:
            flash(f"ПОБЕДА! «{h['name']}» закрыт! (+{reward} XP). LEVEL UP!", "levelup")
        else:
            flash(f"Победа! «{h['name']}» выполнен! Комбо: x{h['streak']} (+{reward} XP)", "success")

    return redirect(url_for("index"))


@app.route("/reset/<int:habit_id>")
def reset_habit(habit_id: int):
    game_state = load_game()
    if 0 <= habit_id < len(game_state["habits"]):
        game_state["habits"][habit_id]["streak"] = 0
        game_state["habits"][habit_id]["last_completed"] = None
        save_game(game_state)
        flash("Комбо квеста обнулено.", "info")
    return redirect(url_for("index"))


@app.route("/delete/<int:habit_id>")
def delete_habit(habit_id: int):
    game_state = load_game()
    if 0 <= habit_id < len(game_state["habits"]):
        deleted = game_state["habits"].pop(habit_id)
        save_game(game_state)
        flash(f"Квест «{deleted['name']}» сожжен!", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
