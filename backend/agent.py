import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from embeddings import search_papers

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

prompt = ChatPromptTemplate.from_template("""
You are an autonomous research agent.

STRICT RULES:
- Answer ONLY using the provided research context
- DO NOT invent information
- DO NOT use placeholders like [Insert ...]
- If information is missing, say "Not found in provided paper"

Research Context:
{context}

Question:
{question}

Give a factual summary based only on the context.
""")


chain = prompt | llm | StrOutputParser()


def agent_answer(question):

    results = search_papers(question)

    docs = results.get("documents", [[]])[0]

    context = "\n\n".join(docs)

    context = context[:4000]

    answer = chain.invoke({
        "context": context,
        "question": question
    })

    return answer
