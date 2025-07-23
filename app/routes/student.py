from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.student import StudentCreate, StudentResponse
from app.crud import student as crud_student
from app.database import SessionLocal

router = APIRouter(prefix="/students", tags=["Students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return crud_student.create_student(db, student)

@router.get("/", response_model=list[StudentResponse])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_student.get_students(db, skip, limit)

@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    return crud_student.get_student(db, student_id)
