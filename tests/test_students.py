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



async def crear_colegio(ac, nombre="Colegio Default"):
    resp = await ac.post("/api/schools/", json={
        "name": nombre,
        "address": "Calle 123",
        "phone": "3100000000"
    })
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.json()["id"]



async def crear_estudiante(ac, nombre="Estudiante Default", email=None, school_id=1):
    email = email or f"{uuid.uuid4()}@test.com"
    resp = await ac.post("/api/students/", json={
        "name": nombre,
        "email": email,
        "school_id": school_id
    })
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.json()["id"], email


@pytest.mark.asyncio
async def test_create_student():
    limpiar_base_de_datos()
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        school_id = await crear_colegio(ac, "Colegio Test")
        email = f"{uuid.uuid4()}@estudiante.com"

        resp = await ac.post("/api/students/", json={
            "name": "Juan Pérez",
            "email": email,
            "school_id": school_id
        })

        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.json()
        assert "id" in data and data["email"] == email


@pytest.mark.asyncio
async def test_update_student():
    limpiar_base_de_datos()
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        school_id = await crear_colegio(ac, "Colegio Actualizar")
        student_id, email = await crear_estudiante(ac, "Estudiante Original", school_id=school_id)

        resp = await ac.put(f"/api/students/{student_id}", json={
            "name": "Estudiante Actualizado",
            "email": email,
            "age": 17,
            "school_id": school_id
        })

        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert data["name"] == "Estudiante Actualizado"
        assert data["email"] == email


@pytest.mark.asyncio
async def test_delete_student():
    limpiar_base_de_datos()
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        school_id = await crear_colegio(ac, "Colegio Eliminar")
        student_id, _ = await crear_estudiante(ac, "Estudiante Borrar", school_id=school_id)

        delete_resp = await ac.delete(f"/api/students/{student_id}")
        assert delete_resp.status_code == status.HTTP_200_OK
        assert delete_resp.json()["message"] == "Student deleted successfully"

        get_resp = await ac.get(f"/api/students/{student_id}")
        assert get_resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_list_students():
    limpiar_base_de_datos()
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        school_id = await crear_colegio(ac, "Colegio Listar")
        _, email = await crear_estudiante(ac, "Juan Pérez", school_id=school_id)

        list_resp = await ac.get("/api/students/")
        assert list_resp.status_code == status.HTTP_200_OK
        data = list_resp.json()

        assert isinstance(data, list)
        assert any(student["email"] == email for student in data)
