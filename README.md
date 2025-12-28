# AI Engineering Learning

This repository contains scripts and experiments for learning AI engineering concepts, focusing on structured data extraction from documents using LLMs (Gemini).

## Files

- **`structure-data.py`**: The main script for extracting structured data from insurance claim documents (PDF or Image).
  - Uses Google's `gemini-2.5-pro` model for vision and structured output.
  - Requires a `.env` file with `GEMINI_API_KEY`.
- **`gen_test_data.py`**: A helper script to generate synthetic "messy" PDF insurance claims for testing extraction resilience.
- **`summerize-text.py`**: Script for text summarization experiments.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   brew install poppler  # Required for PDF processing
   ```

2. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

### Generate Test Data
```bash
python3 gen_test_data.py
# Creates messy_claim.pdf
```

### Run Extraction
```bash
python3 structure-data.py --file messy_claim.pdf --output result.json
```
