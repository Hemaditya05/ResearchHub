import os
from groq import Groq
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Create Groq client using API key
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, context):

    prompt = f"""
You are an advanced research assistant.

Research Context:
{context}

User Question:
{question}

Give a clear, professional research-based answer.
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {"role": "user", "content": prompt}
        ],

        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content
