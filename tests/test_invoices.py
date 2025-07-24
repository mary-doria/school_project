import pytest
import uuid
import sqlalchemy
from httpx import AsyncClient, ASGITransport
from fastapi import status
from app.main import app
from app.database import engine

def limpiar_base_de_datos():
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("DELETE FROM invoices"))
        conn.execute(sqlalchemy.text("DELETE FROM students"))
        conn.execute(sqlalchemy.text("DELETE FROM schools"))
        conn.commit()

async def crear_colegio(ac, nombre="Colegio Factura"):
    resp = await ac.post("/api/schools/", json={
        "name": nombre,
        "address": "Cra 1 # 2-3",
        "phone": "3001112233"
    })
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.json()["id"]

async def crear_estudiante(ac, nombre="Estudiante Factura", email=None, school_id=1):
    email = email or f"{uuid.uuid4()}@test.com"
    resp = await ac.post("/api/students/", json={
        "name": nombre,
        "email": email,
        "school_id": school_id
    })
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.json()["id"]

@pytest.mark.asyncio
async def test_create_invoice():
    limpiar_base_de_datos()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        school_id = await crear_colegio(ac)
        student_id = await crear_estudiante(ac, school_id=school_id)
        factura_data = {
            "amount": 500000,
            "description": "Matrícula primer semestre",
            "student_id": student_id
        }
        invoice_resp = await ac.post("/api/invoices/", json=factura_data)
        assert invoice_resp.status_code == status.HTTP_200_OK
        data = invoice_resp.json()
        assert data["amount"] == factura_data["amount"]
        assert data["student_id"] == student_id
        assert data["paid"] is False

@pytest.mark.asyncio
async def test_list_invoices():
    limpiar_base_de_datos()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        school_id = await crear_colegio(ac)
        student_id = await crear_estudiante(ac, school_id=school_id)
        await ac.post("/api/invoices/", json={
            "amount": 500000,
            "description": "Matrícula primer semestre",
            "student_id": student_id
        })
        list_resp = await ac.get("/api/invoices/")
        assert list_resp.status_code == status.HTTP_200_OK
        data = list_resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["student_id"] == student_id

@pytest.mark.asyncio
async def test_delete_invoice():
    limpiar_base_de_datos()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        school_id = await crear_colegio(ac)
        student_id = await crear_estudiante(ac, school_id=school_id)
        create_resp = await ac.post("/api/invoices/", json={
            "amount": 500000,
            "description": "Matrícula primer semestre",
            "student_id": student_id
        })
        invoice_id = create_resp.json()["id"]
        delete_resp = await ac.delete(f"/api/invoices/{invoice_id}")
        assert delete_resp.status_code == status.HTTP_200_OK
        assert delete_resp.json()["message"] == "Invoice deleted successfully"
        get_resp = await ac.get("/api/invoices/")
        data = get_resp.json()
        assert all(invoice["id"] != invoice_id for invoice in data)

@pytest.mark.asyncio
async def test_update_invoice():
    limpiar_base_de_datos()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        school_id = await crear_colegio(ac)
        student_id = await crear_estudiante(ac, school_id=school_id)
        create_resp = await ac.post("/api/invoices/", json={
            "amount": 500000,
            "description": "Matrícula primer semestre",
            "student_id": student_id
        })
        invoice_id = create_resp.json()["id"]
        update_resp = await ac.put(f"/api/invoices/{invoice_id}", json={
            "amount": 500000,
            "student_id": student_id,
            "paid": True
        })
        assert update_resp.status_code == status.HTTP_200_OK
        data = update_resp.json()
        assert data["id"] == invoice_id
        assert data["paid"] is True
