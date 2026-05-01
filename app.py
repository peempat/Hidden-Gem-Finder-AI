from google import genai
from groq import Groq
from qdrant_client import QdrantClient
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
# ── Config ──────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")

gemini = genai.Client(api_key=GEMINI_API_KEY)
groq   = Groq(api_key=GROQ_API_KEY)
qdrant = QdrantClient(path="./qdrant_storage")  # โหลดจาก disk

# ── Functions ────────────────────────────────────────
def retrieve(query, top_k=5):
    result = gemini.models.embed_content(
        model="gemini-embedding-2",
        contents=query
    )
    hits = qdrant.query_points(
        collection_name="thailand_provinces",
        query=result.embeddings[0].values,
        limit=top_k
    ).points
    return [{"text": h.payload["text"]} for h in hits]

def llm_generate(prompt):
    response = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content

def agent_chat(user_message):
    results  = retrieve(user_message)
    context  = "\n\n---\n\n".join([r["text"] for r in results])
    prompt   = f"""
You are a friendly travel companion for Nakhon Nayok, Thailand.
Help foreign tourists plan their trip with practical, honest advice.
Always include prices in both THB and USD.

CONTEXT:
{context}

USER: {user_message}
ASSISTANT:"""
    return llm_generate(prompt)

# ── Streamlit UI ─────────────────────────────────────
st.title("🌿 Nakhon Nayok Hidden Gem")
st.caption("Your AI travel companion for Thailand's best kept secret")

if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดง chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# รับ input
user_input = st.chat_input("Ask me anything about Nakhon Nayok...")
if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Finding the best answer..."):
        response = agent_chat(user_input)

    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})