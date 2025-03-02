from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pdfplumber
import re
import nltk
from nltk import word_tokenize, pos_tag
import google.generativeai as genai
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

app = Flask(__name__)
CORS(app) 

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"pdf"}

# Initialize NLTK
# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger")


genai.configure(api_key="your_beautiful_api_key")

uri = "mongodb+srv://<user>:<password>@cluster0.4inxm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client["hirehive_db"] 
collection = db["job_id"]  

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

def extract_skills(text, skill_req):
    """Extract skills from the resume text."""
    skills = []
    for keyword in skill_req:
        if keyword.lower() in text.lower():
            skills.append(keyword)
    return skills

def extract_experience(text):
    """Extract experience-related information."""
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    skills = [word for word, pos in tagged if pos in ["NN", "NNS", "NNP", "NNPS"]]
    return list(set(skills))

def extract_education(text):
    """Extract education-related information."""
    education = []
    pattern = r"(?i)(?:(?:Bachelor|B\.S\.|B\.A\.|Master|M\.S\.|M\.A\.|Ph\.D\.)\s(?:[A-Za-z]+\s)*[A-Za-z]+)"
    matches = re.findall(pattern, text)
    for match in matches:
        education.append(match.strip())
    return education

def analyze_strengths(resume_text, job_description):
    """Analyze resume strengths using Gemini AI."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Analyze this resume and highlight its key strengths based on the job description.
    Provide a concise list of 3-5 bullet points. Each bullet point should be short and to the point.
    Do not mention any weaknesses or recommendations. Only list the strengths.

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    response = model.generate_content(prompt)
    return response.text

def analyze_weaknesses(resume_text, job_description):
    """Analyze resume weaknesses (gaps in skills and experience)."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Analyze this resume and highlight areas of weaknesses (gaps in skills and experience) compared to the job description.
    Provide a concise list of 3-5 bullet points. Each bullet point should be short and to the point.
    Do not provide recommendations or suggestions. Only list the gaps.

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    response = model.generate_content(prompt)
    return response.text

def analyze_suggested_skills(resume_text, job_description):
    """Suggest skills the candidate should acquire to better match the job description."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Analyze this resume and suggest skills the candidate should acquire to better match the job description.
    Provide a concise list of 3-5 bullet points. Each bullet point should be short and to the point.
    Do not provide general recommendations. Only list the suggested skills.

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    response = model.generate_content(prompt)
    return response.text

def analyze_gaps_in_experience(resume_text, job_description):
    """Identify gaps in experience compared to the job description."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Analyze this resume and identify gaps in experience compared to the job description.
    Provide a concise list of 3-5 bullet points. Each bullet point should be short and to the point.
    Do not provide general recommendations. Only list the gaps in experience.

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    response = model.generate_content(prompt)
    return response.text

def evaluate_resume(resume_text, job_description):
    """Evaluate the resume and return a score."""
    score = 0
    max_score = 100

    # Contact Information
    name_present = bool(re.search(r"Name:\s*[A-Za-z\s]+", resume_text))
    phone_present = bool(re.search(r"\+?\d{10,15}", resume_text))
    email_present = bool(re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text))
    linkedin_present = "linkedin.com" in resume_text.lower() or "github.com" in resume_text.lower()

    score += 2 if name_present else 0
    score += 3 if phone_present else 0
    score += 3 if email_present else 0
    score += 2 if linkedin_present else 0

    # Skills Evaluation
    job_skills = set(re.findall(r"\b\w+\b", job_description.lower()))
    resume_skills = set(re.findall(r"\b\w+\b", resume_text.lower()))

    matched_skills = job_skills.intersection(resume_skills)
    score += min(len(matched_skills) * 1.5, 15)  # Up to 15 points for hard skills
    score += 5 if "teamwork" in resume_text.lower() or "communication" in resume_text.lower() else 0
    score += 5 if "certified" in resume_text.lower() or "certification" in resume_text.lower() else 0
    score += 5 if "python" in resume_text.lower() or "java" in resume_text.lower() else 0

    # Work Experience
    experience_matches = re.findall(r"\b(?:years|experience|worked at|internship|job)\b", resume_text.lower())
    score += min(len(experience_matches) * 3, 15)  # Up to 15 points

    years_exp = re.search(r"(\d+)\s+years", resume_text.lower())
    score += min(int(years_exp.group(1)) * 1 if years_exp else 0, 5)

    job_achievements = re.findall(r"\b(?:led|managed|increased|developed|optimized|improved)\b", resume_text.lower())
    score += min(len(job_achievements) * 2, 5)

    # Education
    if "bachelor" in resume_text.lower() or "master" in resume_text.lower():
        score += 10
    if "certification" in resume_text.lower() or "course" in resume_text.lower():
        score += 5

    # Resume Formatting & Readability
    well_formatted = len(resume_text.split("\n")) >= 10 and len(resume_text.split(" ")) > 50
    score += 10 if well_formatted else 0

    # Keyword Match with Job Description
    keyword_match = len(matched_skills)
    score += min(keyword_match, 10)

    return min(score, max_score)  # Ensure score does not exceed 100

def extract_name(text):
    name_pattern = re.compile(r'\b([A-Z][a-z]+) ([A-Z][a-z]+)\b')
    matches = name_pattern.findall(text)
    return matches  

def top_of_text(text, n):
    lines = text.split('\n')
    return '\n'.join(lines[:n])

@app.route("/api/uploadfile", methods=["POST"])
def upload_file():
    """Handle file uploads."""
    if "myFile" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["myFile"]
    job_description = request.form.get("jobDescription", "")
    job_id = request.form.get("jobId", "")
    job_name = request.form.get("jobName", "")
    skills = request.form.get("skills", "")

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not job_id or not job_name or not skills:
        return jsonify({"error": "Job ID, Job Name, and Skills are required"}), 400

    skill_req = [skill.strip() for skill in skills.split(",")]

    if file and allowed_file(file.filename):
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        resume_text = extract_text_from_pdf(filename)

        # Extract the candidate's name
        shortened_text_5 = top_of_text(resume_text, 5)
        candidate_name = extract_name(shortened_text_5)[0][0] + " " + extract_name(shortened_text_5)[0][1]

        extracted_skills = extract_skills(resume_text, skill_req)
        extracted_education = extract_education(resume_text)
        extracted_experience = extract_experience(resume_text)

        # Calculate the score
        score = evaluate_resume(resume_text, job_description)

        strengths = analyze_strengths(resume_text, job_description)
        weaknesses = analyze_weaknesses(resume_text, job_description)
        suggested_skills = analyze_suggested_skills(resume_text, job_description)
        gaps_in_experience = analyze_gaps_in_experience(resume_text, job_description)

        # Save the data to MongoDB
        analysis_data = {
            "job_id": job_id,
            "job_name": job_name,
            "resume_filename": file.filename,
            "resumePath": f"/uploads/{file.filename}",  
            "candidate_name": candidate_name,
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggested_skills": suggested_skills,
            "gaps_in_experience": gaps_in_experience,
        }
        collection.insert_one(analysis_data)

        return jsonify({
            "message": "File uploaded and evaluated successfully!",
            "filename": file.filename,
            "resumePath": f"/uploads/{file.filename}",
            "jobDescription": job_description,
            "jobId": job_id,
            "jobName": job_name,
            "skills": extracted_skills,
            "education": extracted_education,
            "experience": extracted_experience,
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggested_skills": suggested_skills,
            "gaps_in_experience": gaps_in_experience,
        }), 200
    else:
        return jsonify({"error": "Only PDF files are allowed"}), 400

@app.route("/uploads/<filename>", methods=["GET"])
def serve_pdf(filename):
    """Serve the uploaded PDF file."""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    """Fetch all unique job IDs."""
    try:
        job_ids = collection.distinct("job_id")
        return jsonify({"job_ids": job_ids}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/leaderboard/<job_id>", methods=["GET"])
def get_leaderboard(job_id):
    """Fetch leaderboard data for a specific job ID."""
    try:
        print(f"Fetching leaderboard data for job_id: {job_id}")  
        candidates = list(collection.find(
            {"job_id": job_id},
            {"_id": 1, "resume_filename": 1, "score": 1, "candidate_name": 1}  
        ).sort("score", -1))

        for candidate in candidates:
            candidate["_id"] = str(candidate["_id"])

        print("Candidates:", candidates) 
        return jsonify({"candidates": candidates}), 200
    except Exception as e:
        print("Error fetching leaderboard data:", str(e)) 
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/candidate/<candidate_id>", methods=["GET"])
def get_candidate(candidate_id):
    """Fetch candidate data by ID."""
    try:
        candidate = collection.find_one({"_id": ObjectId(candidate_id)}, {"_id": 0})
        if candidate:
            return jsonify(candidate), 200
        else:
            return jsonify({"error": "Candidate not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(port=5000, debug=True)