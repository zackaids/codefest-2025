import pdfplumber
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
import regex as re

nltk.download("punkt")  # For tokenization
nltk.download("averaged_perceptron_tagger")  # For part-of-speech tagging
nltk.download("maxent_ne_chunker")  # For named entity recognition
nltk.download("words")  # For named entity recognition
nltk.download("punkt_tab")  # For tokenization
nltk.download("averaged_perceptron_tagger_eng")  # For part-of-speech tagging

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pdfplumber.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_skills(text, keywords):

    skills = []
    for keyword in keywords:
        if keyword.lower() in text.lower():
            skills.append(keyword)
    return skills

    # tokens = word_tokenize(text)
    # tagged = pos_tag(tokens)
    
   
    # skills = [word for word, pos in tagged if pos in ["NN", "NNS", "NNP", "NNPS"]]
    
    return list(set(skills))

def extract_experience(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)

    skills = [word for word, pos in tagged if pos in ["NN", "NNS", "NNP", "NNPS"]]
    return list(set(skills))

def top_of_text(text, n):
    lines = text.split('\n')
    return '\n'.join(lines[:n])

def extract_names(text):
    name_pattern = re.compile(r'\b([A-Z][a-z]+) ([A-Z][a-z]+)\b')
    matches = name_pattern.findall(text)
    return matches  

def extract_emails(text):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = email_pattern.findall(text)
    return emails if emails else ["No email found"]

def extract_phone_numbers(text):
    phone_number_pattern = re.compile(
        r'\b(?:\+?(\d{1,3})[-.\s]?)?(?:\(?(\d{3})\)?[-.\s]?)?(\d{3})[-.\s]?(\d{4})\b'
    )
    matches = phone_number_pattern.findall(text)
    phone_numbers = ["".join(match) for match in matches]
    return phone_numbers

def extract_linked_in(text):
    linked_in_pattern = re.compile(r'linkedin\.com/in/[A-Za-z0-9_-]+')
    linked_in_links = linked_in_pattern.findall(text)
    return linked_in_links if linked_in_links else ["No LinkedIn profile found"]

def extract_education(text):
    education = []

    # Use regex pattern to find education information
    pattern = r"(?i)(?:(?:Bachelor|B\.S\.|B\.A\.|Master|M\.S\.|M\.A\.|Ph\.D\.)\s(?:[A-Za-z]+\s)*[A-Za-z]+)"
    matches = re.findall(pattern, text)
    for match in matches:
        education.append(match.strip())

    return education

def extract_college_name(text):
    lines = text.split('\n')
    college_pattern = r"(?i).*(college|university|high school).*"
    colleges = []
    for line in lines:
        if re.match(college_pattern, line):
            if len(line.strip()) < 80:
                colleges.append(line.strip())
    return colleges

def extract_classes(text, classes_list):
    classes = []

    for class_name in classes_list:
        if class_name.lower() in text.lower():
            classes.append(class_name)
    return classes




pdf_path = "C:/Users/Maksym/Documents/Github/codefest-2025/backend/example_resume.pdf"
resume_text = extract_text_from_pdf(pdf_path)
print(resume_text)
shortened_text_5 = top_of_text(resume_text, 5)
skill_req = [
    "Python", "Java", "C++", "SQL", "JavaScript", "HTML", "CSS", "React", "Node.js", 
    "Django", "Flask", "Machine Learning", "Deep Learning", "Data Analysis", 
    "Data Visualization", "TensorFlow", "Keras", "PyTorch", "Natural Language Processing", 
    "Computer Vision", "Git", "Docker", "Kubernetes", "AWS", "Azure", "GCP", 
    "Agile", "Scrum", "Linux", "Unix", "Algorithms", "Data Structures"
]
skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau']
classes_list = [
    'Introduction to Computer Science', 'Computer Programming I', 'Computer Programming II', 
    'Data Structures', 'Algorithms', 'Computer Systems', 'Operating Systems', 
    'Software Engineering', 'Database Systems', 'Computer Networks', 'Artificial Intelligence', 
    'Machine Learning', 'Computer Vision', 'Natural Language Processing', 'Human-Computer Interaction', 
    'Web Development', 'Mobile App Development', 'Game Development', 'Cybersecurity', 
    'Cryptography', 'Parallel Computing', 'Distributed Systems', 'Cloud Computing', 
    'Big Data', 'Data Mining', 'Data Visualization', 'Bioinformatics', 'Robotics', 
    'Theory of Computation', 'Compiler Design', 'Programming Languages', 'Computer Graphics', 
    'Digital Logic Design', 'Computer Architecture', 'Embedded Systems', 'Internet of Things', 
    'Software Testing', 'Software Project Management', 'Information Retrieval', 
    'Computer-Aided Design', 'Computer Animation', 'Augmented Reality', 'Virtual Reality', 
    'Quantum Computing', 'Ethics in Computing', 'Computational Biology', 'Computational Geometry', 
    'Formal Methods', 'Numerical Methods', 'Scientific Computing', 'Social Computing', 
    'Ubiquitous Computing', 'Wearable Computing', 'Wireless Networks', 'Advanced Algorithms', 
    'Advanced Data Structures', 'Advanced Operating Systems', 'Advanced Software Engineering', 
    'Advanced Database Systems', 'Advanced Computer Networks', 'Advanced Artificial Intelligence', 
    'Advanced Machine Learning', 'Advanced Computer Vision', 'Advanced Natural Language Processing', 
    'Advanced Human-Computer Interaction', 'Advanced Web Development', 'Advanced Mobile App Development', 
    'Advanced Game Development', 'Advanced Cybersecurity', 'Advanced Cryptography', 
    'Advanced Parallel Computing', 'Advanced Distributed Systems', 'Advanced Cloud Computing', 
    'Advanced Big Data', 'Advanced Data Mining', 'Advanced Data Visualization', 
    'Advanced Bioinformatics', 'Advanced Robotics', 'Advanced Theory of Computation', 
    'Advanced Compiler Design', 'Advanced Programming Languages', 'Advanced Computer Graphics', 
    'Advanced Digital Logic Design', 'Advanced Computer Architecture', 'Advanced Embedded Systems', 
    'Advanced Internet of Things', 'Advanced Software Testing', 'Advanced Software Project Management', 
    'Advanced Information Retrieval', 'Advanced Computer-Aided Design', 'Advanced Computer Animation', 
    'Advanced Augmented Reality', 'Advanced Virtual Reality', 'Advanced Quantum Computing', 
    'Advanced Ethics in Computing', 'Advanced Computational Biology', 'Advanced Computational Geometry', 
    'Advanced Formal Methods', 'Advanced Numerical Methods', 'Advanced Scientific Computing', 
    'Advanced Social Computing', 'Advanced Ubiquitous Computing', 'Advanced Wearable Computing', 
    'Advanced Wireless Networks'
]


name = extract_names(shortened_text_5)[0][0] + " " + extract_names(shortened_text_5)[0][1]
email = extract_emails(shortened_text_5)[0]
phone = extract_phone_numbers(shortened_text_5)[0]
linkedin = extract_linked_in(shortened_text_5)[0]
education = extract_education(resume_text)

skills = extract_skills(resume_text, skill_req)

print(f"\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nLinkedIn: {linkedin}")
print(f"Skills: {skills}")
print(f"Education: {education}")
print(f"Classes: {extract_classes(resume_text, classes_list)}")
print(f"College: {extract_college_name(resume_text)}")
print(f"Experience: {extract_experience(resume_text)}")

