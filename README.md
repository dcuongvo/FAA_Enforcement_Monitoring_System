# FAA Enforcement Monitoring System

## Overview
The **FAA Enforcement Monitoring System** is a data engineering and analytics project designed to process and analyze **Federal Aviation Administration (FAA) enforcement action records**.  
The **current goal** is to build a robust **ELT (Extract, Load, Transform) pipeline** for data ingestion, cleaning, and publishing.  
The **stretch goal** is to implement a **real-time monitoring dashboard** with predictive analytics to identify potential safety and compliance risks.  

## Data Source
The datasets used in this project are sourced from the **Federal Aviation Administration (FAA) Enforcement Information System**.
You can access the raw enforcement data here:  
🔗 [FAA Enforcement Actions Reports](https://www.faa.gov/about/office_org/headquarters_offices/agc/practice_areas/enforcement/reports)

---

## Features

### ✅ Current Capabilities
- **Automated ELT Pipeline**  
  - Extracts raw FAA enforcement reports from multiple formats (PDF, XLSX, CSV).  
  - Cleans, standardizes, and merges data into a unified schema.  
  - Outputs **publish-ready datasets** in CSV/XLSX for downstream use.  

- **Exploratory Data Analysis (EDA)**  
  - Performed in Jupyter Notebooks (`analysis for cleaning.ipynb`, `faa_enforcement_analysis.ipynb`).  
  - Trend analysis by year, violation type, and enforcement action.  
  - Data quality validation and governance compliance.  

- **Data Publishing**  
  - Final cleaned datasets (`faa_enforcement_final_cleaned.csv`) are documented and stored for reproducibility.  
  - Supports integration with BI tools (Power BI, Tableau).  

---

### 🚀 Planned Enhancements (Stretch Goals)  
- **Interactive Dashboard**  
  - Build with Power BI / Tableau / Plotly Dash for dynamic filtering and visualization.  

- **Predictive Analytics**  
  - Implement ML models to forecast potential safety/compliance risks.  

- **Automated Cloud Deployment**  
  - Host ETL on AWS with scheduled refresh and CI/CD integration.  

---

## Repository Structure
```
FAA_ENFORCEMENT_MONITORING_SYSTEM/
│
├── dashboards/                     # Future BI dashboard files
├── data/
│   ├── processed/                   # Cleaned & merged datasets
│   ├── raw/                         # Original FAA datasets
│
├── FAA_Quarterly_Reports/           # Source enforcement reports
├── notebooks/                       # Jupyter analysis workflows
│   ├── analysis for cleaning.ipynb
│   └── faa_enforcement_analysis.ipynb
│
├── scripts/
│   ├── elt/                         # ETL pipeline scripts
│   │   ├── clean/
│   │   │   └── clean_faa_enforcement_data.py
│   │   └── extract/
│   │       ├── pdf_parser.py
│   │       ├── record_extractor.py
│   │       └── ...
│
├── output.csv                       # Example processed output
├── README.md                        # Project documentation
├── requirements.txt                 # Dependencies
└── venv/                             # Virtual environment
```

---

## Installation & Usage

### **1. Clone Repository**
```bash
git clone https://github.com/<your-username>/FAA_Enforcement_Monitoring_System.git
cd FAA_Enforcement_Monitoring_System
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate    # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run ETL Pipeline**
```bash
python scripts/elt/clean/clean_faa_enforcement_data.py
```

### **5. Explore Analysis**
```bash
jupyter notebook
```
Open the notebooks in the `notebooks/` folder.

---

## Example Output
Example snippet from processed dataset (`faa_enforcement_final_cleaned.csv`):  

| Year | Violation Type         | Action Taken | Penalty Amount |
|------|-----------------------|--------------|----------------|
| 2022 | Airspace Violation    | Suspension   | 1500           |
| 2021 | Maintenance Violation | Civil Penalty| 2500           |

---

## Tech Stack
- **Languages:** Python (Pandas, NumPy, PyPDF2)  
- **Tools:** Jupyter Notebook, Power BI / Tableau (planned)  
- **Data Engineering:** ETL Pipelines, Data Cleaning, Data Standardization  
- **Cloud (Stretch Goal):** AWS Lambda, S3, CloudWatch, CI/CD  

## License
This project is released under the [MIT License](LICENSE).