from fastapi import FastAPI
from app.routes import school, student, invoice
from app.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Management API",
    description="API para gestionar colegios, estudiantes y facturas",
    version="1.0.0"
)


app.include_router(school.router, prefix="/api/schools", tags=["Schools"])
app.include_router(student.router, prefix="/api/students", tags=["Students"])
app.include_router(invoice.router, prefix="/api/invoices", tags=["Invoices"])


@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}
