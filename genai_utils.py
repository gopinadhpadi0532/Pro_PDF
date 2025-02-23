# genai_utils.py
import PyPDF2
import pdfminer.high_level
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def load_google_gemini_pro_model():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')  # or 'gemini-pro-vision' if you need image input
    return model


def extract_text_from_pdf_pypdf2(pdf_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text with PyPDF2: {e}")
        return None  # Indicate failure
    return text


def extract_text_from_pdf_pdfminer(pdf_file):
    try:
        text = pdfminer.high_level.extract_text(pdf_file)
        return text
    except Exception as e:
        print(f"Error extracting text with PDFMiner: {e}")
        return None

def generate_answer(model, context, question):
    prompt = f"Based on the following document content:\n\n{context}\n\nAnswer the question: {question}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "An error occurred while generating the answer."



if __name__ == '__main__':
    # Example usage (for testing)
    pdf_path = "example.pdf"  # Replace with an actual PDF file

    # Create a dummy example.pdf file for testing
    with open(pdf_path, "w") as f:
        f.write("This is a test PDF file.  The answer to the question is 42.")


    pdf_text = extract_text_from_pdf_pypdf2(pdf_path)
    if pdf_text:
        print("Extracted Text (PyPDF2):\n", pdf_text)

    pdf_text_miner = extract_text_from_pdf_pdfminer(pdf_path)
    if pdf_text_miner:
        print("Extracted Text (PDFMiner):\n", pdf_text_miner)

    # Example usage of Gemini Pro
    model = load_google_gemini_pro_model()
    if model:
        question = "What is the answer to the question?"
        answer = generate_answer(model, pdf_text, question)
        print("Generated Answer:\n", answer)