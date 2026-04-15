#Needs to be able to take and output data in streamlit make it looka pretty and clean
#This is placeholder code from previous class assignment it will be deleted and new code will be added but it is here for now to provide an example
# Anime DLC Store - Chat Assistant
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage,
SystemMessage
load_dotenv() # loads environment variables from .env file,
including GOOGLE_API_KEY

# PAGE CONFIG
st.set_page_config(
page_title="Anime DLC Assistant",
page_icon="￿",
layout="centered",
)

# INITIALIZE SESSION STATE
if "messages" not in st.session_state:
st.session_state.messages = [] # stores {role,
content} dicts for display
if "chat_history" not in st.session_state:
# LangChain message objects for the LLM
st.session_state.chat_history =
[SystemMessage(content=SYSTEM_PROMPT)]

# HEADER
st.markdown("### ￿ Yuki-AI &nbsp; <small
style='color:#888;font-size:0.7rem;'>Anime DLC
Assistant</small>", unsafe_allow_html=True)
st.markdown("<p style='color:#888;font-size:0.78rem;margin-
top:-10px;'>Ask me about DLC, anime characters, or
games!</p>", unsafe_allow_html=True)
st.divider()

# LOAD GEMINI MODEL via LangChain
@st.cache_resource
def load_model():
"""Load the Gemini model. Cached so it only loads
once."""
api_key = os.environ.get("GOOGLE_API_KEY", "")
if not api_key:
return None
return ChatGoogleGenerativeAI(
model="gemini-2.5-flash",
google_api_key=api_key,
temperature=0.7, # slight creativity
for friendly chat
convert_system_message_to_human=True, # Gemini
requires
)
llm = load_model()

# DISPLAY CHAT HISTORY
if not st.session_state.messages:
# Show welcome message on first load
with st.chat_message("assistant"):
st.markdown("Hey there! I'm **Yuki-AI**, your Anime
DLC guide! \n\nI can help you find the perfect DLC pack for
your SteamDeck. Which anime series are you into?")
else:
for msg in st.session_state.messages:
with st.chat_message(msg["role"]):
st.markdown(msg["content"])

# CHAT INPUT
user_input = st.chat_input("Ask about DLC, anime, or SteamDeck
games...")
if user_input:
# 1. user message
with st.chat_message("user"):
st.markdown(user_input)
st.session_state.messages.append({"role": "user", "content":
user_input})
# 2. Add to LangChain history, call Gemini
st.session_state.chat_history.append(HumanMessage(content=use
r_input))
if llm is None:
# No API key - show helpful error
response_text = (
"**No API key found.**\n\n"
"Set your Gemini API key before starting:\n"
"```bash\nexport GOOGLE_API_KEY='your-key-
here'\n```\n"
"Get a free key at [Google AI
Studio](https://aistudio.google.com)."
)
else:
# Call the Gemini model
with st.spinner("Yuki-AI is thinking..."):
try:
response =
llm.invoke(st.session_state.chat_history)
response_text = response.content
# Add AI response to LangChain history for multi-
turn memory
st.session_state.chat_history.append(AIMessage(co
ntent=response_text))
except Exception as e:
response_text = f"Error calling Gemini API:
`{str(e)}`"
# 3. Show response
with st.chat_message("assistant"):
st.markdown(response_text)
st.session_state.messages.append({"role": "assistant",
"content": response_text})
