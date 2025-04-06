import pandas as pd
from agents.jd_summarizer import job_summarizer
from agents.recruiting_agent import RecruitingAgent
from agents.shortlister import Shortlister
#from agents.interview_scheduler import InterviewScheduler
from data_utils import create_db

CV_DIR = "./cvs"
JD_CSV = "job_description.csv"

create_db()

# Load JD and summarize
df_jd = pd.read_csv("job_description.csv",encoding="latin1")
jd_text = df_jd["Job Description"].iloc[0]
jd_summary = job_summarizer(jd_text)

# Agents
recruiter = RecruitingAgent("CVs1")
shortlister = Shortlister()
#scheduler = InterviewScheduler()

# Extract + match + insert
total_candidates = recruiter.extract_and_score(jd_summary)
shortlisted = shortlister.shortlist(total_candidates)
"""
# Generate invites
for candidate in shortlisted:
    invite = scheduler.generate_invite(candidate["name"], "example@example.com", "Python Developer")
    print(invite)
"""
