import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_groq_api_key():
    api_key = os.getenv("GROQ_API_KEY", "")
    if api_key:
        return api_key
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return ""

def translate_text(language, text):
    api_key = get_groq_api_key()
    if not api_key:
        st.error("Missing GROQ_API_KEY. Add it in Streamlit secrets or environment variables.")
        return None

    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=api_key)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Translate the following into {language}:"),
        ("user", "{text}")
    ])
    parser = StrOutputParser()
    chain = prompt | llm | parser
    return chain.invoke({"language": language, "text": text})

st.title("This is a robot to convert texts in different languages")

st.subheader("please select the language you want to convert in:")
option = st.selectbox(
    "Select one language",
    ("French", "Hindi", "German", "Chinese")
)

input_text = st.text_input(f"Write the text you want to convert to {option}")

if input_text:
    try:
        result = translate_text(option, input_text)
        if result is not None:
            st.write(result)
    except Exception as e:
        st.error(f"Translation failed: {e}")