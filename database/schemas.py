from typing import Dict

from sqlalchemy import Column, Integer, String, Text, UUID, null
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class StudentORM(Base):
    __tablename__ = 'students'
    
    user_id = Column("student_id", UUID, primary_key=True)
    name = Column("email", String, nullable=False)
    
    def to_dict(self) -> Dict:
        model_dict = {
            "student_id": str(self.user_id),
            "name": self.name
        }
        return model_dict


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

    
