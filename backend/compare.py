#pip install google-generativeai

import re
import google.generativeai as genai

# Initialize Google Gemini AI client
genai.configure(api_key="AIzaSyBLi3xUnco4sZsuoi0oPRLzDo0SKTNMPu8")

# Scoring criteria
def evaluate_resume(resume_text, job_description):
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


# AI-assisted resume analysis - Strengths
def analyze_strengths(resume_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Analyze this resume and highlight its key strengths: (do not return any weaknesses, make sure no weaknesses are mentioned here)\n\n{resume_text}")
    return response.text

# AI-assisted resume analysis - Weaknesses
def analyze_weaknesses(resume_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Analyze this resume and highlight areas of weaknesses:\n\n{resume_text}")
    return response.text


# Main Execution
if __name__ == "__main__":
    resume = """
    Name: John Doe
    Email: john.doe@example.com
    Phone: +1234567890
    LinkedIn: linkedin.com/in/johndoe
    Skills: Python, Java, Machine Learning, Data Analysis, Leadership, Communication
    Experience: 5 years in software development. Worked at XYZ Corp. Led multiple projects.
    Education: Bachelor’s in Computer Science, Certified in AI and Data Science.
    """

    job_desc = "Looking for a Python developer with experience in AI, data analysis, and software development."

    score = evaluate_resume(resume, job_desc)
    strengths = analyze_strengths(resume)
    weaknesses = analyze_weaknesses(resume)

    print(f"Resume Score: {score}/100")
    print("\nAI Analysis of Strengths:\n", strengths)
    print("\nAI Analysis of Weaknesses:\n", weaknesses)
