from fastapi import FastAPI
from app.routes import school, student, invoice
from app.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Management API",
    description="API para gestionar colegios, estudiantes y facturas",
    version="1.0.0"
)

# Incluir routers
app.include_router(school.router)
app.include_router(student.router)
app.include_router(invoice.router)

@app.get("/")
def read_root():
    return {"message": "Hola Mundo"}
