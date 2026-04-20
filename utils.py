import fitz

def extract_text(file):
    text = ""
    pdf = fitz.open(stream = file.read(), filetype = "pdf")
    for page in pdf:
        text += page.get_text()
    return text

def is_resume(text):
    resume_keywords = ["experience", "education", "skills", "projects", 
                       "internship", "certifications", "objective", "summary"]
    text_lower = text.lower()
    matches = sum(1 for word in resume_keywords if word in text_lower)
    return matches >= 3

job_descriptions = {
    "Data Scientist": "machine learning python statistics pandas numpy deep learning",
    "Data Analyst": "excel sql visualization tableau powerbi data cleaning",
    "ML Engineer": "machine learning deployment flask api docker tensorflow",
    "Web Developer": "html css javascript react node frontend backend web development responsive design"
}

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_to_jobs(resume_text, jobs):
    resume_text = resume_text.lower()
    documents = [resume_text] + [desc.lower() for desc in jobs.values()]
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
    results = {}
    for i, job in enumerate(jobs.keys()):
        results[job] = round(scores[i] * 100, 2)
    return results

skills = {
    "Data Scientist": ["python", "machine learning", "statistics", "pandas"],
    "Data Analyst": ["excel", "sql", "tableau", "powerbi"],
    "ML Engineer": ["tensorflow", "docker", "api", "deployment"],
    "Web Developer": ["html", "css", "javascript", "react", "node"]
}

def find_missing_skills(resume_text, role):
    resume_text = resume_text.lower()
    required = skills[role]
    
    missing = [skill for skill in required if skill not in resume_text]
    
    return missing

def generate_suggestions(missing_skills):
    suggestions = []
    
    for skill in missing_skills:
        suggestions.append(f"Consider adding projects or experience related to {skill}")
    
    return suggestions
