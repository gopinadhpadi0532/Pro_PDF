# app.py
import streamlit as st
from genai_utils import extract_text_from_pdf_pypdf2, extract_text_from_pdf_pdfminer, generate_answer, load_google_gemini_pro_model
import io  # For handling file uploads as bytes


def main():
    st.title("GenAI PDF Question Answering")

    pdf_file = st.file_uploader("Hello user please upload your pdf :", type="pdf")

    question = st.text_input("Please enter your question:")

    if pdf_file and question:
        # Determine which PDF extraction method to use
        pdf_text = extract_text_from_pdf_pypdf2(pdf_file)
        if not pdf_text:
            st.warning("PyPDF2 failed to extract text. Trying PDFMiner...")
            pdf_text = extract_text_from_pdf_pdfminer(pdf_file)  # Try the alternative

        if pdf_text:
            # Load the Gemini Pro model (only if we have PDF text)
            model = load_google_gemini_pro_model()

            if model:
                answer = generate_answer(model, pdf_text, question)
                st.subheader("Answer:")
                st.write(answer)
            else:
                st.error("Failed to load the Gemini Pro model. Check your API key.")

        else:
            st.error("Failed to extract text from the PDF.  The PDF might be corrupted or contain scanned images (not text).")


if __name__ == "__main__":
    main()
    