"""import streamlit as st
import pandas as pd
import os
import fitz  # PyMuPDF
from tempfile import NamedTemporaryFile
from agents.jd_summarizer import job_summarizer
from agents.recruiting_agent import RecruitingAgent
from agents.shortlister import Shortlister
from agents.interview_scheduler import InterviewScheduler
from data_utils import create_db, fetch_shortlisted, insert_candidate

# Create DB initially
create_db()

st.title("🧠 AI Recruitment Shortlister")
st.write("Upload a **Job Description** CSV and **Candidate CVs (PDFs)**")

jd_file = st.file_uploader("📄 Upload Job Description CSV", type=["csv"])
uploaded_cvs = st.file_uploader("📁 Upload Candidate CVs (PDF)", type=["pdf"], accept_multiple_files=True)

if jd_file and uploaded_cvs:
    with st.spinner("Processing..."):

        # Load JD CSV
        df_jd = pd.read_csv(jd_file,encoding="latin1")
        jd_text = df_jd["Job Description"].iloc[0]
        jd_summary = job_summarizer(jd_text)

        st.success("✅ Job Description Summarized")

        # Agents
        shortlister = Shortlister()
        scheduler = InterviewScheduler()

        # Loop over uploaded PDFs
        candidates = []
        for pdf_file in uploaded_cvs:
            try:
                file_bytes = pdf_file.read()
                doc = fitz.open(stream=file_bytes, filetype="pdf")

                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()

                # Extract candidate ID from filename
                candidate_id = os.path.splitext(pdf_file.name)[0]

                # Compute match score
                from agents.recruiting_agent import get_match_score
                match_score = get_match_score(jd_summary, text)

                # Store in DB
                insert_candidate(candidate_id, match_score, text)

                # Append for shortlisting
                candidates.append({
                    "name": candidate_id,
                    "match": match_score,
                    "resume": text
                })

            except Exception as e:
                st.error(f"Error processing {pdf_file.name}: {e}")

        # Shortlist candidates
        shortlisted = shortlister.shortlist(candidates)

        if shortlisted:
            st.subheader("✅ Shortlisted Candidates")
            for candidate in shortlisted:
                st.markdown(f"**🧑 {candidate['name']}** — Match: `{candidate['match']}%`")
                st.text_area("📄 Resume Extract", candidate["resume"], height=200)

                invite = scheduler.generate_invite(candidate["name"], "example@example.com", "Python Developer")
                st.code(invite)
                st.markdown("---")
        else:
            st.warning("⚠️ No candidates matched the criteria.")
import streamlit as st
import pandas as pd
import os
import tempfile
import fitz  # PyMuPDF
from agents.jd_summarizer import job_summarizer
from agents.recruiting_agent import get_match_score
from agents.interview_scheduler import InterviewScheduler
from agents.shortlister import Shortlister
from data_utils import create_db, insert_candidate

# Initialize DB
create_db()

st.title("🧠 AI Recruitment System")
st.write("Upload a job description and candidate resumes to find top matches.")

# Upload job description CSV
jd_file = st.file_uploader("📄 Upload Job Description CSV", type="csv")
cv_files = st.file_uploader("📎 Upload CV PDFs", type="pdf", accept_multiple_files=True)

threshold = st.slider("🎯 Matching Threshold", 0, 100, 80)

if jd_file and cv_files:
    # Read job description
    try:
        df_jd = pd.read_csv(jd_file, encoding='latin1')
        jd_text = df_jd["Job Description"].iloc[0]
    except Exception as e:
        st.error(f"Error reading JD file: {e}")
        st.stop()

    # Summarize job description
    with st.spinner("🔍 Summarizing Job Description..."):
        jd_summary = job_summarizer(jd_text)
        st.subheader("📋 JD Summary")
        st.markdown(jd_summary)

    # Process resumes
    candidates = []
    for file in cv_files:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            doc = fitz.open(tmp_path)
            resume_text = ""
            for page in doc:
                resume_text += page.get_text()

            candidate_id = os.path.splitext(file.name)[0]  # e.g., "C1061"
            match_score = get_match_score(jd_summary, resume_text)
            insert_candidate(candidate_id, match_score, resume_text)
            candidates.append({
                "name": candidate_id,
                "match": match_score,
                "resume": resume_text
            })

        except Exception as e:
            st.error(f"❌ Error reading {file.name}: {e}")

    # Display all candidates
    if candidates:
        st.write("## 📊 All Candidates & Match Scores")
        for c in candidates:
            st.markdown(f"**{c['name']}** — Match Score: `{c['match']}%`")
            with st.expander("📝 View Resume Text"):
                st.text(c['resume'])
            st.markdown("---")

        # Shortlist
        shortlister = Shortlister(threshold)
        shortlisted = shortlister.shortlist(candidates)

        if shortlisted:
            st.success(f"✅ {len(shortlisted)} candidates shortlisted!")
            st.write("## 🏆 Shortlisted Candidates & Interview Invites")
            scheduler = InterviewScheduler()
            for candidate in shortlisted:
                invite = scheduler.generate_invite(candidate["name"], "example@example.com", "Python Developer")
                st.markdown(f"**{candidate['name']}** — Match Score: `{candidate['match']}%`")
                st.code(invite)
        else:
            st.warning("⚠️ No candidates matched the threshold. Try lowering it or verify resume content.")

    else:
        st.warning("No resumes could be processed.")
import streamlit as st
import pandas as pd
import os
import tempfile
import fitz  # PyMuPDF
from agents.jd_summarizer import job_summarizer
from agents.recruiting_agent import get_match_score
from agents.interview_scheduler import InterviewScheduler
from agents.shortlister import Shortlister
from data_utils import create_db, insert_candidate

# Initialize DB
create_db()

st.set_page_config(page_title="AI Recruitment System", layout="wide")
st.title("🤖 AI Recruitment System")
st.write("Upload job descriptions and candidate resumes to find top matches.")

# Upload job description CSV
jd_file = st.file_uploader("📄 Upload Job Description CSV", type="csv")
cv_files = st.file_uploader("📎 Upload CV PDFs", type="pdf", accept_multiple_files=True)

threshold = st.slider("🎯 Matching Threshold (%)", 0, 100, 80)

if jd_file and cv_files:
    try:
        df_jd = pd.read_csv(jd_file, encoding='latin1')

        if "Job Title" not in df_jd.columns or "Job Description" not in df_jd.columns:
            st.error("CSV must contain 'Role' and 'Job Description' columns.")
            st.stop()

        roles = df_jd["Job Title"].unique().tolist()
        selected_roles = st.multiselect("🎯 Select Open Roles", roles)

        if not selected_roles:
            st.info("Please select at least one role to continue.")
            st.stop()

        st.success(f"{len(selected_roles)} role(s) selected. {len(cv_files)} resumes uploaded.")
        st.divider()

        for role in selected_roles:
            st.header(f"🧑‍💼 Role: {role}")
            jd_text = df_jd[df_jd["Role"] == role]["Job Description"].iloc[0]
            jd_summary = job_summarizer(jd_text)

            st.subheader("📋 JD Summary")
            st.markdown(jd_summary)

            # Process candidates for this role
            candidates = []
            for file in cv_files:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(file.read())
                        tmp_path = tmp.name

                    doc = fitz.open(tmp_path)
                    resume_text = ""
                    for page in doc:
                        resume_text += page.get_text()

                    candidate_id = os.path.splitext(file.name)[0]
                    score = get_match_score(jd_summary, resume_text)
                    insert_candidate(candidate_id, score, resume_text)
                    candidates.append({
                        "name": candidate_id,
                        "match": score,
                        "resume": resume_text
                    })

                except Exception as e:
                    st.error(f"❌ Error processing {file.name}: {e}")

            if candidates:
                st.subheader("📊 All Candidates & Match Scores")
                for c in candidates:
                    st.markdown(f"**{c['name']}** — Match Score: `{c['match']}%`")
                    with st.expander("📄 View Resume Text", expanded=False):
                        st.text(c['resume'][:1000])  # truncate for readability

                # Shortlist
                shortlister = Shortlister(threshold)
                shortlisted = shortlister.shortlist(candidates)

                if shortlisted:
                    st.success(f"✅ {len(shortlisted)} candidates shortlisted for {role}!")
                    st.write("## 🏆 Shortlisted Candidates & Interview Invites")
                    scheduler = InterviewScheduler()
                    for candidate in shortlisted:
                        invite = scheduler.generate_invite(candidate["name"], "example@example.com", role)
                        st.markdown(f"**{candidate['name']}** — Match Score: `{candidate['match']}%`")
                        st.code(invite)
                else:
                    st.warning(f"⚠️ No candidates met the {threshold}% threshold for **{role}**.")

            st.divider()

    except Exception as e:
        st.error(f"❌ Error reading JD file: {e}")

import streamlit as st
import pandas as pd
import os
import tempfile
import fitz  # PyMuPDF

from agents.jd_summarizer import job_summarizer
from agents.recruiting_agent import get_match_score
from agents.interview_scheduler import InterviewScheduler
from agents.shortlister import Shortlister
from data_utils import create_db, insert_candidate

# Set Streamlit page config FIRST
st.set_page_config(page_title="AI Recruitment System", layout="wide")

# Initialize DB
create_db()

st.title("🧠 AI Recruitment System")
st.write("Upload a job description and candidate resumes to find top matches for selected **Job Titles**.")

# Uploads
jd_file = st.file_uploader("📄 Upload Job Description CSV", type="csv")
cv_files = st.file_uploader("📎 Upload CV PDFs", type="pdf", accept_multiple_files=True)

threshold = st.slider("🎯 Matching Threshold", 0, 100, 80)

if jd_file and cv_files:
    try:
        df_jd = pd.read_csv(jd_file, encoding="latin1")
        if "Job Title" not in df_jd.columns or "Job Description" not in df_jd.columns:
            st.error("CSV must contain 'Job Title' and 'Job Description' columns.")
            st.stop()

        # User selects job titles
        job_titles = df_jd["Job Title"].unique().tolist()
        selected_jobs = st.multiselect("🎯 Select Job Titles to Screen Candidates For:", job_titles)

        if selected_jobs:
            # Process resumes once and reuse
            candidates = []
            for file in cv_files:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(file.read())
                        tmp_path = tmp.name

                    doc = fitz.open(tmp_path)
                    resume_text = "".join([page.get_text() for page in doc])
                    candidate_id = os.path.splitext(file.name)[0]
                    
                    candidates.append({
                        "name": candidate_id,
                        "resume": resume_text
                    })
                except Exception as e:
                    st.error(f"❌ Error reading {file.name}: {e}")

            # Process each selected job
            for title in selected_jobs:
                st.subheader(f"🔎 Processing for Job Title: `{title}`")
                job_row = df_jd[df_jd["Job Title"] == title].iloc[0]
                jd_text = job_row["Job Description"]

                with st.spinner(f"Summarizing JD for '{title}'..."):
                    jd_summary = job_summarizer(jd_text)
                    st.markdown(f"**JD Summary for {title}:**\n\n{jd_summary}")

                # Match scoring
                matched_candidates = []
                for c in candidates:
                    score = get_match_score(jd_summary, c["resume"])
                    insert_candidate(c["name"], score, c["resume"])
                    matched_candidates.append({
                        "name": c["name"],
                        "match": score,
                        "resume": c["resume"]
                    })

                st.markdown("### 📊 All Candidates for this Job")
                for c in matched_candidates:
                    st.markdown(f"- **{c['name']}** — Match Score: `{c['match']}%`")
                    with st.expander("📝 View Resume Text"):
                        st.text(c["resume"])
                    st.markdown("---")

                # Shortlist
                shortlister = Shortlister(threshold)
                shortlisted = shortlister.shortlist(matched_candidates)

                if shortlisted:
                    st.success(f"✅ {len(shortlisted)} candidates shortlisted for {title}!")
                    scheduler = InterviewScheduler()
                    for candidate in shortlisted:
                        invite = scheduler.generate_invite(candidate["name"], "example@example.com", title)
                        st.markdown(f"**{candidate['name']}** — Match Score: `{candidate['match']}%`")
                        st.code(invite)
                else:
                    st.warning(f"⚠️ No candidates matched threshold for {title}. Try lowering the threshold or reviewing resumes.")

        else:
            st.info("Please select at least one job title.")

    except Exception as e:
        st.error(f"Error processing files: {e}")
else:
    st.info("Please upload both the JD CSV and some resume PDFs to proceed.")
"""
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
st.set_page_config(page_title="🎯 AI Shortlisting System", layout="wide")
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

