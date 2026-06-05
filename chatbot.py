import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Personality Chatbot",
    page_icon="🤖",
    layout="wide",
)

# ---------------------------------------------------
# Load Environment
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .stChatMessage {
        border-radius: 15px;
    }

    .title {
        text-align:center;
        font-size:40px;
        font-weight:bold;
        margin-bottom:10px;
    }

    .subtitle{
        text-align:center;
        color:gray;
        margin-bottom:25px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.markdown(
    '<div class="title">🤖 AI Personality Chatbot</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Choose a personality and start chatting</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------
# Session State Initialization
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = None

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    personality = st.radio(
        "Select AI Personality",
        [
            "Funny 😆",
            "Angry 😡",
            "Sad 😔"
        ],
        index=None
    )

    if st.button("Apply Personality", use_container_width=True):

        if personality == "Funny 😆":
            system_prompt = "You are a funny AI Assistant."

        elif personality == "Angry 😡":
            system_prompt = "You are an angry AI Assistant."

        elif personality == "Sad 😔":
            system_prompt = "You are a sad AI Assistant."

        st.session_state.personality = system_prompt

        st.session_state.messages = [
            SystemMessage(content=system_prompt)
        ]

        st.success("Personality Selected!")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        if st.session_state.personality:

            st.session_state.messages = [
                SystemMessage(
                    content=st.session_state.personality
                )
            ]
        else:
            st.session_state.messages = []

        st.rerun()

# ---------------------------------------------------
# Require Personality Selection
# ---------------------------------------------------

if st.session_state.personality is None:

    st.info(
        "👈 Select a personality from the sidebar and click Apply Personality."
    )
    st.stop()

# ---------------------------------------------------
# Mistral Model
# ---------------------------------------------------

model = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.9
)

# ---------------------------------------------------
# Display Chat History
# ---------------------------------------------------

for msg in st.session_state.messages:

    if isinstance(msg, SystemMessage):
        continue

    if isinstance(msg, HumanMessage):

        with st.chat_message("user"):
            st.markdown(msg.content)

    elif isinstance(msg, AIMessage):

        with st.chat_message("assistant"):
            st.markdown(msg.content)

# ---------------------------------------------------
# User Input
# ---------------------------------------------------

prompt = st.chat_input(
    "Type your message..."
)

if prompt:

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    # AI Response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = model.invoke(
                st.session_state.messages
            )

            st.markdown(response.content)

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )