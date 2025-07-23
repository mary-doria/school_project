from sqlalchemy.orm import Session
from app.models.school import School
from app.schemas.school import SchoolCreate
from fastapi import HTTPException, status


def create_school(db: Session, school: SchoolCreate):
    try:
        db_school = School(**school.dict())
        db.add(db_school)
        db.commit()
        db.refresh(db_school)
        return db_school
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_es": "Ocurrió un error al crear el colegio.",
                "error_en": "An error occurred while creating the school.",
                "details": str(e)
            }
        )


def get_schools(db: Session, skip: int = 0, limit: int = 10):
    return db.query(School).offset(skip).limit(limit).all()


def get_school(db: Session, school_id: int):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_es": f"No se encontró el colegio con ID {school_id}.",
                "error_en": f"School with ID {school_id} was not found."
            }
        )
    return school


def update_school(db: Session, school_id: int, updated_school: SchoolCreate):
    school = get_school(db, school_id)
    try:
        for key, value in updated_school.dict().items():
            setattr(school, key, value)
        db.commit()
        db.refresh(school)
        return school
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_es": "Ocurrió un error al actualizar el colegio.",
                "error_en": "An error occurred while updating the school.",
                "details": str(e)
            }
        )


def delete_school(db: Session, school_id: int):
    school = get_school(db, school_id)
    try:
        db.delete(school)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_es": "Ocurrió un error al eliminar el colegio.",
                "error_en": "An error occurred while deleting the school.",
                "details": str(e)
            }
        )
