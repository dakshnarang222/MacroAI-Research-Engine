import os
import pandas as pd
from PyPDF2 import PdfReader

RAW_DATA_PATH = os.path.join("..", "data", "raw")

def list_files():
    print("\n📁 Files detected in raw directory:\n")
    for root, dirs, files in os.walk(RAW_DATA_PATH):
        for file in files:
            print(f" - {file}   (path: {os.path.join(root, file)})")

def preview_csv(file_path, n=5):
    print(f"\n🔍 Previewing CSV: {file_path}")
    df = pd.read_csv(file_path)
    print(df.head(n))

def preview_excel(file_path, n=5):
    print(f"\n🔍 Previewing Excel: {file_path}")
    df = pd.read_excel(file_path)
    print(df.head(n))

def preview_pdf(file_path, pages=1):
    print(f"\n📄 Reading PDF: {file_path}")
    reader = PdfReader(file_path)
    text = reader.pages[0].extract_text()
    print("\n📝 First page text preview:\n")
    print(text[:800], "...")

if __name__ == "__main__":
    list_files()
