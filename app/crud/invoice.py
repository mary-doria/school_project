from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate
from fastapi import HTTPException, status


def create_invoice(db: Session, invoice: InvoiceCreate):
    try:
        db_invoice = Invoice(**invoice.dict())
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        return db_invoice
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_es": "Ocurrió un error al crear la factura.",
                "error_en": "An error occurred while creating the invoice.",
                "details": str(e)
            }
        )


def get_invoices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Invoice).offset(skip).limit(limit).all()


def get_invoice(db: Session, invoice_id: int):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_es": f"No se encontró la factura con ID {invoice_id}.",
                "error_en": f"Invoice with ID {invoice_id} was not found."
            }
        )
    return invoice


def update_invoice(db: Session, invoice_id: int, updated_invoice: InvoiceCreate):
    invoice = get_invoice(db, invoice_id)
    try:
        for key, value in updated_invoice.dict().items():
            setattr(invoice, key, value)
        db.commit()
        db.refresh(invoice)
        return invoice
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_es": "Ocurrió un error al actualizar la factura.",
                "error_en": "An error occurred while updating the invoice.",
                "details": str(e)
            }
        )


def delete_invoice(db: Session, invoice_id: int):
    invoice = get_invoice(db, invoice_id)
    try:
        db.delete(invoice)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_es": "Ocurrió un error al eliminar la factura.",
                "error_en": "An error occurred while deleting the invoice.",
                "details": str(e)
            }
        )
