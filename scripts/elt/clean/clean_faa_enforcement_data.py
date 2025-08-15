import os
import pandas as pd
import numpy as np

def clean_faa_enforcement_data(input_path, output_path):
    df = pd.read_excel(input_path)

    # 1. Drop unwanted columns if they exist
    extra_columns = ["MASTER #", "c95", "c710"]
    df = df.drop(columns=[col for col in extra_columns if col in df.columns])

    # 2. Drop rows with no CASE NUMBER
    df = df.dropna(subset=["CASE NUMBER"])

    # 3. Strip whitespace from all string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.astype(str).str.strip())

    # 4. Fix inconsistent casing
    for col in ["ACTION", "SANCTION", "CASE TYPE"]:
        if col in df.columns:
            df[col] = df[col].str.upper()

    # 5. Normalize dates
    df["DATE KNOWN"] = pd.to_datetime(df["DATE KNOWN"], errors="coerce").dt.date
    df["CLOSED DATE"] = pd.to_datetime(df["CLOSED DATE"], errors="coerce").dt.date

    # 6. Normalize ENTITY TYPE
    entity_type_mapping = {
        "A/C OR COMM OPER": "A/C or COMM OPER",
        "CERTIFICATE SHCOOL": "CERTIFICATE SCHOOL",
        "FOREIGN AIR CA": "FOREIGN AIR CAR",
        "APPROVD RPR STA": "APPROVD REPAIR STA",
        "APPROVED RPR STN": "APPROVD REPAIR STA",
        "AIR CARRIER ON DMAND": "AIR CARRIER ON DEMAND",
        "ARPT OPN/INSP": "AIRPORT OPERATOR",
        "COMP PROD": "COMPONENT PRODUCTION",
        "COMM OPER & PART 125": "A/C or COMM OPER",
    }
    df["ENTITY TYPE"] = df["ENTITY TYPE"].replace(entity_type_mapping)

    # 7. Normalize ACTION
    action_mapping = {
        "ORDER ASSESSING CIVIL PENALTY": "ORD ASSESS CIVIL PENALTY",
        "ORDER ASSESS CIVIL PENALTY": "ORD ASSESS CIVIL PENALTY",
        "ORD ASSESS CVIIL PENALTY": "ORD ASSESS CIVIL PENALTY",
        "ORD ASSESS CIVIL PENALTY CONSOLIDATE D CASE": "ORD ASSESS CIVIL PENALTY",
        "ORD ASSESS CP HMT AC": "ORD ASSESS CP HMT",
        "CP FA ACT": "ORD ASSESS CP FA ACT",
        "CERTIFICATE REVOCATION .": "CERTIFICATE REVOCATION",
        "CERTIFICATE REVOCATION 1": "CERTIFICATE REVOCATION",
        "CERT REVOKE": "CERTIFICATE REVOCATION",
        "CERT SUSPEND": "CERTIFICATE SUSPENSION",
    }
    df["ACTION"] = df["ACTION"].replace(action_mapping)

    # 8. Normalize SANCTION
    sanction_mapping = {
        "CONSOLIDATE D CASE": "CONSOLIDATED CASE",
        "CONSOLIDAT ED CASE": "CONSOLIDATED CASE",
        "CONSOLID ATED CASE": "CONSOLIDATED CASE",
        "CONSOLIDA TED CASE": "CONSOLIDATED CASE",
        "INDEFINIT E DURATION": "INDEFINITE DURATION",
        "INDEFINTE DURATION": "INDEFINITE DURATION",
    }
    df["SANCTION"] = df["SANCTION"].replace(sanction_mapping)

    # 9. Normalize CASE TYPE
    case_type_mapping = {
        "RECORDS/RPT S": "RECORDS/RPTS",
        "ACFT ALTR": "AIRCRAFT ALTR",
        "REVOCATIO N OTHER": "REVOCATION OTHER",
        "REVOCATI ON OTHER": "REVOCATION OTHER",
        "REVOCATIO N FLT OPNS": "REVOCATION FLT OPNS",
        "REVOCATI ON FLT OPNS": "REVOCATION FLT OPNS",
        "REVOCATIO N MAINTENANCE": "REVOCATION MAINTENANCE",
        "REVOCATI ON MAINTENANCE": "REVOCATION MAINTENANCE",
        "REVOCATIO N TYPE DESGN DATA": "REVOCATION TYPE DESGN DATA",
        "REVOCATIO N RECORDS/RPTS": "REVOCATION RECORDS/RPTS",
    }
    df["CASE TYPE"] = df["CASE TYPE"].replace(case_type_mapping)

    # 10. Drop rows where any important column (except SANCTION AMOUNT) is null
    columns_to_check = [col for col in df.columns if col != "SANCTION AMOUNT"]
    def is_nan_or_string_nan(val):
        if pd.isna(val):
            return True
        val_str = str(val).strip().lower()
        return val_str == 'nan'
    df = df[~df[columns_to_check].applymap(is_nan_or_string_nan).any(axis=1)]

    # 11. Final cleanup: trim strings again
    df[str_cols] = df[str_cols].apply(lambda col: col.astype(str).str.strip())

    # 12. Convert SANCTION AMOUNT to numeric
    df["SANCTION AMOUNT"] = pd.to_numeric(df["SANCTION AMOUNT"], errors="coerce")

    # 13. Reset index and save
    df = df.dropna(how="all").reset_index(drop=True)
    df.to_csv(output_path.replace(".xlsx", ".csv"), index=False)
    print(f"Cleaned data saved to {output_path.replace('.xlsx', '.csv')} with {len(df)} rows.")
