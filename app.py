import openai
from openai import AzureOpenAI
import streamlit as st
import toml

secrets = toml.load("streamlit/secrets.toml")

st.title("Chat Bot with Fine-tuned model (Hospital-ws-bot)")

openai.api_key = secrets["OPENAI_API_KEY"]

client = AzureOpenAI(
    azure_endpoint = secrets["AZURE_OPENAI_API_URL"], 
    api_key=secrets["AZURE_OPENAI_API_KEY"], 
    api_version=secrets["AZURE_OPENAI_API_VERSION"]
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = secrets["FINE_TUNED_MODEL_NAME"]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})