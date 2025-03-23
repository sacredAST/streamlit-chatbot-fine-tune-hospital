from openai import AzureOpenAI
import streamlit as st

st.title("Chat Bot with Fine-tuned model (Hospital-ws-bot)")

client = AzureOpenAI(
    azure_endpoint = st.secrets["AZURE_OPENAI_API_URL"], 
    api_key=st.secrets["AZURE_OPENAI_API_KEY"], 
    api_version=st.secrets["AZURE_OPENAI_API_VERSION"]
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = st.secrets["FINE_TUNED_MODEL_NAME"]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})