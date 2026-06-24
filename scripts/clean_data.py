import os
import pandas as pd
import PyPDF2

RAW_DIR = "../data/raw"
CLEAN_DIR = "../data/cleaned"

os.makedirs(CLEAN_DIR, exist_ok=True)

print("\n🔽 CLEANING RAW DATA... 🔽\n")

# ------------ 1. EXTRACT TEXT FROM PDF FILES --------------
for root, dirs, files in os.walk(RAW_DIR):
    for file in files:
        if file.endswith(".pdf"):
            raw_path = os.path.join(root, file)
            clean_path = os.path.join(CLEAN_DIR, file.replace(".pdf", ".txt"))

            print(f"📄 Extracting PDF → {file}")
            try:
                with open(raw_path, "rb") as pdf:
                    reader = PyPDF2.PdfReader(pdf)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"

                with open(clean_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"   ✔ Saved cleaned text → {clean_path}")

            except Exception as e:
                print(f"   ❌ PDF extraction failed for {file}: {e}")


# ------------ 2. CLEAN CSV FILES --------------
for root, dirs, files in os.walk(RAW_DIR):
    for file in files:
        if file.endswith(".csv"):
            raw_path = os.path.join(root, file)
            clean_path = os.path.join(CLEAN_DIR, file)

            print(f"📊 Cleaning CSV → {file}")
            try:
                df = pd.read_csv(raw_path)
                df = df.dropna()
                df.to_csv(clean_path, index=False)
                print(f"   ✔ Clean CSV saved → {clean_path}")

            except Exception as e:
                print(f"   ❌ CSV cleaning failed for {file}: {e}")

print("\n🎉 CLEANING COMPLETE — check /data/cleaned")
