import re
import os
import shutil
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import docx
import requests

OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

def extract_links_from_text(text):
    return re.findall(r'(https?://\S+)', text)

def extract_links_from_file(filepath):
    links = []
    if filepath.endswith('.pdf'):
        doc = fitz.open(filepath)
        for page in doc:
            text = page.get_text()
            links += extract_links_from_text(text)
    elif filepath.endswith('.docx'):
        doc = docx.Document(filepath)
        full_text = "\n".join([p.text for p in doc.paragraphs])
        links += extract_links_from_text(full_text)
    return links

def extract_links_from_gdoc(gdoc_url):
    # Return link directly — will be processed by Playwright like any URL
    if "docs.google.com" in gdoc_url:
        return [gdoc_url]
    return []

def clear_outputs():
    # Clear all files in uploads and outputs folder
    for folder in [OUTPUT_FOLDER, UPLOAD_FOLDER]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
