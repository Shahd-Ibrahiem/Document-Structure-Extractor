import os
import io
import json
import base64
from typing import Union, Tuple
from dotenv import load_dotenv
from pypdf import PdfReader
from PIL import Image

from groq import Groq
from openai import OpenAI
from src.schemas import InvoiceExtraction, KeyInformationExtraction

load_dotenv()

class DocumentExtractorEngine:
    def __init__(self, groq_key: str = None, openai_key: str = None):
        self.groq_key = groq_key or os.getenv("GROQ_API_KEY")
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")
        
        if self.groq_key:
            self.groq_client = Groq(api_key=self.groq_key)
        else:
            self.groq_client = None

        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
        else:
            self.openai_client = None

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extract raw text from PDF document."""
        reader = PdfReader(io.BytesIO(pdf_bytes))
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        return extracted_text.strip()

    def encode_image_to_base64(self, image_bytes: bytes) -> str:
        """Encode image file bytes to base64 string for Vision API."""
        return base64.b64encode(image_bytes).decode('utf-8')

    def extract_structured_data(
        self, 
        file_bytes: bytes, 
        file_type: str, 
        extraction_target: str = "Invoice"
    ) -> Tuple[Union[InvoiceExtraction, KeyInformationExtraction], str]:
        """
        Parses PDF or Image file bytes and extracts structured JSON using schema rules.
        """
        target_schema = InvoiceExtraction if extraction_target == "Invoice" else KeyInformationExtraction

        # Determine if file is PDF (text-based) or Image (vision-based)
        if file_type == "application/pdf":
            raw_text = self.extract_text_from_pdf(file_bytes)
            if not raw_text or len(raw_text) < 10:
                raise ValueError("Could not extract readable text from PDF. If this is a scanned PDF, convert it to an image.")

            meta_prompt = f"""
            You are an expert Document Processing AI system.
            Extract all requested fields from the following document text into strict JSON format.
            
            Document Text:
            "{raw_text}"
            
            JSON Schema Specification:
            {json.dumps(target_schema.model_json_schema(), indent=2)}
            """

            # Use Groq for fast text schema extraction
            if self.groq_client:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": meta_prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                raw_json = response.choices[0].message.content
                parsed = target_schema.model_validate_json(raw_json)
                return parsed, raw_text

            elif self.openai_client:
                response = self.openai_client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": meta_prompt}],
                    response_format=target_schema,
                    temperature=0.1
                )
                return response.choices[0].message.parsed, raw_text
            else:
                raise ValueError("No valid Groq or OpenAI API key available.")

        elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
            base64_img = self.encode_image_to_base64(file_bytes)
            
            # Vision Extraction via OpenAI gpt-4o-mini
            if not self.openai_client:
                raise ValueError("OpenAI API key is required for Vision image processing.")

            prompt_text = f"""
            Analyze the attached image document and extract information matching this strict JSON Schema:
            {json.dumps(target_schema.model_json_schema(), indent=2)}
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:{file_type};base64,{base64_img}"}
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            raw_json = response.choices[0].message.content
            parsed = target_schema.model_validate_json(raw_json)
            return parsed, "[Visual Image Input Processed]"

        else:
            raise ValueError(f"Unsupported file type: {file_type}")