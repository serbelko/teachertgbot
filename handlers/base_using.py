from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from teachertgbot.handlers.schemas import PlanORM, Base


class PlanRepository:
    def __init__(self, db: Session):
        self.db = db
        Base.metadata.create_all(db.bind)

    def add_plan(self, user_id: str, text: str) -> PlanORM:
        """Добавляет новый план в базу данных."""
        plan_id = uuid4()
        new_plan = PlanORM(id=plan_id, user_id=user_id, text=text)

        self.db.add(new_plan)
        self.db.commit()
        self.db.refresh(new_plan)

        return new_plan.to_dict()

    def get_plan_by_user_id(self, user_id: UUID) -> Optional[PlanORM]:
        """Получает план по его ID."""
        return self.db.query(PlanORM).filter(PlanORM.id == user_id).first()
