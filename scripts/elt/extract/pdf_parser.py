def extract_records_from_pdf(pdf_path: str) -> list[str]:
    import fitz
    import re
    # Load and extract text from PDF
    doc = fitz.open(pdf_path)
    all_text = "\n".join([page.get_text() for page in doc])
    lines = all_text.split("\n")
    # group text into each row (record)
    records = []
    current = []
    case_started = False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r"^\d{4}[A-Z]{2,3}\d{5,6}", line):
            case_started = True
            if current:
                records.append(" ".join(current))
            current = [line]
        elif case_started:
            current.append(line)

    if current:
        records.append(" ".join(current))

    return records