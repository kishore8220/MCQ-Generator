import os
import re
import pdfplumber
import docx
from fpdf import FPDF
import gradio as gr
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Output folder setup
OUTPUT_FOLDER = "results"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# LangChain model setup
llm = ChatOllama(model="mistral`", temperature=0.0)

mcq_prompt = PromptTemplate(
    input_variables=["context", "num_questions"],
    template="""
You are an AI assistant helping the user generate multiple-choice questions (MCQs) from the text below:

Text:
{context}

Generate {num_questions} MCQs. Each should include:
- A clear question
- Four answer options labeled A, B, C, and D
- The correct answer clearly indicated at the end

Format:
## MCQ
Question: [question]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
Correct Answer: [correct option]
"""
)

mcq_chain = LLMChain(llm=llm, prompt=mcq_prompt)

# -------- Utility Functions --------

def extract_text(file):
    name, ext = os.path.splitext(file.name)
    ext = ext.lower()
    if ext == ".pdf":
        with pdfplumber.open(file) as pdf:
            return ''.join([p.extract_text() for p in pdf.pages if p.extract_text()])
    elif ext == ".docx":
        doc = docx.Document(file)
        return ' '.join([para.text for para in doc.paragraphs])
    elif ext == ".txt":
        return file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file type")

def clean_text(text):
    # Remove <think>...</think> content
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

def save_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for mcq in text.split("## MCQ"):
        if mcq.strip():
            pdf.multi_cell(0, 10, mcq.strip())
            pdf.ln(5)
    path = os.path.join(OUTPUT_FOLDER, filename)
    pdf.output(path)
    return path

# -------- Gradio Interface --------

def generate_mcqs(file, num_questions):
    try:
        raw_text = extract_text(file)
        cleaned_text = clean_text(raw_text)

        mcqs = mcq_chain.run({"context": cleaned_text, "num_questions": num_questions}).strip()
        
        base = os.path.splitext(os.path.basename(file.name))[0]
        txt_path = os.path.join(OUTPUT_FOLDER, f"{base}_mcqs.txt")
        pdf_path = save_pdf(mcqs, f"{base}_mcqs.pdf")
        
        # Save plain text
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(mcqs)
        
        return mcqs, txt_path, pdf_path

    except Exception as e:
        return f"Error: {str(e)}", None, None

# UI elements
iface = gr.Interface(
    fn=generate_mcqs,
    inputs=[
        gr.File(label="Upload PDF / DOCX / TXT"),
        gr.Slider(1, 20, step=1, value=5, label="Number of MCQs")
    ],
    outputs=[
        gr.Textbox(label="Generated MCQs", lines=15),
        gr.File(label="Download TXT"),
        gr.File(label="Download PDF")
    ],
    title="MCQ Generator using Qwen3 + LangChain",
    description="Upload a document and generate MCQs. Content within <think>...</think> will be ignored."
)

iface.launch()
