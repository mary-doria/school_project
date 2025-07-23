from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.school import SchoolCreate, SchoolResponse
from app.crud import school as crud_school
from app.database import SessionLocal

router = APIRouter(prefix="/schools", tags=["Schools"])

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
