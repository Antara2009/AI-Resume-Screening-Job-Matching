# AI-Powered Resume Screening & Job Matching

A beginner-friendly mini-project prototype that accepts PDF, DOCX, and TXT resumes, compares them with a job description, shows a matching score, and explains matched/missing skills.

## Requirements
- Python 3.10 or newer
- Internet connection for the first-time package installation

## Run in VS Code

1. Extract this ZIP file.
2. Open the `ai_resume_job_matcher` folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment (recommended):

   **Windows**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

5. Install packages:
   ```powershell
   pip install -r requirements.txt
   ```

6. Start the app:
   ```powershell
   python app.py
   ```

7. Open this address in your browser:
   `http://127.0.0.1:5000`

## How to test
- Enter a job description with clear requirements, e.g. Python, SQL, Machine Learning, Pandas.
- Upload two or more text-based sample resumes.
- Compare the displayed scores and skill lists.

## Important limitations
- This is a student prototype, not a production hiring system.
- The score is a transparent baseline combining TF-IDF text similarity and overlap of detected skills. It is not a calibrated probability of success or a validated measure of candidate quality.
- Skill extraction uses a built-in keyword list. Add to `SKILL_KEYWORDS` in `matcher.py` for more terms.
- Scanned PDFs (image-only PDFs) will need OCR; this version does not include OCR.
- Do not use the score to automatically reject candidates. Human review is required.
- This development server is intended for local testing only. Do not deploy it publicly as-is.
- Uploaded files are temporarily saved for parsing and then removed. Do not upload sensitive real resumes during development.
