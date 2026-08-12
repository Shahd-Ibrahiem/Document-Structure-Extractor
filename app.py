import streamlit as st
import json
import pandas as pd
from PIL import Image
import io

from src.extractor import DocumentExtractorEngine

st.set_page_config(
    page_title="Automated Document Extractor",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Automated Structured Document Extractor")
st.caption("Parse unstructured PDFs and images into validated, schema-enforced JSON using LLMs & Vision models.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings & API Keys")
    groq_key = st.text_input("Groq API Key", type="password", help="Used for PDF text extraction")
    openai_key = st.text_input("OpenAI API Key", type="password", help="Required for image vision processing")

    st.divider()
    extraction_target = st.radio(
        "Select Extraction Schema",
        ["Invoice", "General Business Document"],
        help="Choose specific Pydantic schema to enforce."
    )

col_file, col_result = st.columns([1, 1])

with col_file:
    st.subheader("📥 Upload Document")
    uploaded_file = st.file_uploader(
        "Upload a PDF invoice, receipt image, or contract:",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file:
        st.info(f"📁 **Filename:** {uploaded_file.name} | **Type:** {uploaded_file.type}")
        
        # Preview File
        if uploaded_file.type.startswith("image/"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Document Preview", use_container_width=True)
        elif uploaded_file.type == "application/pdf":
            st.warning("PDF uploaded. Text parsing engine active.")

with col_result:
    st.subheader("📤 Extracted Structured Data")
    
    if uploaded_file:
        process_btn = st.button("🚀 Process & Extract Schema", type="primary", use_container_width=True)

        if process_btn:
            with st.spinner("Extracting & validating fields against Pydantic schema..."):
                try:
                    engine = DocumentExtractorEngine(groq_key=groq_key, openai_key=openai_key)
                    file_bytes = uploaded_file.read()
                    
                    result, raw_text = engine.extract_structured_data(
                        file_bytes=file_bytes,
                        file_type=uploaded_file.type,
                        extraction_target=extraction_target
                    )

                    st.success("Extraction Successful!")

                    # Confidence Metric
                    confidence = getattr(result, "confidence_score", 1.0)
                    st.progress(confidence, text=f"Extraction Confidence: {int(confidence * 100)}%")

                    # Invoice View
                    if extraction_target == "Invoice":
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Vendor", result.vendor_name)
                        m2.metric("Date", result.invoice_date or "N/A")
                        m3.metric("Total", f"{result.total_amount} {result.currency}")

                        if result.line_items:
                            st.markdown("### 🛒 Line Items")
                            items_df = pd.DataFrame([item.model_dump() for item in result.line_items])
                            st.dataframe(items_df, use_container_width=True)

                    # General Document View
                    else:
                        st.markdown(f"**Document Type:** `{result.document_type}`")
                        st.markdown(f"**Summary:** {result.summary}")
                        
                        if result.extracted_fields:
                            st.markdown("### 🔑 Key Fields")
                            fields_df = pd.DataFrame([field.model_dump() for field in result.extracted_fields])
                            st.dataframe(fields_df, use_container_width=True)

                    # Raw JSON Export
                    st.divider()
                    json_data = json.dumps(result.model_dump(), indent=2, ensure_ascii=False)
                    st.download_button(
                        label="💾 Download Validated JSON",
                        data=json_data,
                        file_name=f"extracted_{uploaded_file.name.split('.')[0]}.json",
                        mime="application/json"
                    )

                    with st.expander("🔍 View Raw JSON Payload"):
                        st.json(result.model_dump())

                except Exception as e:
                    st.error(f"Extraction Error: {str(e)}")
    else:
        st.info("Please upload a file on the left panel to start.")