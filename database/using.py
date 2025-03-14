# как использовать

from session import SessionLocal
from base_using import PlanRepository

db = SessionLocal()
repo = PlanRepository(db)


def something():
    new_plan =repo.add_plan(user_id="123", text="Изучить SQLAlchemy")

    fetched_plan = repo.get_plan_by_id(new_plan.id)