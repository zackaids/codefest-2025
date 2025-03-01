import pdfplumber
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk

# nltk.download("punkt")  # For tokenization
# nltk.download("averaged_perceptron_tagger")  # For part-of-speech tagging
# nltk.download("maxent_ne_chunker")  # For named entity recognition
# nltk.download("words")  # For named entity recognition

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pdfplumber.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

pdf_path = "example_resume.pdf"
resume_text = extract_text_from_pdf(pdf_path)
print(resume_text)

def extract_skills(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    
   
    skills = [word for word, pos in tagged if pos in ["NN", "NNS", "NNP", "NNPS"]]
    
    return list(set(skills))  


resume_text = "Skills: Python, Java, SQL, Machine Learning"
skills = extract_skills(resume_text)
print("Skills:", skills)