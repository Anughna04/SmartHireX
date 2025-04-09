## SmartHireX 
### **AI-Powered Hiring. Smarter. Faster. Fairer.**

## 📌 Overview
**SmartHireX is a cutting-edge, AI-driven recruitment solution that simplifies the hiring process by automating resume screening, candidate shortlisting, and interview scheduling. It leverages a multi-agent architecture, LLMs (LLaMA3 via Ollama), and Streamlit for a seamless, end-to-end hiring workflow tailored for modern organizations.

## 🎥 Demo Video
![Demo GIF](SmartHireX_demo.gif)

## 📌 Features
- ✅ Multi-Agent System – Individual AI agents for job summarization, resume parsing, candidate scoring, shortlisting, and interview scheduling.
- ✅ LLM-Powered Matching – Uses Ollama LLMs and custom embeddings (mxbai-embed-large) for accurate candidate-job matching.
- ✅ Streamlit UI – Clean, interactive UI for uploading CVs, job descriptions, and managing the hiring pipeline.
- ✅ Auto Interview Scheduler – Automatically drafts and schedules interviews for top candidates.
- ✅ SQLite Memory – Persistent and efficient data storage for job and candidate data.

## 🚀 Technologies Used
- Programming Language: Python 
- Web Framework: Streamlit 🌐
- AI Models: Ollama (LLaMA3, Phi-3), mxbai-embed-large for embeddings 🤖
- Data Parsing: PyMuPDF for CV reading
- Database: SQLite 🗄️
- UI Tools: Streamlit, HTML/CSS for styling 🎨
- Emailing: SMTP for interview invites ✉️
- Deployment: Can be deployed on Streamlit Cloud / AWS / GCP ☁️

## 📂 Project Structure
```
SmartHireX/
│── app.py                  # Streamlit UI
│── main.py                 # Main pipeline controller
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
│
├── agents/                 # Multi-agent architecture components
│   ├── jd_summarizer.py       # JD Summarizer using LLaMA3
│   ├── recruiting_agent.py    # Matches resumes with job requirements
│   ├── shortlister.py         # Filters candidates based on match score
│   ├── interview_scheduler.py # Generates interview emails
│
├── utils/
│   ├── data_utils.py          # SQLite DB and helper functions
│
├── data/
│   ├── job_description.csv    # Uploaded job description(s)
│   ├── CVs/                   # Folder containing candidate resumes (PDFs)
```

## 🔧 Installation & Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Anughna04/SmartHireX.git
   cd SmartHireX
   ```

2. **Install Required Libraries:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start Ollama & Pull LLaMA3 Model:**
   ```
   ollama run llama3
   ```
4. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

##  How It Works
- Upload a job description CSV and CV folder.

- JD Summarizer (LLaMA3) extracts key requirements.

- Resume Extractor parses PDFs using PyMuPDF (fitz).

- Recruiting Agent scores candidates using embedding similarity.

- Shortlister filters top candidates based on match score.

- Interview Scheduler drafts personalized emails for selected candidates

---
### 📧 Contact
For any queries, reach out to **[anughnakandimalla11@gmail.com](mailto:anughnakandimalla11@gmail.com)**.
