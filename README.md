SmartHireX 🤖💼
Revolutionizing Recruitment with Multi-Agent AI
📌 Overview
SmartHireX is a cutting-edge, AI-driven recruitment solution that simplifies the hiring process by automating resume screening, candidate shortlisting, and interview scheduling. It uses multi-agent architecture, LLMs (like LLaMA3, Phi-3, etc.), and Streamlit for a seamless, end-to-end hiring workflow tailored for modern organizations.

🎥 Demo Video


📌 Features
✅ Multi-Agent System – Individual AI agents for job summarization, resume parsing, candidate scoring, shortlisting, and interview scheduling.
✅ LLM-Powered Matching – Uses Ollama LLMs and custom embeddings (mxbai-embed-large) for accurate candidate-job matching.
✅ Streamlit UI – Clean, interactive UI for uploading CVs, job descriptions, and managing the hiring pipeline.
✅ Auto Interview Scheduler – Automatically drafts and schedules interviews for top candidates.
✅ SQLite Memory – Persistent and efficient data storage for job and candidate data.

🚀 Technologies Used
Programming Language: Python 🐍

Web Framework: Streamlit 🌐

AI Models: Ollama (LLaMA3, Phi-3), mxbai-embed-large for embeddings 🤖

Data Parsing: PyMuPDF for CV reading

Database: SQLite 🗄️

UI Tools: Streamlit, HTML/CSS for styling 🎨

Emailing: SMTP for interview invites ✉️

Deployment: Can be deployed on Streamlit Cloud / AWS / GCP ☁️

📂 Project Structure
bash
Copy
Edit
SmartHireX/
│── app.py                  # Streamlit UI logic
│── main.py                 # Core script that runs agents and coordinates flow
│── jd_summarizer.py        # Agent for summarizing job descriptions
│── recruiting_agent.py     # Agent that extracts, scores, and matches resumes
│── shortlister.py          # Agent that filters top candidates
│── interview_scheduler.py  # Agent that schedules interviews and sends invites
│── data_utils.py           # SQLite DB operations
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
🔧 Installation & Setup
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/Anughna04/SmartHireX.git
cd SmartHireX
Install Required Libraries:

bash
Copy
Edit
pip install -r requirements.txt
Run the Streamlit App:

bash
Copy
Edit
streamlit run app.py
This will launch SmartHireX in your browser.

💡 How It Works
Upload a .csv file containing job descriptions.

Upload a folder of resumes (.pdf format) named by candidate ID (e.g., C1061.pdf).

The system summarizes the job, parses resumes, matches candidates, and shows a shortlist.

Optionally, send automated interview invites to shortlisted candidates.

📧 Contact
For any queries, reach out to anughnakandimalla11@gmail.com.

Let me know if you'd like to customize the style more or generate a requirements.txt if it's not ready!







You said:
ta Parsing: PyMuPDF for CV reading..why did i use fitz..what is fitz


ChatGPT said:
Great question!

🔍 Why you used fitz:
You used fitz because it's PyMuPDF's interface. Essentially:

✅ fitz is the Python module name for using PyMuPDF.

🧠 What's the relationship?
PyMuPDF is the library/package name.

fitz is the import name (the actual module you use in your code).

So when you write:

python
Copy
Edit
import fitz  # this is PyMuPDF
You're using PyMuPDF's API via the fitz namespace.

🔧 Why it's named fitz:
Historically, PyMuPDF was developed on top of MuPDF, and fitz was the internal name of the interface they exposed early on. Even though the library is now officially called PyMuPDF, the fitz module name stuck for backward compatibility.

🛠 What can you do with fitz (PyMuPDF)?
Extract text from PDFs (structured or unstructured)

Access metadata (author, page count, etc.)

Extract images, fonts, tables

Render pages to images

Highlight, annotate, or redact PDFs

Example:

python
Copy
Edit
import fitz  # aka PyMuPDF

doc = fitz.open("resume.pdf")
text = ""
for page in doc:
    text += page.get_text()
Let me know if you want a short code snippet that shows how you're using fitz to extract candidate information!







You said:
SmartHireX is a cutting-edge, AI-driven recruitment solution that simplifies the hiring process by automating resume screening, candidate shortlisting, and interview scheduling. It uses multi-agent architecture, LLMs (like LLaMA3, Phi-3, etc.), and Streamlit for a seamless, end-to-end hiring workflow tailored for modern organizations...i used llama3 model via ollama not phi-3


ChatGPT said:
Memory updated
Got it! I've noted that you're using the LLaMA3 model via Ollama, not Phi-3, in the SmartHireX project. Let me know if you'd like help updating this in your README, pitch, or anywhere else!







You said:
update the readme


ChatGPT said:
Here’s the updated README.md for SmartHireX with the format and tone similar to your PathFinder.AI README, and corrected to show that you're using LLaMA3 via Ollama (not Phi-3 or anything else):

SmartHireX 🤖
AI-Powered Recruitment Redefined – Screen Smarter, Hire Faster!
📌 Overview
SmartHireX is a cutting-edge, AI-driven recruitment solution that simplifies the hiring process by automating resume screening, candidate shortlisting, and interview scheduling. It leverages a multi-agent architecture, LLMs (LLaMA3 via Ollama), and Streamlit for a seamless, end-to-end hiring workflow tailored for modern organizations.

🎥 Demo Video
(Include demo.gif or YouTube link here)

📌 Features
✅ Automated Resume Parsing – Extract structured data from unstructured PDF resumes.
✅ Intelligent JD Understanding – Uses LLaMA3 to summarize job descriptions efficiently.
✅ Candidate Scoring – Embedding-based matching using mxbai-embed-large and SQLite for memory.
✅ Shortlisting System – Filter candidates based on configurable match thresholds.
✅ Interview Scheduler – Auto-generates interview invitation emails.
✅ Streamlit UI – Intuitive app interface for uploading JDs, CVs, viewing results, and sending invites.

🚀 Technologies Used
Programming Language: Python 🐍

Web Framework: Streamlit 🌐

LLM: LLaMA3 via Ollama 🦙

Embeddings: mxbai-embed-large

Resume Parsing: PyMuPDF (fitz)

Database: SQLite 💾

Email Service: SMTP (for interview invites)

📂 Project Structure
bash
Copy
Edit
SmartHireX/
│── app.py                 # Streamlit UI
│── main.py                # Orchestrates end-to-end pipeline
│── jd_summarizer.py       # LLaMA3-based JD summarization agent
│── recruiting_agent.py    # Embedding-based matching and scoring
│── shortlister.py         # Candidate filtering logic
│── interview_scheduler.py # Generates interview invitation emails
│── data_utils.py          # Handles SQLite interactions
│── CVs/                   # Folder containing candidate resumes
│── job_description.csv    # Uploaded job descriptions
│── requirements.txt       # Dependencies
│── README.md              # Project documentation
🔧 Installation & Setup
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/Anughna04/SmartHireX.git
cd SmartHireX
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Start Ollama & Pull LLaMA3 Model:

bash
Copy
Edit
ollama run llama3
Run the Streamlit App:

bash
Copy
Edit
streamlit run app.py
💡 How It Works
Upload a job description CSV and CV folder.

JD Summarizer (LLaMA3) extracts key requirements.

Resume Extractor parses PDFs using PyMuPDF (fitz).

Recruiting Agent scores candidates using embedding similarity.

Shortlister filters top candidates based on match score.

Interview Scheduler drafts personalized emails for selected candidates.

📧 Contact
For any queries, reach out to anughnakandimalla11@gmail.com.

