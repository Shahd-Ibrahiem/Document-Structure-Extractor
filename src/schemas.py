from pydantic import BaseModel, Field
from typing import List, Optional

# --- Invoice Extraction Schema ---
class LineItem(BaseModel):
    description: str = Field(description="Description of item or service")
    quantity: float = Field(default=1.0, description="Quantity purchased")
    unit_price: float = Field(default=0.0, description="Price per unit")
    total_amount: float = Field(default=0.0, description="Total cost for this item")

class InvoiceExtraction(BaseModel):
    vendor_name: str = Field(default="Unknown Vendor", description="Name of vendor or issuing company")
    invoice_number: Optional[str] = Field(default=None, description="Invoice ID or receipt number")
    invoice_date: Optional[str] = Field(default=None, description="Date invoice was issued")
    currency: str = Field(default="USD", description="Currency symbol or code (e.g., USD, EUR, EGP)")
    line_items: List[LineItem] = Field(default_factory=list, description="Extracted individual items")
    subtotal: Optional[float] = Field(default=0.0, description="Subtotal amount before tax")
    tax_amount: Optional[float] = Field(default=0.0, description="Tax amount charged")
    total_amount: float = Field(default=0.0, description="Final total bill amount")
    confidence_score: float = Field(default=0.5, description="Confidence rating between 0.0 and 1.0 based on document clarity")
    extraction_notes: List[str] = Field(default_factory=list, description="Flags or ambiguities found during extraction")

# --- Generic Business Document / Contract Schema ---
class KeyValuePair(BaseModel):
    key: str = Field(description="Identified field name")
    value: str = Field(description="Extracted value corresponding to field")

class KeyInformationExtraction(BaseModel):
    document_type: str = Field(description="Detected document type (Invoice, Receipt, Contract, Resume, Form)")
    summary: str = Field(description="High-level 2-sentence summary of document contents")
    extracted_fields: List[KeyValuePair] = Field(description="List of key-value field pairs")
    confidence_score: float = Field(description="Confidence rating between 0.0 and 1.0")