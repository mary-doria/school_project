from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.student import StudentCreate, StudentResponse
from app.crud import student as crud_student
from app.database import SessionLocal
from app.models.invoice import Invoice
from fastapi import HTTPException, status
from sqlalchemy import func 


router = APIRouter()

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

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    return crud_student.update_student(db, student_id, student)

@router.delete("/{student_id}", response_model=dict)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    crud_student.delete_student(db, student_id)
    return {"message": "Student deleted successfully"}

@router.get("/{student_id}/balance")
def get_student_balance(student_id: int, db: Session = Depends(get_db)):
    student = crud_student.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    total_due = db.query(func.sum(Invoice.amount)).filter(
        Invoice.student_id == student_id,
        Invoice.paid == False
    ).scalar() or 0.0

    invoices = db.query(Invoice).filter(Invoice.student_id == student_id).all()

    return {
        "student": student.name,
        "total_due": total_due,
        "invoices": [{"amount": i.amount, "paid": i.paid} for i in invoices]
    }

