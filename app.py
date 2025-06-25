import streamlit as st
import requests

st.set_page_config(page_title="PyXpert", page_icon="💡")
st.title("💡 PyXpert – Your Expert Python & AI Assistant")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-Small-3.1-24B-Instruct-2503"

user_input = st.text_input("Ask PyXpert a question:")

if user_input:
    headers = {
        "Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}",
        "Content-Type": "application/json"
    }

    # Expert system prompt
    system_prompt = """
    You are PyXpert, an expert Python and AI mentor trained to help students and developers with programming, data science, and machine learning.
    - Provide accurate, clear, and structured answers.
    - Explain code in Python.
    - Support debugging and project guidance.
    - Simplify complex topics while staying concise.
    - Never make up facts.
    """

    prompt = f"[INST] <<SYS>>{system_prompt}<</SYS>> {user_input} [/INST]"

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7, "max_new_tokens": 350}
    }

    with st.spinner("PyXpert is thinking..."):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            reply = result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text')
            st.markdown(reply or "No response generated.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
