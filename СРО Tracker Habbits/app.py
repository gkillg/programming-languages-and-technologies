"""
Веб-трекер привычек "Habby" (Мультипользовательская версия)
Дисциплина: Языки и технология программирования (СРО)
"""

import json
import os
import random
import string
from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "habby_retro_multiuser_secret_key"
DATA_FILE = "habby_save.json"


def generate_unique_id() -> str:
    """Генерация уникального ретро-ID (например: HB-4921)."""
    digits = "".join(random.choices(string.digits, k=4))
    return f"HB-{digits}"


def load_all_data() -> dict:
    """Загрузка общей базы данных из JSON (Лекция: Файлы и JSON)."""
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) and "users" in data else {"users": {}}
    except (json.JSONDecodeError, OSError):
        return {"users": {}}


def save_all_data(data: dict) -> None:
    """Сохранение базы данных в JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"[Критическая ошибка сохранения]: {e}")


def get_current_user(all_data: dict) -> tuple:
    """Получение данных текущего пользователя по сессии."""
    user_id = session.get("user_id")
    if not user_id or user_id not in all_data["users"]:
        return None, None
    return user_id, all_data["users"][user_id]


def update_streaks_on_load(habits: list) -> None:
    """Проверка пропущенных дней."""
    today = date.today()
    yesterday_str = (today - timedelta(days=1)).isoformat()
    today_str = today.isoformat()

    for habit in habits:
        last = habit.get("last_completed")
        if last and last != today_str and last != yesterday_str:
            habit["streak"] = 0


def add_xp(player: dict, amount: int) -> bool:
    """Расчет опыта и Level Up."""
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
    all_data = load_all_data()
    user_id, user_data = get_current_user(all_data)

    # Если пользователь еще не создал слот игрока — отправляем на экран логина
    if not user_data:
        return render_template("login.html")

    update_streaks_on_load(user_data["habits"])
    save_all_data(all_data)

    today_str = date.today().isoformat()
    filter_type = request.args.get("filter", "all")
    habits = user_data["habits"]

    completed_today = sum(1 for h in habits if h.get("last_completed") == today_str)
    total_habits = len(habits)

    if filter_type == "active":
        filtered_habits = [h for h in habits if h.get("last_completed") != today_str]
    elif filter_type == "done":
        filtered_habits = [h for h in habits if h.get("last_completed") == today_str]
    else:
        filtered_habits = habits

    progress_percent = int((completed_today / total_habits) * 100) if total_habits > 0 else 0

    return render_template(
        "index.html",
        user_id=user_id,
        nickname=user_data["nickname"],
        player=user_data["player"],
        habits=filtered_habits,
        today=today_str,
        progress_percent=progress_percent,
        completed_today=completed_today,
        total_habits=total_habits,
        current_filter=filter_type
    )


@app.route("/register", methods=["POST"])
def register():
    """Создание нового слота сохранения с уникальным ID."""
    nickname = request.form.get("nickname", "").strip()
    if not nickname:
        flash("Введи имя героя!", "error")
        return redirect(url_for("index"))

    all_data = load_all_data()
    new_id = generate_unique_id()
    while new_id in all_data["users"]:
        new_id = generate_unique_id()

    all_data["users"][new_id] = {
        "nickname": nickname[:15],
        "player": {"xp": 0, "level": 1, "completed_total": 0},
        "habits": []
    }
    save_all_data(all_data)
    session["user_id"] = new_id
    flash(f"Добро пожаловать, {nickname}! Твой ретро-код сохранения: {new_id}", "success")
    return redirect(url_for("index"))


@app.route("/login", methods=["POST"])
def login():
    """Вход по ID сохранения с другого браузера или устройства."""
    user_id = request.form.get("user_id", "").strip().upper()
    all_data = load_all_data()

    if user_id in all_data["users"]:
        session["user_id"] = user_id
        flash(f"Картридж вставлен! С возвращением, {all_data['users'][user_id]['nickname']}!", "success")
    else:
        flash("Герой с таким ID не найден на картридже!", "error")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))


@app.route("/add", methods=["POST"])
def add_habit():
    all_data = load_all_data()
    user_id, user_data = get_current_user(all_data)
    if not user_data:
        return redirect(url_for("index"))

    name = request.form.get("name", "").strip()
    if not name:
        flash("Имя квеста не может быть пустым!", "error")
        return redirect(url_for("index"))

    if any(h["name"].lower() == name.lower() for h in user_data["habits"]):
        flash("Такой квест уже записан в свитке!", "error")
        return redirect(url_for("index"))

    user_data["habits"].append({
        "name": name,
        "streak": 0,
        "best_streak": 0,
        "last_completed": None
    })

    if add_xp(user_data["player"], 15):
        flash(f"Квест добавлен! (+15 XP). LEVEL UP! Твой уровень: Lv.{user_data['player']['level']}!", "levelup")
    else:
        flash(f"Квест «{name}» добавлен в свиток! (+15 XP)", "success")

    save_all_data(all_data)
    return redirect(url_for("index"))


@app.route("/complete/<int:habit_id>")
def complete_habit(habit_id: int):
    all_data = load_all_data()
    user_id, user_data = get_current_user(all_data)
    if not user_data:
        return redirect(url_for("index"))

    habits = user_data["habits"]
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
        user_data["player"]["completed_total"] = user_data["player"].get("completed_total", 0) + 1

        reward = 30 + (h["streak"] * 5)
        lvl_up = add_xp(user_data["player"], reward)
        save_all_data(all_data)

        if lvl_up:
            flash(f"ПОБЕДА! «{h['name']}» закрыт! (+{reward} XP). LEVEL UP!", "levelup")
        else:
            flash(f"Победа! «{h['name']}» выполнен! Комбо: x{h['streak']} (+{reward} XP)", "success")

    return redirect(url_for("index"))


@app.route("/reset/<int:habit_id>")
def reset_habit(habit_id: int):
    all_data = load_all_data()
    user_id, user_data = get_current_user(all_data)
    if user_data and 0 <= habit_id < len(user_data["habits"]):
        user_data["habits"][habit_id]["streak"] = 0
        user_data["habits"][habit_id]["last_completed"] = None
        save_all_data(all_data)
        flash("Комбо квеста обнулено.", "info")
    return redirect(url_for("index"))


@app.route("/delete/<int:habit_id>")
def delete_habit(habit_id: int):
    all_data = load_all_data()
    user_id, user_data = get_current_user(all_data)
    if user_data and 0 <= habit_id < len(user_data["habits"]):
        deleted = user_data["habits"].pop(habit_id)
        save_all_data(all_data)
        flash(f"Квест «{deleted['name']}» сожжен!", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)