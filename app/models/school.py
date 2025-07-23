from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=True)

    students = relationship("Student", back_populates="school")
