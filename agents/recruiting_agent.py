"""import os
from data_utils import insert_candidate
from langchain_ollama import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

def extract_relevant_sections(text):
    Extract only qualifications, experience, and skills from job description.
    lines = text.split('\n')
    relevant_keywords = ['qualification', 'experience', 'skill', 'requirement']
    relevant_sections = []

    for line in lines:
        if any(kw in line.lower() for kw in relevant_keywords):
            relevant_sections.append(line)

    return "\n".join(relevant_sections) if relevant_sections else text

def get_match_score(jd_text, resume_text):
    # Only keep relevant parts of the JD
    relevant_jd = extract_relevant_sections(jd_text)

    jd_vec = np.array(embeddings.embed_query(relevant_jd)).reshape(1, -1)
    res_vec = np.array(embeddings.embed_query(resume_text)).reshape(1, -1)
    score = cosine_similarity(jd_vec, res_vec)[0][0]
    return round(score * 100, 2)

class RecruitingAgent:
    def __init__(self, cv_folder):
        self.cv_folder = cv_folder

    def extract_and_score(self, jd_summary):
        candidates = []
        for filename in os.listdir(self.cv_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(self.cv_folder, filename), "r", encoding="utf-8") as f:
                    resume_text = f.read()
                    match_score = get_match_score(jd_summary, resume_text)
                    name = filename.replace(".txt", "")
                    insert_candidate(name, match_score, resume_text)
                    candidates.append({
                        "name": name,
                        "match": match_score,
                        "resume": resume_text
                    })
        return candidates
"""

import os
import re
from data_utils import insert_candidate
from langchain_ollama import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

def extract_relevant_sections(text):
    lines = text.split('\n')
    relevant_keywords = ['qualification', 'experience', 'skill', 'requirement']
    relevant_sections = []
    for line in lines:
        if any(kw in line.lower() for kw in relevant_keywords):
            relevant_sections.append(line)
    return "\n".join(relevant_sections) if relevant_sections else text

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def get_match_score(jd_text, resume_text):
    relevant_jd = extract_relevant_sections(jd_text)
    jd_vec = np.array(embeddings.embed_query(relevant_jd)).reshape(1, -1)
    res_vec = np.array(embeddings.embed_query(resume_text)).reshape(1, -1)
    score = cosine_similarity(jd_vec, res_vec)[0][0]
    return round(score * 100, 2)

class RecruitingAgent:
    def __init__(self, cv_folder):
        self.cv_folder = cv_folder

    def extract_and_score(self, jd_summary):
        candidates = []
        for filename in os.listdir(self.cv_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(self.cv_folder, filename), "r", encoding="utf-8") as f:
                    resume_text = f.read()
                    match_score = get_match_score(jd_summary, resume_text)
                    name = filename.replace(".txt", "")
                    email = extract_email(resume_text)
                    insert_candidate(name, match_score, resume_text, email)
                    candidates.append({
                        "name": name,
                        "match": match_score,
                        "resume": resume_text,
                        "email": email
                    })
        return candidates
