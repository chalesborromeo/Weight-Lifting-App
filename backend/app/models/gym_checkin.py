from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class GymCheckIn(Base):
    __tablename__ = "gym_checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    gym_name = Column(String(200), nullable=False)
    gym_address = Column(String(200), nullable=True)
    checked_in_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="checkins")
