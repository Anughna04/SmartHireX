"""from langchain_ollama.llms import OllamaLLM

# Load the Ollama LLM
llama3 = OllamaLLM(model="llama3")

# Agent as a simple function
def job_summarizer(jd_text: str) -> str:
    prompt = (
        "You are a Job Description Summarizer.\n\n"
        "Extract the required skills, qualifications, experience, and responsibilities "
        "from the given JD.\n\n"
        "Return a short, clear summary in bullet points.\n\n"
        f"Job Description:\n{jd_text}"
    )
    return llama3.invoke(prompt)
"""
import os
from groq import Groq

# Set your actual Groq API key here
client = Groq(api_key="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")

def job_summarizer(jd_text):
    prompt = f"Summarize the following job description:\n\n{jd_text}"
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

