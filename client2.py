import requests
import streamlit as st
import os


# create a function

def groq_input_response(language,input_text):
    json_body={
        "input":{
            "language":language,
            "text":input_text
        },
        "kwargs":{},
        "config":{}
    }

    backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
    response = requests.post(
        f"{backend_url}/chain/invoke", json=json_body, timeout=60
    )
    response.raise_for_status()
    return response.json()

# streamlit
st.title("This is a robot to convert texts in different languages")

st.subheader("please select the language you want to convert in:")
option=st.selectbox(
    "Select one language",
    ("French",
    "Hindi",
    "German",
    "Chinese")
)

input_text=st.text_input(f"Write the text you want to convert to {option}")

if input_text:
    try:
        res = groq_input_response(option, input_text)
        st.write(res["output"])
    except requests.RequestException:
        st.error("The translation service is unavailable. Please try again shortly.")
    

