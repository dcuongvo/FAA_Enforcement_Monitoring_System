import os
import pandas as pd
from glob import glob
from clean.clean_faa_enforcement_data import clean_faa_enforcement_data
from extract.pdf_parser import extract_records_from_pdf
from extract.record_extractor import record_extractor

def extract_all_files():
    print(" Starting PDF extraction...")
    raw_dir = "data/raw/faa_enforcement_data"
    processed_dir = "data/processed/faa_enforcement_processed_xlsx"
    os.makedirs(processed_dir, exist_ok=True)

    years = range(2010, 2025)
    quarters = ["q1", "q2", "q3", "q4"]

    for year in years:
        for q in quarters:
            filename = f"{q}-{str(year)[-2:]}.pdf"
            input_path = os.path.join(raw_dir, filename)
            output_path = os.path.join(processed_dir, f"{q}_{year}_structured.xlsx")

            if os.path.exists(input_path):
                print(f"Processing {filename}...")
                records = extract_records_from_pdf(input_path)
                parsed = [record_extractor(rec) for rec in records]
                pd.DataFrame(parsed).to_excel(output_path, index=False)
            else:
                print(f"⚠️ File not found: {filename}, skipping.")

def merge_and_clean_all():
    print("📊 Merging all structured XLSX files...")
    processed_dir = "data/processed/faa_enforcement_processed_xlsx"
    merged_path = "data/processed/faa_enforcement_merged.xlsx"
    final_cleaned_path = "data/processed/faa_enforcement_final_cleaned.csv"
    xlsx_files = sorted(glob(os.path.join(processed_dir, "*.xlsx")))
    df_list = [pd.read_excel(file) for file in xlsx_files]
    merged_df = pd.concat(df_list, ignore_index=True)
    merged_df.to_excel(merged_path, index=False)
    print(f"Merged {len(xlsx_files)} files into: {merged_path}")
    # Clean the merged data
    clean_faa_enforcement_data(merged_path, final_cleaned_path)

def full_pipeline():
    extract_all_files()
    merge_and_clean_all()

full_pipeline()
