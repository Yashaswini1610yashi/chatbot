import os
from pypdf import PdfReader

def load_pdfs(folder="data/pdfs"):
    texts = []

    if not os.path.exists(folder):
        os.makedirs(folder)
        return []

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            try:
                reader = PdfReader(os.path.join(folder, file))
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                texts.append(text)
            except Exception as e:
                print(f"Error reading {file}: {e}")

    return texts

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""
