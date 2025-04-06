import streamlit as st
import pandas as pd
import os
import tempfile
import fitz  # PyMuPDF
import re

from agents.jd_summarizer import job_summarizer
from agents.recruiting_agent import RecruitingAgent,get_match_score
from agents.shortlister import Shortlister
from data_utils import create_db, insert_candidate
from agents.interview_scheduler import send_email_invites  # ✅ Updated function import

# Streamlit config
st.set_page_config(page_title="🎯 AI Recruiting System", layout="wide")
create_db()

st.markdown("""
        <h1 style='text-align: center; 
            font-size: 50px;
            font-weight: bold;
            color: #87CEEB; 
            text-shadow: 2px 2px 15px rgba(135, 206, 235, 0.8);'>
            SmartHireX ⚡️
        </h1>
        """,unsafe_allow_html=True)
st.markdown(""" <h6 style='texr-align:center;margin-left:375px;
            font-size:25px;color:white;'>
            ☆ 1<i>AI-Powered Hiring. Smarter. Faster. Fairer.<i> ☆
            </h6>
        """,unsafe_allow_html=True)
st.write('---')

# Upload inputs
jd_file = st.file_uploader("📄 Upload Job Description CSV", type="csv")
cv_files = st.file_uploader("📎 Upload Candidate CVs (PDFs)", type="pdf", accept_multiple_files=True)
threshold = st.slider("🎯 Shortlist Match Threshold", 0, 100, 80)

if jd_file and cv_files:
    df = pd.read_csv(jd_file, encoding="latin1")
    if "Job Title" not in df.columns or "Job Description" not in df.columns:
        st.error("❌ CSV must contain 'Job Title' and 'Job Description' columns.")
        st.stop()

    job_titles = df["Job Title"].unique().tolist()
    selected_jobs = st.multiselect("🎯 Select Job Titles", job_titles)

    if selected_jobs:
        candidates = []

        # Extract resume text from PDFs
        for file in cv_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            doc = fitz.open(tmp_path)
            resume_text = "\n".join([page.get_text() for page in doc])
            name = os.path.splitext(file.name)[0]

            email_match = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
            email = email_match.group(0) if email_match else "not_found@example.com"

            candidates.append({
                "name": name,
                "resume": resume_text,
                "email": email
            })

        for title in selected_jobs:
            st.subheader(f"🔍 Processing for `{title}`")
            jd_row = df[df["Job Title"] == title].iloc[0]
            jd_text = jd_row["Job Description"]
            jd_summary = job_summarizer(jd_text)

            st.markdown(f"**Job Summary:**\n\n{jd_summary}")

            recruiter = RecruitingAgent("CVs1")
            shortlister = Shortlister(threshold)

            for c in candidates:
                score = get_match_score(jd_summary, c["resume"])
                insert_candidate(c["name"], score, c["resume"],c["email"])
                c["match"] = score

            shortlisted = shortlister.shortlist(candidates)

            if shortlisted:
                st.success(f"✅ {len(shortlisted)} candidates shortlisted for `{title}`!")

                for cand in shortlisted:
                    st.markdown(f"**{cand['name']}** — Match Score: `{cand['match']}%`, Email: {cand['email']}")
                    with st.expander("📄 View Resume"):
                        st.text(cand["resume"])

                if st.button("📧 Send Interview Emails to All Shortlisted Candidates"):
                    for cand in shortlisted:
                        try:
                            send_email_invites(cand["name"], cand["email"])
                            st.success(f"📬 Email sent to {cand['name']} at {cand['email']}")
                        except Exception as e:
                            st.error(f"❌ Failed to send email to {cand['name']}: {e}")
            else:
                st.warning(f"No candidates matched the threshold for `{title}`.")
    else:
        st.info("👈 Please select at least one job title to begin.")
else:
    st.info("📥 Upload a JD CSV and resumes to begin.")

