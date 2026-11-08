import streamlit as st
import re
from openai import OpenAI

try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_KEY = ""

client = OpenAI(
    api_key=GROQ_KEY,
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="ZimWAI Farm", page_icon="🌾")

st.title("🌾 ZimWAI Farm")
st.write("Your smart farming helper for Zimbabwe 🇿🇼")

language = st.selectbox(
    "Choose language / Sarudza mutauro / Khetha ulimi",
    ["English", "Shona", "Ndebele"]
)

st.write("### Quick questions — just click one:")
col1, col2, col3, col4 = st.columns(4)

clicked = None
with col1:
    if st.button("🌽 Maize"):
        clicked = "When should I plant maize in Bulawayo? What fertiliser and spacing?"
with col2:
    if st.button("🥜 Groundnuts"):
        clicked = "How do I grow groundnuts in Zimbabwe? Best variety and spacing?"
with col3:
    if st.button("🐔 Chickens"):
        clicked = "How do I raise broiler chickens for profit in Zimbabwe? Feed and vaccines?"
with col4:
    if st.button("🐄 Cattle"):
        clicked = "How do I take care of cattle in dry season in Matabeleland?"

question = st.text_input("Or type your own question here...")

final_question = clicked if clicked else question

if final_question:
    with st.spinner("ZimWAI is thinking..."):
        models_to_try = ["llama-3.3-70b-versatile", "openai/gpt-oss-120b", "llama-3.1-8b-instant"]
        answer = None
        for model_name in models_to_try:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": f"You are a helpful farming expert in Zimbabwe for a smallholder farmer in Bulawayo. Answer simply, with practical steps, prices in USD if possible, and local varieties. Answer in {language}. Never use tables. Use only bullet points and headings. Do NOT use HTML tags like <br> or <p>."},
                        {"role": "user", "content": final_question}
                    ]
                )
                answer = response.choices[0].message.content
                # Remove ANY html tag like <br>, <p>, etc
                answer = re.sub(r"<[^>]+>", " ", answer)
                break
            except Exception:
                continue

        if answer:
            st.success("Here is your answer:")
            st.markdown(answer)
        else:
            st.error("Still busy, wait a few seconds and try again.")

st.divider()
st.caption("Made in Bulawayo with ❤️ — ZimWAI")