from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.invoice import InvoiceCreate, InvoiceResponse
from app.crud import invoice as crud_invoice
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=InvoiceResponse)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    return crud_invoice.create_invoice(db, invoice)

@router.get("/", response_model=list[InvoiceResponse])
def read_invoices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_invoice.get_invoices(db, skip, limit)

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def read_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return crud_invoice.get_invoice(db, invoice_id)

@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(invoice_id: int, invoice: InvoiceCreate, db: Session = Depends(get_db)):
    return crud_invoice.update_invoice(db, invoice_id, invoice)

@router.delete("/{invoice_id}", response_model=dict)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    crud_invoice.delete_invoice(db, invoice_id)
    return {"message": "Invoice deleted successfully"}
