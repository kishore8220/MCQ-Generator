# 📚 Automated MCQ Generator using LLMs

This project is a smart, file-based **MCQ (Multiple Choice Questions) generator** built using **LangChain**, **Ollama (Qwen3)**, and document parsing tools. It takes educational content from PDF, DOCX, or TXT files and generates well-structured multiple-choice questions automatically, saving the results in both `.txt` and `.pdf` formats.

---

## 🚀 Key Features

- 📄 **Supports Multiple File Types**: Extracts text from `.pdf`, `.docx`, and `.txt` formats using `pdfplumber`, `python-docx`, and native file I/O.
- 🧠 **LLM-Powered MCQ Generation**: Uses `LangChain` and `ChatOllama` (Qwen3) to generate intelligent MCQs from the provided content.
- 📁 **Dual Output Format**: Outputs the MCQs into a `.txt` file and a formatted `.pdf` using `FPDF`.
- 🛠️ **Customizable**: Easily change the number of questions and file paths.

---

## 📦 Dependencies

Install the required packages:

```bash
pip install langchain pdfplumber python-docx fpdf
```

Ensure you have [Ollama](https://ollama.com/) installed and running locally.

---

## 🧪 How It Works

1. **Text Extraction**: The script first identifies the file type and extracts the raw text content.
2. **Prompt Template**: A custom LangChain `PromptTemplate` instructs the model to generate MCQs in a clear, structured format.
3. **LLM Chain**: The extracted text and number of questions are passed to the model via a `LLMChain`.
4. **File Saving**:

   - A `.txt` version is saved for readability.
   - A `.pdf` version is saved with proper formatting using `FPDF`.

---

## 📝 Output Format

```
## MCQ
Question: What is AI?
A) Animal Intelligence
B) Artificial Intelligence
C) Actual Input
D) Advanced Interface
Correct Answer: B
```

---

## 🏁 Run the Script

Update the `UPLOAD_FILE` path in the script and run:

```bash
python mcq.py
```

Your output will be saved inside the `results/` directory.

---

## 📂 Folder Structure

```
├── mcq.py
├── results/
│   ├── generated_mcqs_pdf2.txt
│   └── generated_mcqs_pdf2.pdf
```
