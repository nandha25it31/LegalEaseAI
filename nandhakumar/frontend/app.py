import streamlit as st
import requests

from utils.document_utils import (
    format_txt,
    format_docx,
    format_pdf,
    format_html_preview
)


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# -----------------------------
# Custom Styling
# -----------------------------

st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #777;
            margin-bottom: 30px;
        }

        .document-preview {
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #444;
            background-color: #111;
            color: white;
            max-height: 600px;
            overflow-y: auto;
        }

        .stButton button {
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Title
# -----------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Backend URL
# -----------------------------

BACKEND_URL = "http://127.0.0.1:8000"


# -----------------------------
# Input Section
# -----------------------------

st.subheader("📄 Create Your Legal Document")

document_type = st.text_input(
    "Document Type",
    placeholder="Example: Freelance Work Contract"
)

parties = st.text_area(
    "Parties Involved",
    placeholder="Example: John Doe (Freelancer), ABC Corp (Client)"
)

terms = st.text_area(
    "Terms & Conditions",
    placeholder=(
        "Enter terms separated by semicolons;\n"
        "Payment within 30 days;\n"
        "Confidentiality must be maintained;\n"
        "Either party may terminate with 15 days notice"
    )
)

dates = st.text_input(
    "Effective Date",
    placeholder="Example: 25/09/2026"
)


# -----------------------------
# Generate Button
# -----------------------------

if st.button("🚀 Generate Document"):

    if not document_type:
        st.warning("Please enter the document type.")

    elif not parties:
        st.warning("Please enter the parties involved.")

    elif not terms:
        st.warning("Please enter the terms and conditions.")

    elif not dates:
        st.warning("Please enter the effective date.")

    else:

        request_data = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates
        }

        try:

            with st.spinner("Generating your legal document..."):

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=request_data,
                    timeout=120
                )

            if response.status_code == 200:

                result = response.json()

                if result.get("success"):

                    st.session_state["document"] = result["document"]
                    st.session_state["document_type"] = document_type

                    st.success("✅ Document generated successfully!")

                else:
                    st.error("Document generation failed.")

            else:
                st.error(
                    f"Backend Error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Backend is not running. "
                "Please start FastAPI first."
            )

        except Exception as e:

            st.error(
                f"Something went wrong: {str(e)}"
            )


# -----------------------------
# Generated Document
# -----------------------------

if "document" in st.session_state:

    st.divider()

    st.subheader("📑 Generated Document")

    document = st.session_state["document"]

    # Preview
    st.markdown(
        '<div class="document-preview">',
        unsafe_allow_html=True
    )

    st.markdown(
        format_html_preview(document),
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.divider()

    # -------------------------
    # Edit Document
    # -------------------------

    st.subheader("✏️ Edit Document")

    edited_document = st.text_area(
        "Modify your document if required:",
        value=document,
        height=500
    )

    st.session_state["document"] = edited_document

    # -------------------------
    # Download Section
    # -------------------------

    st.subheader("⬇️ Download Document")

    col1, col2, col3 = st.columns(3)

    final_document = st.session_state["document"]
    final_type = st.session_state.get(
        "document_type",
        "Legal Document"
    )

    # TXT
    with col1:

        txt_data = format_txt(final_document)

        st.download_button(
            label="📄 Download TXT",
            data=txt_data,
            file_name="LegalEase_Document.txt",
            mime="text/plain"
        )

    # DOCX
    with col2:

        docx_data = format_docx(
            final_document,
            final_type
        )

        st.download_button(
            label="📝 Download DOCX",
            data=docx_data,
            file_name="LegalEase_Document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        )

    # PDF
    with col3:

        try:

            pdf_data = format_pdf(
                final_document,
                final_type
            )

            st.download_button(
                label="📕 Download PDF",
                data=pdf_data,
                file_name="LegalEase_Document.pdf",
                mime="application/pdf"
            )

        except Exception as e:

            st.error(
                f"PDF generation error: {str(e)}"
            )