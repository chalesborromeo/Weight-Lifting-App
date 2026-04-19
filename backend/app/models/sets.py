from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Set(Base):
    __tablename__ = "sets"

    # primary key
    id=Column(Integer, primary_key=True, autoincrement=True)

    # fields
    reps=Column(Integer, nullable=False)
    weight=Column(Float, nullable=False)

    exercise_id=Column(Integer, ForeignKey("exercises.id"), nullable=False)

    # relationships
    exercise=relationship("Exercise", back_populates="sets")
    

