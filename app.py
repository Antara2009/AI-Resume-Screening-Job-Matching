from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pathlib import Path
import re
import os

from matcher import analyse_resume, extract_text_from_file

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB per upload
app.config["UPLOAD_FOLDER"] = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
Path(app.config["UPLOAD_FOLDER"]).mkdir(exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    error = None
    job_description = ""

    if request.method == "POST":
        job_description = request.form.get("job_description", "").strip()
        uploaded_files = request.files.getlist("resumes")

        if not job_description:
            error = "Please enter a job description."
        elif not uploaded_files or all(not f.filename for f in uploaded_files):
            error = "Please upload at least one resume."
        else:
            for file in uploaded_files:
                if not file or not file.filename:
                    continue
                filename = secure_filename(file.filename)
                if not allowed_file(filename):
                    results.append({
                        "filename": filename,
                        "error": "Unsupported file type. Upload PDF, DOCX, or TXT."
                    })
                    continue

                # Save only temporarily for parsing; filenames are sanitized.
                saved_path = Path(app.config["UPLOAD_FOLDER"]) / filename
                file.save(saved_path)
                try:
                    resume_text = extract_text_from_file(saved_path)
                    if not resume_text.strip():
                        results.append({
                            "filename": filename,
                            "error": "No readable text found. If this is a scanned PDF, run OCR first."
                        })
                    else:
                        results.append({
                            "filename": filename,
                            **analyse_resume(resume_text, job_description)
                        })
                except Exception as exc:
                    results.append({
                        "filename": filename,
                        "error": f"Could not read this file: {exc}"
                    })
                finally:
                    try:
                        saved_path.unlink(missing_ok=True)
                    except OSError:
                        pass

    results.sort(key=lambda item: item.get("score", -1), reverse=True)
    return render_template(
        "index.html",
        results=results,
        error=error,
        job_description=job_description
    )

if __name__ == "__main__":
    # Local development only. Do not use Flask's development server in production.
    app.run(debug=True)
