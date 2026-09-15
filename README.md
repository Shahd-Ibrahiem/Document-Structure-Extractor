# 📄 Automated Structured Document Extractor

> An Intelligent Document Processing (IDP) system that parses unstructured PDFs, receipts, and images into schema-validated, type-safe JSON using Vision LLMs and Pydantic V2.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-V2-e91e63.svg)](https://docs.pydantic.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-ff4b4b.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Overview

Extracting unstructured data from business documents (invoices, receipts, contracts, resumes) often suffers from parsing errors, missing fields, and unpredictable output structures. 

**Automated Structured Document Extractor** solves this by combining multi-modal document extraction (PDF text parsing & Vision APIs) with strict **Pydantic V2** schemas. It guarantees that extracted JSON output strictly matches declared models, completes confidence evaluations, and flags missing or ambiguous field entries.

---

## ✨ Key Features

* 📄 **Multi-Modal Document Ingestion:** Handles native text-based PDFs via `pypdf` and visual document formats (`PNG`, `JPG`, `JPEG`) via Base64 Vision encoding.
* 🛡️ **Type-Safe Schema Enforcement:** Uses **Pydantic V2** models to guarantee structured, validated JSON payloads without missing parameters.
* 🔀 **Dynamic Extraction Targets:** Supports specialized schemas out-of-the-box (e.g., *Invoices & Line-Item Receipts* vs. *General Business Contracts*).
* 📊 **Confidence Scoring & Flagging:** Calculates confidence metrics and flags ambiguities or missing fields for human-in-the-loop audit trails.
* 🚀 **Multi-Provider LLM Integration:** Powered by **Groq** (`llama-3.3-70b`) for lightning-fast text JSON extraction and **OpenAI** (`gpt-4o-mini`) for visual image parsing.
* 💾 **Interactive GUI & JSON Export:** Features a Streamlit interface with preview panels, structured tables, and single-click JSON file downloads.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework / UI:** Streamlit, Pandas
* **Data Validation:** Pydantic V2
* **LLM & Vision Providers:** Groq API, OpenAI API
* **Document Processing:** PyPDF, Pillow (PIL)
* **Configuration:** `python-dotenv`

---

## 📂 Repository Structure

```text
document-structure-extractor/
├── .streamlit/
│   └── config.toml          # Custom dark UI styling for Streamlit
├── src/
│   ├── __init__.py          # Marks src as a Python package
│   ├── schemas.py           # Pydantic V2 models (Invoice, LineItems, KeyValue)
│   └── extractor.py         # Multi-modal extraction engine (PDF text & Vision APIs)
├── .env                     # API keys configuration (git-ignored)
├── .gitignore               # Ignored files (venv, env, cache)
├── app.py                   # Streamlit interactive application entry point
├── README.md                # Project documentation
└── requirements.txt         # Project dependencies
