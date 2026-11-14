import pytest
from fastapi.testclient import TestClient
from vaultsense.api import app

client = TestClient(app)

def test_root_endpoint():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["service"] == "VaultSense UGOS"
    assert data["skill_id"] == "com.ugreen.skill.vaultsense"

def test_health_status():
    resp = client.get("/api/v1/status")
    assert resp.status_code == 200
    assert resp.json()["status"] == "HEALTHY"

def test_canary_deploy_and_check():
    resp = client.post("/api/v1/canary/deploy", json={"count": 2})
    assert resp.status_code == 200
    assert resp.json()["deployed_count"] == 2

    status_resp = client.get("/api/v1/canary/status")
    assert status_resp.status_code == 200
    assert "status" in status_resp.json()

def test_invoice_parse_endpoint():
    payload = {
        "document_text": "Invoice #: INV-TEST-001\nTotal: $350.00\nVAT: US9921827",
        "filename": "test.txt"
    }
    resp = client.post("/api/v1/invoices/parse", json=payload)
    assert resp.status_code == 200
    res = resp.json()["invoice"]
    assert res["invoice_number"] == "INV-TEST-001"
    assert res["total_amount"] == 350.00
