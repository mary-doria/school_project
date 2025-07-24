from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)

    school_id = Column(Integer, ForeignKey("schools.id", ondelete="CASCADE"))


    school = relationship("School", back_populates="students")
    invoices = relationship("Invoice", back_populates="student")
