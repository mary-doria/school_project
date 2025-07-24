import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from app.main import app


async def crear_colegio(ac, nombre="Colegio Test", direccion="Cra 1 # 2-3", telefono="3001234567"):
    resp = await ac.post("/api/schools/", json={
        "name": nombre,
        "address": direccion,
        "phone": telefono
    })
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.json()


@pytest.mark.asyncio
async def test_create_school():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        data = await crear_colegio(ac)
        assert data["name"] == "Colegio Test"


@pytest.mark.asyncio
async def test_get_schools():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/schools/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_school():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:

        school = await crear_colegio(ac, nombre="Colegio Temporal", direccion="Cra 2 # 3-4", telefono="3000000000")
        school_id = school["id"]


        update_resp = await ac.put(f"/api/schools/{school_id}", json={
            "name": "Colegio Actualizado",
            "address": "Cra 5 # 6-7",
            "phone": "3109876543"
        })

        assert update_resp.status_code == status.HTTP_200_OK
        assert update_resp.json()["name"] == "Colegio Actualizado"


@pytest.mark.asyncio
async def test_delete_school():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:

        school = await crear_colegio(ac, nombre="Colegio a Eliminar", direccion="Cra 7 # 8-9", telefono="3112223344")
        school_id = school["id"]


        delete_resp = await ac.delete(f"/api/schools/{school_id}")
        assert delete_resp.status_code == status.HTTP_200_OK
        assert delete_resp.json()["message"] == "School deleted successfully"
