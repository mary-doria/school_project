from sqlalchemy.orm import Session
from app.models.school import School
from app.schemas.school import SchoolCreate
from fastapi import HTTPException

def create_school(db: Session, school: SchoolCreate):
    db_school = School(**school.dict())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school

def get_schools(db: Session, skip: int = 0, limit: int = 10):
    return db.query(School).offset(skip).limit(limit).all()

def get_school(db: Session, school_id: int):
    return db.query(School).filter(School.id == school_id).first()

def update_school(db: Session, school_id: int, updated_school: SchoolCreate):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    for key, value in updated_school.dict().items():
        setattr(school, key, value)
    db.commit()
    db.refresh(school)
    return school

def delete_school(db: Session, school_id: int):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    db.delete(school)
    db.commit()