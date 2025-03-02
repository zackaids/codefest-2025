from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pdfplumber

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Set the upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def compare_skills(resume_text, required_skills):
    """
    Compare the skills in the resume with the required skills.
    """
    resume_text_lower = resume_text.lower()
    required_skills_lower = [skill.strip().lower() for skill in required_skills]

    matching_skills = [skill for skill in required_skills_lower if skill in resume_text_lower]
    missing_skills = [skill for skill in required_skills_lower if skill not in resume_text_lower]

    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
    }

@app.route("/api/uploadfile", methods=["POST"])
def upload_file():
    """Handle file uploads."""
    if "myFile" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["myFile"]
    job_description = request.form.get("jobDescription", "")
    job_id = request.form.get("jobId", "")
    job_name = request.form.get("jobName", "")
    skills = request.form.get("skills", "")  # Get skills as a comma-separated string

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not job_id or not job_name or not skills:
        return jsonify({"error": "Job ID, Job Name, and Skills are required"}), 400

    # Split the skills string into a list
    required_skills = [skill.strip() for skill in skills.split(",")]

    if file and allowed_file(file.filename):
        # Save the file to the upload folder
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        # Extract text from the resume
        resume_text = extract_text_from_pdf(filename)

        # Compare resume skills with required skills
        comparison_result = compare_skills(resume_text, required_skills)

        # Return the evaluation results
        return jsonify({
            "message": "File uploaded and evaluated successfully!",
            "filename": file.filename,
            "path": filename,
            "jobDescription": job_description,
            "jobId": job_id,
            "jobName": job_name,
            "required_skills": required_skills,
            "matching_skills": comparison_result["matching_skills"],
            "missing_skills": comparison_result["missing_skills"],
        }), 200
    else:
        return jsonify({"error": "Only PDF files are allowed"}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)