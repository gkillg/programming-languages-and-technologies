"""
Веб-трекер привычек "Habby" (Мультипользовательская версия)
Дисциплина: Языки и технология программирования (СРО)
"""

import calendar
import json
import os
import random
import string
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

app = Flask(__name__)
app.secret_key = "habby_retro_multiuser_secret_key"
DATA_FILE = "habby_save.json"

# Конфигурация накопительной системы бонусов и достижений
ACHIEVEMENTS_CONFIG = [
    {
        "id": "streak_7",
        "tier": "weekly",
        "type": "streak",
        "threshold": 7,
        "icon": "[7D]",
        "title": "Недельный воин",
        "description": "Серия 7 дней подряд",
        "bonus_xp": 100,
        "status_grant": "Хранитель недели",
        "artifact": None,
    },
    {
        "id": "streak_30",
        "tier": "monthly",
        "type": "streak",
        "threshold": 30,
        "icon": "[30D]",
        "title": "Повелитель месяца",
        "description": "Серия 30 дней подряд",
        "bonus_xp": 500,
        "status_grant": "Мастер ритма",
        "artifact": "Золотой картридж DMG",
    },
    {
        "id": "streak_100",
        "tier": "epic",
        "type": "streak",
        "threshold": 100,
        "icon": "[100D]",
        "title": "Центурион привычек",
        "description": "Серия 100 дней подряд",
        "bonus_xp": 1500,
        "status_grant": "8-бит Титан",
        "artifact": "Пиксельная корона",
    },
    {
        "id": "streak_365",
        "tier": "yearly",
        "type": "streak",
        "threshold": 365,
        "icon": "[365D]",
        "title": "Легенда Game Boy",
        "description": "Годовая серия: 365 дней подряд!",
        "bonus_xp": 5000,
        "status_grant": "Бессмертный чемпион",
        "artifact": "Платиновый Game Boy",
    },
    {
        "id": "total_10",
        "tier": "activity",
        "type": "total",
        "threshold": 10,
        "icon": "[10X]",
        "title": "Первые шаги",
        "description": "Выполнено 10 квестов суммарно",
        "bonus_xp": 50,
        "status_grant": None,
        "artifact": None,
    },
    {
        "id": "total_50",
        "tier": "activity",
        "type": "total",
        "threshold": 50,
        "icon": "[50X]",
        "title": "Стабильный комбо",
        "description": "Выполнено 50 квестов суммарно",
        "bonus_xp": 250,
        "status_grant": "Адепт дисциплины",
        "artifact": "Турбо-кнопка",
    },
    {
        "id": "total_100",
        "tier": "yearly",
        "type": "total",
        "threshold": 100,
        "icon": "[100X]",
        "title": "Мастер аркады",
        "description": "Выполнено 100 квестов суммарно",
        "bonus_xp": 600,
        "status_grant": "Грандмастер",
        "artifact": "Кристалл упорства",
    },
]


def generate_unique_id() -> str:
    digits = "".join(random.choices(string.digits, k=4))
    return f"HB-{digits}"


def load_all_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) and "users" in data else {"users": {}}
    except (json.JSONDecodeError, OSError):
        return {"users": {}}


def save_all_data(data: dict) -> None:
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"[Критическая ошибка сохранения]: {e}")


def ensure_user_schema(user_data: dict) -> None:
    today_str = date.today().isoformat()
    player = user_data.setdefault("player", {"xp": 0, "level": 1, "completed_total": 0})
    player.setdefault("completed_total", 0)
    player.setdefault("status", "Новичок")
    player.setdefault("artifacts", [])

    user_data.setdefault("habits", [])
    user_data.setdefault("achievements", [])
    user_data.setdefault("last_active_date", today_str)
    user_data.setdefault("daily_log", {"date": today_str, "entries": []})
    user_data.setdefault("daily_archive", {})
    user_data.setdefault("history", {})

    for h in user_data["habits"]:
        h.setdefault("streak", 0)
        h.setdefault("best_streak", h.get("streak", 0))
        h.setdefault("last_completed", None)
        if "created_at" not in h:
            last_comp = h.get("last_completed")
            h["created_at"] = min(today_str, last_comp) if last_comp else today_str


def get_current_user(all_data: dict) -> tuple:
    user_id = session.get("user_id")
    if not user_id or user_id not in all_data["users"]:
        return None, None
    user_data = all_data["users"][user_id]
    ensure_user_schema(user_data)
    return user_id, user_data


def process_day_rollover(user_data: dict) -> bool:
    today = date.today()
    today_str = today.isoformat()
    yesterday_str = (today - timedelta(days=1)).isoformat()
    changed = False

    daily_log = user_data["daily_log"]
    log_date = daily_log.get("date", today_str)
    if log_date != today_str:
        if daily_log.get("entries"):
            user_data["daily_archive"][log_date] = daily_log["entries"]
        user_data["daily_log"] = {"date": today_str, "entries": []}
        changed = True

    last_active_str = user_data.get("last_active_date", today_str)
    try:
        cursor = date.fromisoformat(last_active_str)
    except ValueError:
        cursor = today

    if cursor < today:
        while cursor < today:
            d_str = cursor.isoformat()
            day_hist = user_data["history"].setdefault(d_str, {"completed": [], "missed": []})
            completed_names = {c["name"].lower() for c in day_hist["completed"]}

            missed_list = []
            for h in user_data["habits"]:
                created_at = h.get("created_at", d_str)
                if created_at <= d_str and h["name"].lower() not in completed_names:
                    missed_list.append({"name": h["name"]})

            day_hist["missed"] = missed_list
            cursor += timedelta(days=1)

        user_data["last_active_date"] = today_str
        changed = True

    for habit in user_data["habits"]:
        last = habit.get("last_completed")
        if last and last != today_str and last != yesterday_str and habit.get("streak", 0) != 0:
            habit["streak"] = 0
            changed = True

    return changed


def add_xp(player: dict, amount: int) -> bool:
    player["xp"] += amount
    req_xp = player["level"] * 60
    leveled_up = False
    while player["xp"] >= req_xp:
        player["level"] += 1
        player["xp"] -= req_xp
        req_xp = player["level"] * 60
        leveled_up = True
    return leveled_up


def check_and_grant_achievements(user_data: dict, current_streak: int) -> tuple[list, bool]:
    unlocked_ids = {a["id"] for a in user_data["achievements"]}
    newly_unlocked = []
    bonus_level_up = False
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    completed_total = user_data["player"].get("completed_total", 0)

    for cfg in ACHIEVEMENTS_CONFIG:
        if cfg["id"] in unlocked_ids:
            continue

        achieved = False
        if cfg["type"] == "streak" and current_streak >= cfg["threshold"]:
            achieved = True
        elif cfg["type"] == "total" and completed_total >= cfg["threshold"]:
            achieved = True

        if achieved:
            if cfg["status_grant"]:
                user_data["player"]["status"] = cfg["status_grant"]
            if cfg["artifact"] and cfg["artifact"] not in user_data["player"]["artifacts"]:
                user_data["player"]["artifacts"].append(cfg["artifact"])

            record = {
                "id": cfg["id"],
                "tier": cfg["tier"],
                "icon": cfg["icon"],
                "title": cfg["title"],
                "description": cfg["description"],
                "bonus_xp": cfg["bonus_xp"],
                "status_grant": cfg["status_grant"],
                "artifact": cfg["artifact"],
                "unlocked_at": now_str,
            }
            user_data["achievements"].append(record)
            if add_xp(user_data["player"], cfg["bonus_xp"]):
                bonus_level_up = True
            newly_unlocked.append(record)

    return newly_unlocked, bonus_level_up


def build_calendar_month(user_data: dict, year: int, month: int) -> dict:
    today = date.today()
    today_str = today.isoformat()
    _, days_in_month = calendar.monthrange(year, month)
    first_weekday = date(year, month, 1).weekday()

    days = []
    for day_num in range(1, days_in_month + 1):
        d = date(year, month, day_num)
        d_str = d.isoformat()
        hist = user_data["history"].get(d_str)

        completed_count = len(hist["completed"]) if hist else 0
        missed_count = len(hist["missed"]) if hist else 0

        if d > today:
            status = "future"
        elif d == today:
            total_now = len(user_data["habits"])
            done_now = sum(1 for h in user_data["habits"] if h.get("last_completed") == today_str)
            completed_count = done_now
            missed_count = max(0, total_now - done_now)
            if total_now > 0 and done_now == total_now:
                status = "done"
            elif done_now > 0:
                status = "partial"
            else:
                status = "pending"
        else:
            if completed_count > 0 and missed_count == 0:
                status = "done"
            elif completed_count > 0 and missed_count > 0:
                status = "partial"
            elif missed_count > 0:
                status = "missed"
            else:
                status = "empty"

        days.append({
            "date": d_str,
            "day": day_num,
            "status": status,
            "completed_count": completed_count,
            "missed_count": missed_count,
        })

    return {
        "year": year,
        "month": month,
        "first_weekday": first_weekday,
        "days": days,
    }


def build_heatmap_days(user_data: dict, weeks: int = 12) -> list:
    today = date.today()
    today_str = today.isoformat()
    total_days = weeks * 7
    start_date = today - timedelta(days=total_days - 1 - (6 - today.weekday()))

    cells = []
    for offset in range(total_days):
        d = start_date + timedelta(days=offset)
        d_str = d.isoformat()
        hist = user_data["history"].get(d_str)

        if d > today:
            status = "future"
            c_cnt, m_cnt = 0, 0
        elif d == today:
            total_now = len(user_data["habits"])
            c_cnt = sum(1 for h in user_data["habits"] if h.get("last_completed") == today_str)
            m_cnt = max(0, total_now - c_cnt)
            status = "done" if (total_now > 0 and c_cnt == total_now) else ("partial" if c_cnt > 0 else "pending")
        elif hist:
            c_cnt = len(hist["completed"])
            m_cnt = len(hist["missed"])
            if c_cnt > 0 and m_cnt == 0:
                status = "done"
            elif c_cnt > 0 and m_cnt > 0:
                status = "partial"
            elif m_cnt > 0:
                status = "missed"
            else:
                status = "empty"
        else:
            status = "empty"
            c_cnt, m_cnt = 0, 0

        cells.append({
            "date": d_str,
            "status": status,
            "completed_count": c_cnt,
            "missed_count": m_cnt,
        })
    return cells


@app.route("/")
def index():
    all_data = load_all_data()
    user_id, user_data = get_current_user(all_data)

    if not user_data:
        return render_template("login.html")

    process_day_rollover(user_data)
    save_all_data(all_data)

    today = date.today()
    today_str = today.isoformat()
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

    daily_log = user_data["daily_log"]
    daily_summary_text = ", ".join(
        f"{e['habit_name']} — {e['time']}" for e in daily_log["entries"]
    )
    unlocked_map = {a["id"]: a for a in user_data["achievements"]}
    achievements_view = [
        {
            **cfg,
            "unlocked": cfg["id"] in unlocked_map,
            "unlocked_at": unlocked_map[cfg["id"]]["unlocked_at"] if cfg["id"] in unlocked_map else None,
        }
        for cfg in ACHIEVEMENTS_CONFIG
    ]
    calendar_month = build_calendar_month(user_data, today.year, today.month)
    heatmap_cells = build_heatmap_days(user_data, weeks=12)

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
        current_filter=filter_type,
        daily_log=daily_log,
        daily_summary_text=daily_summary_text,
        daily_archive=user_data["daily_archive"],
        achievements=achievements_view,
        calendar_month=calendar_month,
        heatmap_cells=heatmap_cells,
    )


@app.route("/register", methods=["POST"])
def register():
    nickname = request.form.get("nickname", "").strip()
    if not nickname:
        flash("Введи имя героя!", "error")
        return redirect(url_for("index"))

    all_data = load_all_data()
    new_id = generate_unique_id()
    while new_id in all_data["users"]:
        new_id = generate_unique_id()

    today_str = date.today().isoformat()
    all_data["users"][new_id] = {
        "nickname": nickname[:15],
        "player": {
            "xp": 0,
            "level": 1,
            "completed_total": 0,
            "status": "Новичок",
            "artifacts": [],
        },
        "habits": [],
        "achievements": [],
        "last_active_date": today_str,
        "daily_log": {"date": today_str, "entries": []},
        "daily_archive": {},
        "history": {},
    }
    save_all_data(all_data)
    session["user_id"] = new_id
    flash(f"Добро пожаловать, {nickname}! Твой ретро-код сохранения: {new_id}", "success")
    return redirect(url_for("index"))


@app.route("/login", methods=["POST"])
def login():
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

    process_day_rollover(user_data)

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
        "last_completed": None,
        "created_at": date.today().isoformat(),
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

    process_day_rollover(user_data)

    habits = user_data["habits"]
    if 0 <= habit_id < len(habits):
        h = habits[habit_id]
        today_str = date.today().isoformat()
        yesterday_str = (date.today() - timedelta(days=1)).isoformat()
        now_time = datetime.now().strftime("%H:%M")

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

        user_data["daily_log"]["entries"].append({
            "habit_name": h["name"],
            "time": now_time,
            "xp": reward,
            "streak": h["streak"],
        })

        day_hist = user_data["history"].setdefault(today_str, {"completed": [], "missed": []})
        day_hist["completed"].append({
            "name": h["name"],
            "time": now_time,
            "xp": reward,
        })
        day_hist["missed"] = [m for m in day_hist["missed"] if m["name"].lower() != h["name"].lower()]

        newly_unlocked, bonus_lvl_up = check_and_grant_achievements(user_data, h["streak"])
        save_all_data(all_data)

        if lvl_up or bonus_lvl_up:
            flash(f"ПОБЕДА! «{h['name']}» закрыт в {now_time}! (+{reward} XP). LEVEL UP!", "levelup")
        else:
            flash(f"Победа! «{h['name']}» выполнен в {now_time}! Комбо: x{h['streak']} (+{reward} XP)", "success")

        for ach in newly_unlocked:
            extra = f" | Артефакт: {ach['artifact']}" if ach["artifact"] else ""
            extra += f" | Статус: {ach['status_grant']}" if ach["status_grant"] else ""
            flash(f"ТРОФЕЙ ОТКРЫТ: «{ach['title']}» (+{ach['bonus_xp']} XP{extra})!", "levelup")

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


@app.route("/api/calendar")
def api_calendar():
    all_data = load_all_data()
    user_id, user_data = get_current_user(all_data)
    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    today = date.today()
    year = request.args.get("year", default=today.year, type=int)
    month = request.args.get("month", default=today.month, type=int)
    if not (1 <= month <= 12):
        return jsonify({"error": "Invalid month"}), 400

    return jsonify(build_calendar_month(user_data, year, month))


@app.route("/api/day/<date_str>")
def api_day_details(date_str: str):
    all_data = load_all_data()
    user_id, user_data = get_current_user(all_data)
    if not user_data:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        target_date = date.fromisoformat(date_str)
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    today = date.today()
    today_str = today.isoformat()
    hist = user_data["history"].get(date_str, {"completed": [], "missed": []})

    completed = hist.get("completed", [])
    missed = hist.get("missed", [])

    if target_date == today:
        done_names = {c["name"].lower() for c in completed}
        missed = [
            {"name": h["name"]}
            for h in user_data["habits"]
            if h["name"].lower() not in done_names
        ]

    return jsonify({
        "date": date_str,
        "is_today": date_str == today_str,
        "completed": completed,
        "missed": missed,
        "archived_log": user_data["daily_archive"].get(date_str, []),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
