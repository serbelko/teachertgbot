# как использовать

from teachertgbot.handlers.session import SessionLocal
from teachertgbot.handlers.base_using import PlanRepository

db = SessionLocal()
repo = PlanRepository(db)


def something():
    new_plan =repo.add_plan(user_id="123", text="Изучить SQLAlchemy")

    fetched_plan = repo.get_plan_by_id(new_plan.id)


def get_text(user_id):
    plans = repo.get_plan_by_id(user_id)
    if plans:
        return [{"label": plan.name, "text": plan.text} for plan in plans]
    else:
        return {"label": "Нет сценариев", "text": "Вы еще не создали сценариев."}
    
def get_top_users(user_id):
    top_users = repo.get_top_users_by_id(user_id)
    if top_users:
        return [{"name": user.name, "plans_count": user.plans_count} for user in top_users]
    else:
        return ['тут пока никого нет :(']
