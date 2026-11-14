import pytest
from vaultsense.invoice_vault import InvoiceTaxVault

def test_invoice_parsing_standard_tax():
    vault = InvoiceTaxVault()
    sample_text = """
    UGREEN Technology Ltd.
    Commercial Tax Invoice
    Invoice #: INV-2026-9812
    VAT Number: GB123456789
    Date: November 10, 2026

    Item: UGREEN NAS DXP4800 Plus Pro 4-Bay AI Server
    Quantity: 2
    Subtotal: $1,400.00
    Total Amount: $1,540.00
    Payment Due: Upon Receipt
    """

    res = vault.parse_invoice_text(sample_text, source_file="nas_purchase.txt")
    assert res["invoice_number"] == "INV-2026-9812"
    assert "GB123456789" in res["tax_identifier"]
    assert res["total_amount"] == 1540.00
    assert res["currency"] == "USD"
    assert res["expense_category"] == "Cloud & Hosting"
    assert res["tax_deductible"] is True
    assert res["estimated_tax_vat"] > 0

def test_invoice_software_subscription():
    vault = InvoiceTaxVault()
    sample_text = """
    GitHub Enterprise Cloud Subscription
    Bill #: GH-SUB-4411
    Tax ID: 94-2849182
    Total Due: $210.50
    """
    res = vault.parse_invoice_text(sample_text, source_file="github_bill.txt")
    assert res["invoice_number"] == "GH-SUB-4411"
    assert res["total_amount"] == 210.50
    assert res["expense_category"] == "Software"
    assert res["tax_deductible"] is True
