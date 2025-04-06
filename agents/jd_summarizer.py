from langchain_ollama.llms import OllamaLLM

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
