from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.school import SchoolCreate, SchoolResponse
from app.crud import school as crud_school
from app.database import SessionLocal
from app.models.student import Student
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

@router.post("/", response_model=SchoolResponse)
def create_school(school: SchoolCreate, db: Session = Depends(get_db)):
    return crud_school.create_school(db, school)

@router.get("/", response_model=list[SchoolResponse])
def read_schools(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_school.get_schools(db, skip, limit)

@router.get("/{school_id}", response_model=SchoolResponse)
def read_school(school_id: int, db: Session = Depends(get_db)):
    return crud_school.get_school(db, school_id)

@router.put("/{school_id}", response_model=SchoolResponse)
def update_school(school_id: int, school: SchoolCreate, db: Session = Depends(get_db)):
    return crud_school.update_school(db, school_id, school)

@router.delete("/{school_id}", response_model=dict)
def delete_school(school_id: int, db: Session = Depends(get_db)):
    crud_school.delete_school(db, school_id)
    return {"message": "School deleted successfully"}
  
@router.get("/{school_id}/balance")
def get_school_balance(school_id: int, db: Session = Depends(get_db)):
    school = crud_school.get_school(db, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    students = db.query(Student).filter(Student.school_id == school_id).all()
    student_ids = [s.id for s in students]

    total_due = db.query(func.sum(Invoice.amount)).filter(
        Invoice.student_id.in_(student_ids),
        Invoice.paid == False
    ).scalar() or 0.0

    return {
        "school": school.name,
        "total_students": len(students),
        "total_due": total_due
    }

