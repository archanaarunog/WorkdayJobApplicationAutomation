import pytest
import httpx

# Import the FastAPI app
from src.main import app


@pytest.mark.asyncio
async def test_health_endpoint_ok():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data
        assert "API is running" in data["message"]


@pytest.mark.asyncio
async def test_jobs_list_public_ok():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/jobs/")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_applications_requires_auth():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # Missing Authorization header should yield 401
        resp = await client.post("/api/applications/", json={"job_id": 1})
        assert resp.status_code in (401, 403)
