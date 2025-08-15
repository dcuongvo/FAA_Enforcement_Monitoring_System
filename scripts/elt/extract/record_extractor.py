import re
from datetime import datetime
import unicodedata

#convert all format into m/d/y
def normalize_date(date_str):
    for fmt in ("%m/%d/%y", "%d-%b-%y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%m/%d/%y")
        except ValueError:
            continue
    return date_str

#Constants
CASE_NUMBER_PATTERN = re.compile(r"^\d{4}[A-Z]{2,3}\d{5,6}")
ENTITY_TYPES = [
    "A/C or COMM OPER",
    "A/C or COMM OPER CARRIER",
    "APPROVD REPAIR STA",
    "ARPT OPN/INSP ",
    "AIRCRAFT PROD",
    "CERTIFICATE SCHOOL",
    "CERTIFICATE SHCOOL",
    "FOREIGN AIR CAR",
    "FOREIGN AIR CA",
    "COMP PROD",
    "AIRPORT OPERATOR",
    "AGRI OPR",
    "EXT LOAD", 
    "SCHED AIR CARRIER", "AIR CARRIER ON DMAND", 
    "APPROVED RPR STN", "SUPP AIR CARRIER", "COMM OPER & PART 125",
]
ENTITY_TYPE_PATTERN = re.compile("|".join(re.escape(e) for e in ENTITY_TYPES), re.IGNORECASE)
#DATE_PATTERN = re.compile(r"\d{2}/\d{2}/\d{2}")
DATE_PATTERN = re.compile(
    r"\b\d{1,3}/\d{1,2}/\d{2,4}\b"         # Matches 1/1/17 or 12/25/2017
    r"|\b\d{1,2}-[A-Za-z]{3}-\d{2,4}\b",   # Matches 1-Jan-17 or 01-Jan-2014
    re.IGNORECASE
)
SANCTION_TYPES = ["DOLLARS", "DOLLAR", "DAYS", "DAY", 
                  "WAIVED","SANCTION WAIVED" ,"REVOCATION",
                  "INDEFINITE DURATION","INDEFINITE","INDEFINTE DURATION", "INDEFINIT E DURATION",
                    "CONSOLIDATED CASE","CONSOLIDAT ED CASE",
                    "CONSOLID ATED CASE", "CONSOLIDA TED CASE","CONSOLIDATE D CASE",
                      "PENDING COMPLIANCE"]
SANCTION_TYPE_PATTERN = re.compile(
    "(" + "|".join(re.escape(s) for s in SANCTION_TYPES) + ")", re.IGNORECASE
)
MONETARY_SANCTION_TYPES = ["DOLLARS", "DOLLAR", "DAY", "DAYS","SANCTION WAIVED"]
NUMBER_PATTERN = re.compile(r"\b\d+(?:,\d{3})*(?:\.\d+)?\b")

def record_extractor(record):
    record = re.sub(r"\s+", " ", record).strip()
    # Normalize all hyphen-like characters to ASCII "-"
    record = ''.join('-' if unicodedata.category(c).startswith("Pd") else c for c in record)
    result = {
        "CASE NUMBER": None,
        "NAME": None,
        "ENTITY TYPE": None,
        "DATE KNOWN": None,
        "ACTION": None,
        "SANCTION AMOUNT": None,
        "SANCTION": None,
        "CASE TYPE": None,
        "CLOSED DATE": None
    }
    # CASE NUMBER
    case_match = CASE_NUMBER_PATTERN.search(record)
    if not case_match:
        return result
    result["CASE NUMBER"] = case_match.group()
    remaining = record[case_match.end():].strip()

    # ENTITY TYPE & NAME
    entity_match = ENTITY_TYPE_PATTERN.search(remaining)
    if not entity_match:
        return result
    result["ENTITY TYPE"] = entity_match.group()
    result["NAME"] = remaining[:entity_match.start()].strip()
    after_entity = remaining[entity_match.end():].strip()

    # DATE KNOWN
    date_match = DATE_PATTERN.search(after_entity)
    if not date_match:
        return result
    raw_date_known = date_match.group()
    result["DATE KNOWN"] = normalize_date(raw_date_known)
    #edge case
    raw_date_known = re.sub(
    r"\b0?(\d{3})/(\d{2})/(\d{2,4})\b",
    lambda m: f"{int(m.group(1)):02d}/{m.group(2)}/{m.group(3)}",
    raw_date_known
    )
    after_date = after_entity[date_match.end():].strip()

    # Find SANCTION
    matches = list(SANCTION_TYPE_PATTERN.finditer(after_date))
    sanction_type_match = matches[-1] if matches else None
    if sanction_type_match:
        result["SANCTION"] = sanction_type_match.group().upper()
        text_before_type = after_date[:sanction_type_match.start()].strip()
        # Only extract SANCTION AMOUNT if type is DOLLARS
        if result["SANCTION"] in MONETARY_SANCTION_TYPES:
            number_match = NUMBER_PATTERN.search(text_before_type)
            if number_match:
                result["SANCTION AMOUNT"] = number_match.group()
                result["ACTION"] = text_before_type[:number_match.start()].strip()
            else:
                result["ACTION"] = text_before_type  # No number found
        else:
            result["SANCTION AMOUNT"] = ""
            result["ACTION"] = text_before_type  # No amount to extract
        # Extract CASE TYPE and CLOSED DATE
        after_type = after_date[sanction_type_match.end():].strip()
        close_date_match = DATE_PATTERN.search(after_type)
        if close_date_match:
            raw_close_date = close_date_match.group()
            result["CLOSED DATE"] = normalize_date(raw_close_date)
            result["CASE TYPE"] = after_type[:close_date_match.start()].strip()
    return result