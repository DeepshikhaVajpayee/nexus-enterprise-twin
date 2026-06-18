import os
from dotenv import load_dotenv
from groq import Groq
from app.services.context_builder import build_context

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_llm_answer(question: str):
    context = build_context()

    prompt = f"""
You are Nexus AI COO, an executive decision intelligence agent.

Use ONLY the enterprise context below.
Give a concise executive answer with:
1. Current situation
2. Priority risk
3. Recommended action

Enterprise Context:
{context}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
