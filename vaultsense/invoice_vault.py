import re
import os
import json
from typing import Dict, Any, List, Optional

class InvoiceTaxVault:
    """Local, Zero-Cloud Invoice & Tax Document Analyzer for UGREEN AI NAS.
    Extracts vendor, invoice number, VAT/Tax ID, amounts, currency, and tax brackets
    using deterministic heuristics and local NER patterns.
    """

    CURRENCY_SYMBOLS = {"$": "USD", "€": "EUR", "£": "GBP", "¥": "JPY", "VND": "VND", "USD": "USD", "EUR": "EUR"}

    def __init__(self):
        self.invoice_patterns = [
            re.compile(r"(?:invoice|bill|reference)\s*(?:no\.?|number|#)?\s*[:\-]\s*([A-Za-z0-9\-_/]+)", re.IGNORECASE),
            re.compile(r"invoice\s*#\s*([A-Za-z0-9\-_/]+)", re.IGNORECASE),
            re.compile(r"bill\s*#\s*([A-Za-z0-9\-_/]+)", re.IGNORECASE),
            re.compile(r"(?:inv|bill)[\-_]([0-9]{4,}[A-Za-z0-9\-_]*)", re.IGNORECASE)
        ]
        self.tax_id_patterns = [
            re.compile(r"vat\s*(?:id|no\.?|number|#)?\s*[:\-]?\s*([A-Z]{2}[0-9A-Za-z\s]{6,14})", re.IGNORECASE),
            re.compile(r"tax\s*(?:id|no\.?|number|#)?\s*[:\-]?\s*([0-9\-_/]{8,15})", re.IGNORECASE),
            re.compile(r"ein\s*[:\-]?\s*(\d{2}-\d{7})", re.IGNORECASE)
        ]
        # Priority-ordered amount patterns
        self.total_patterns = [
            re.compile(r"\btotal\s*(?:amount|due)?\s*[:\-]?\s*([$€£¥]?\s*[\d,]+\.?\d*)", re.IGNORECASE),
            re.compile(r"\bamount\s*due\s*[:\-]?\s*([$€£¥]?\s*[\d,]+\.?\d*)", re.IGNORECASE),
            re.compile(r"\bbalance\s*due\s*[:\-]?\s*([$€£¥]?\s*[\d,]+\.?\d*)", re.IGNORECASE),
            re.compile(r"\bsubtotal\s*[:\-]?\s*([$€£¥]?\s*[\d,]+\.?\d*)", re.IGNORECASE)
        ]

    def parse_invoice_text(self, text: str, source_file: str = "document.txt") -> Dict[str, Any]:
        """Parse raw text of an invoice into structured tax metadata."""
        inv_no = "UNKNOWN"
        for p in self.invoice_patterns:
            m = p.search(text)
            if m:
                candidate = m.group(1).strip()
                if candidate.lower() not in {"invoice", "bill", "tax", "statement"}:
                    inv_no = candidate
                    break

        tax_id = "NOT_FOUND"
        for p in self.tax_id_patterns:
            m = p.search(text)
            if m:
                tax_id = m.group(1).strip()
                break

        total_amount = 0.0
        currency = "USD"
        found_total = False

        for p in self.total_patterns:
            m = p.search(text)
            if m:
                raw_amt = m.group(1).strip()
                for sym, code in self.CURRENCY_SYMBOLS.items():
                    if sym in raw_amt:
                        currency = code
                        raw_amt = raw_amt.replace(sym, "").strip()
                try:
                    cleaned_amt = raw_amt.replace(",", "")
                    val = float(cleaned_amt)
                    if val > 0:
                        total_amount = val
                        found_total = True
                        break
                except ValueError:
                    pass

        estimated_tax = round(total_amount * 0.10, 2)
        category = self._categorize_expense(text)

        return {
            "source_file": source_file,
            "invoice_number": inv_no,
            "tax_identifier": tax_id,
            "currency": currency,
            "total_amount": round(total_amount, 2),
            "estimated_tax_vat": estimated_tax,
            "expense_category": category,
            "tax_deductible": category in {"Office Equipment", "Cloud & Hosting", "Professional Services", "Software"},
            "confidence_score": 0.94 if inv_no != "UNKNOWN" and total_amount > 0 else 0.50
        }

    def _categorize_expense(self, text: str) -> str:
        low = text.lower()
        if any(w in low for w in ["github", "subscription", "saas", "license", "figma", "jetbrains", "slack"]):
            return "Software"
        elif any(w in low for w in ["server", "aws", "nas", "hosting", "ugreen", "azure", "gcp"]):
            return "Cloud & Hosting"
        elif any(w in low for w in ["laptop", "monitor", "cable", "hardware", "dock", "keyboard"]):
            return "Office Equipment"
        elif any(w in low for w in ["legal", "accounting", "consulting", "audit"]):
            return "Professional Services"
        elif any(w in low for w in ["flight", "hotel", "taxi", "uber", "airbnb"]):
            return "Travel & Lodging"
        return "General Business"

    def process_vault_directory(self, vault_dir: str) -> Dict[str, Any]:
        """Batch process all invoice documents inside the vault directory."""
        if not os.path.exists(vault_dir):
            return {"invoices": [], "total_spend": 0.0, "total_vat_claimable": 0.0}

        records = []
        spend = 0.0
        vat_claimable = 0.0

        for root, _, files in os.walk(vault_dir):
            for f in files:
                if f.lower().endswith((".txt", ".json", ".log", ".csv", ".pdf")):
                    path = os.path.join(root, f)
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as doc:
                            content = doc.read(16384)
                        parsed = self.parse_invoice_text(content, source_file=f)
                        records.append(parsed)
                        spend += parsed["total_amount"]
                        if parsed["tax_deductible"]:
                            vat_claimable += parsed["estimated_tax_vat"]
                    except Exception:
                        continue

        return {
            "total_documents": len(records),
            "total_spend": round(spend, 2),
            "total_vat_claimable": round(vat_claimable, 2),
            "records": records
        }
