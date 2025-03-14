from typing import Dict

from sqlalchemy import Column, Integer, String, Text, UUID, null
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class PlanORM(Base):
    __table__ = "plans"

    id = Column("plan_id", UUID, primary_key=True)
    user_id = Column("user_id", String, nullable=False, index=True)
    text = Column('text', Text)

    def to_dict(self) -> Dict:
        model_dict = {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "text": self.user_id
        }

    
