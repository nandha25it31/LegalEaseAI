import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = "gemini-3.1-flash-lite"
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing in the .env file."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ):
        prompt = f"""
You are a professional legal document drafting assistant.

Create a clear and professional legal document.

Document Type:
{document_type}

Parties Involved:
{parties}

Terms and Conditions:
{terms}

Effective Date:
{dates}

Create a professional title, identify all parties,
include the effective date, and convert the terms into
proper legal clauses.

Include suitable sections such as:
Introduction
Parties
Purpose
Terms and Conditions
Responsibilities
Confidentiality where applicable
Termination where applicable
General Provisions
Signatures

Do not invent personal information.
Use clear and professional language.
Return only the legal document content.

This document is AI-generated and should be reviewed
by a qualified legal professional before actual legal use.
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_level="low"
                )
            )
        )

        if not response or not response.text:
            raise ValueError(
                "Gemini did not return any document content."
            )

        return response.text