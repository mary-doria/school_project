from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    paid = Column(Boolean, default=False)
    student_id = Column(Integer, ForeignKey("students.id"))

    student = relationship("Student", back_populates="invoices")
