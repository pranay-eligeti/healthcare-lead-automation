> End-to-end Python + n8n pipeline that automatically cleans, filters, and structures healthcare lead data across 14 specialties and 4 states — zero manual intervention.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![n8n](https://img.shields.io/badge/n8n-Workflow%20Automation-orange)
![Monday.com](https://img.shields.io/badge/Monday.com-API-red)
![pandas](https://img.shields.io/badge/pandas-Data%20Processing-green)

---

## What It Does

Automates the full lifecycle of healthcare lead data — from raw, contaminated exports to clean, verified, specialty-specific CSV files — triggered automatically via Monday.com and n8n without any manual work.

---

## The Problem It Solves

Raw healthcare lead files exported from Monday.com were heavily contaminated:
- Urgent Care files contained primary care clinics and unrelated businesses
- No consistent specialty or state filtering
- Required hours of manual cleaning per batch

This system eliminates all of that.

---

## How It Works

```
Monday.com (bad-contact flagged)
        │
        ▼
   n8n Webhook Trigger
        │
        ▼
   14-Step Python Cleaning Pipeline
        │
        ├── Step 1:  Load file with header=2 (Monday.com export format)
        ├── Step 2:  Normalize column names
        ├── Step 3:  Drop empty rows
        ├── Step 4:  State whitelist filtering (regex-based, flexible)
        ├── Step 5:  Specialty whitelist matching
        ├── Step 6:  Blacklist filtering (remove known bad entries)
        ├── Step 7:  Google Places batch validation
        ├── Step 8:  Deduplicate by phone + name
        ├── Step 9:  Phone number formatting
        ├── Step 10: Email formatting and validation
        ├── Step 11: Remove placeholder/results rows
        ├── Step 12: Flag remaining anomalies
        ├── Step 13: Sort and structure output
        └── Step 14: Export to clean specialty/state CSV
        │
        ▼
  37+ Clean Output Files
  (14 specialties × 4 states: AL / OH / IL / IN)
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core pipeline logic |
| pandas | Data loading, filtering, transformation |
| n8n | Webhook trigger and workflow orchestration |
| Monday.com API | Bad-contact detection and board integration |
| Google Places API | Provider validation and placeholder row resolution |
| regex | Flexible state and specialty pattern matching |
| openpyxl | Excel output formatting |

---

## Specialties Covered

Urgent Care · Physical Therapy · Cardiology · Orthopedics · Neurology · Dermatology · Gastroenterology · Oncology · Ophthalmology · Pediatrics · Psychiatry · Pulmonology · Rheumatology · Endocrinology

---

## States Covered

Alabama (AL) · Ohio (OH) · Illinois (IL) · Indiana (IN)

---

## Project Structure

```
healthcare-lead-automation/
├── src/
│   ├── pipeline.py          # Main 14-step cleaning pipeline
│   ├── filters.py           # Whitelist/blacklist logic
│   ├── places_validator.py  # Google Places batch lookup
│   ├── formatter.py         # Phone/email formatting
│   └── exporter.py          # Output file generation
├── config/
│   ├── whitelists/          # Specialty keyword whitelists
│   └── blacklists/          # Known bad entry patterns
├── .env.example
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/pranay-eligeti/healthcare-lead-automation.git
cd healthcare-lead-automation
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Fill in your API keys in .env
```

### 4. Run the pipeline
```bash
python src/pipeline.py --input data/leads.csv --specialty "urgent_care" --state "OH"
```

---

## Environment Variables

```env
# .env.example
MONDAY_API_KEY=your_monday_api_key_here
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
N8N_WEBHOOK_URL=your_n8n_webhook_url_here
OUTPUT_DIR=./output
```

---

## Requirements

```
pandas>=2.0.0
openpyxl>=3.1.0
requests>=2.31.0
python-dotenv>=1.0.0
```

---

## Results

- ✅ 37+ clean specialty/state output files produced
- ✅ Zero manual file processing
- ✅ Contamination rate reduced to 0% per output file
- ✅ Fully automated — triggered by Monday.com, run by n8n

---

## Author

**Pranay Eligeti** — [linkedin.com/in/pranay-eligeti](https://linkedin.com/in/pranay-eligeti)
