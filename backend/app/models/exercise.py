from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Exercise(Base):
    __tablename__ = "exercises"

    # primary key
    id=Column(Integer, primary_key=True, autoincrement=True)

    # fields
    name=Column(String(100), nullable=False)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)

    # relationships
    sets=relationship("Set", back_populates="exercise")
    workout=relationship("Workout", back_populates="exercises")