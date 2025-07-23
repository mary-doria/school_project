from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate
from fastapi import HTTPException, status


def create_student(db: Session, student: StudentCreate):
    try:
        db_student = Student(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_es": "Ocurrió un error al crear el estudiante.",
                "error_en": "An error occurred while creating the student.",
                "details": str(e)
            }
        )


def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Student).offset(skip).limit(limit).all()


def get_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_es": f"No se encontró el estudiante con ID {student_id}.",
                "error_en": f"Student with ID {student_id} was not found."
            }
        )
    return student


def update_student(db: Session, student_id: int, updated_student: StudentCreate):
    student = get_student(db, student_id)
    try:
        for key, value in updated_student.dict().items():
            setattr(student, key, value)
        db.commit()
        db.refresh(student)
        return student
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_es": "Ocurrió un error al actualizar el estudiante.",
                "error_en": "An error occurred while updating the student.",
                "details": str(e)
            }
        )


def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)
    try:
        db.delete(student)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_es": "Ocurrió un error al eliminar el estudiante.",
                "error_en": "An error occurred while deleting the student.",
                "details": str(e)
            }
        )
