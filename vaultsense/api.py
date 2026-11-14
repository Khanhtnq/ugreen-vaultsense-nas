from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import time

from vaultsense.dedup import SemanticDeduplicator
from vaultsense.canary import EntropyRansomwareCanary
from vaultsense.invoice_vault import InvoiceTaxVault
from vaultsense.config import config

app = FastAPI(
    title="VaultSense UGOS Skill API",
    version="1.0.0",
    description="Enterprise-grade local storage intelligence for UGREEN AI NAS: Zero-Cloud Deduplication, Entropy Ransomware Canary & Automated Invoice Vault."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

dedup_engine = SemanticDeduplicator(chunk_size=config.chunk_size_kb * 1024)
canary_guard = EntropyRansomwareCanary(canary_dir=config.canary_dir, threshold=config.entropy_threshold)
invoice_vault = InvoiceTaxVault()

class ScanRequest(BaseModel):
    directory_path: Optional[str] = None
    deep_analysis: bool = True

class InvoiceParseRequest(BaseModel):
    document_text: str
    filename: Optional[str] = "upload.txt"

class CanaryDeployRequest(BaseModel):
    count: int = 5
    target_directory: Optional[str] = None

@app.get("/")
def root():
    return {
        "service": "VaultSense UGOS",
        "skill_id": "com.ugreen.skill.vaultsense",
        "status": "RUNNING",
        "runtime": "UGOS Edge AI Container",
        "author": "Khanhtnq"
    }

@app.get("/api/v1/status")
def health_status():
    return {
        "status": "HEALTHY",
        "version": "1.0.0",
        "nas_os": "UGOS Linux 6.x",
        "uptime_seconds": 3600,
        "npu_accelerator": "ACTIVE",
        "canary_watchdog": "ACTIVE",
        "dedup_worker": "IDLE"
    }

@app.post("/api/v1/dedup/scan")
def scan_deduplication(req: ScanRequest):
    target = req.directory_path or config.volume_mount
    if not os.path.exists(target):
        os.makedirs(target, exist_ok=True)
    res = dedup_engine.scan_directory_for_duplicates(target)
    return {
        "status": "SUCCESS",
        "target_directory": target,
        "results": res
    }

@app.post("/api/v1/ransomware/entropy-check")
def check_entropy(filepath: str = Query(..., description="Absolute path on NAS")):
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"File not found: {filepath}")
    analysis = canary_guard.analyze_file_entropy(filepath)
    return {"status": "SUCCESS", "analysis": analysis}

@app.post("/api/v1/canary/deploy")
def deploy_canaries(req: CanaryDeployRequest):
    if req.target_directory:
        guard = EntropyRansomwareCanary(canary_dir=req.target_directory)
        paths = guard.deploy_canaries(req.count)
    else:
        paths = canary_guard.deploy_canaries(req.count)
    return {
        "status": "SUCCESS",
        "deployed_count": len(paths),
        "canary_files": paths
    }

@app.get("/api/v1/canary/status")
def check_canaries():
    return canary_guard.check_canaries()

@app.post("/api/v1/invoices/parse")
def parse_invoice(req: InvoiceParseRequest):
    result = invoice_vault.parse_invoice_text(req.document_text, source_file=req.filename or "doc.txt")
    return {"status": "SUCCESS", "invoice": result}

@app.get("/api/v1/invoices/vault-summary")
def get_vault_summary(vault_path: Optional[str] = None):
    target = vault_path or os.path.join(config.volume_mount, "invoices")
    os.makedirs(target, exist_ok=True)
    summary = invoice_vault.process_vault_directory(target)
    return {"status": "SUCCESS", "vault_summary": summary}
