from sqlalchemy import Column,String,Integer,ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class FavoriteExercise(Base):
    __tablename__="favorite_exercises" #Name of table in PostgreSQL

    __table_args__=(
        UniqueConstraint("user_id","name",name="uq_favorite_exercise_user_name"),
    )

    #primary key
    id=Column(Integer,primary_key=True,index=True)

    #fields
    name=Column(String(100),nullable=False)

    #links favorite to a user
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    #lets you do favorite.user in python
    user=relationship("User",back_populates="favorite_exercises")
