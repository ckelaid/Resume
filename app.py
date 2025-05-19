import streamlit as st
import openai
from openai import OpenAI
# from utils import build_prompt
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Load OpenAI key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Load your profile
with open("Chat_About_Me.txt", "r") as f:
    about_me_context = f.read()

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"{about_me_context}"}
    ]

# Page configuration
st.set_page_config(page_title="Carlos Kelaidis - Interactive Resume", page_icon="🤖")  # 💼

# Top section: Title, Location, Date
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("### 📈 Sr. Data Scientist")

with col2:
    st.markdown("### 📍 Somehwere, US")

with col3:
    today = datetime.today().strftime("%m/%d/%Y")
    st.markdown(f"### 📅 {today}")

st.markdown("---")

# Main greeting
st.markdown("## 👋 Hello hello, I'm **Carlos Kelaidis**")

# Bio section
st.markdown("""
###### - 🇨🇭🇬🇷 Swiss and Greek national, raised in Greece - fluent in English, French, and Greek, sprinkle some German in there.  
###### - 🎾 Studied in the US on an athletic scholarship playing D1 tennis for Clemson University — I was ranked #75 in the US. Far gone are the glory days.  
###### - 🤖 Now working in data science because predicting stuff is cool.  
###### - ☕ I pack greek coffee with me everywhere I go because the US has terrible coffee standards, but shush don’t tell 'em 🤫  
""")


# Store temporary input text
if "user_input" not in st.session_state:
    st.session_state.user_input = ""


# Chat UI
st.markdown("## 💬 Ask me anything")

# Input field with submit button
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("", value=st.session_state.user_input, placeholder="e.g., What projects have you worked on?")
    submit = st.form_submit_button("Send")


if submit and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI's API
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.3
        )
        mr_los_reply = response.choices[0].message.content
        
   
    st.session_state.messages.append({"role": "assistant", "content": mr_los_reply})
    st.session_state.user_input = ""
    # st.rerun()

# V2
with st.container():
    chat_box = ""
    for msg in st.session_state.messages[1:]:  # skip system prompt
        # if msg["role"] == "user":
        #     chat_box += f"**You: ** {msg['content']}\n\n"
        if msg["role"] == "assistant":
            chat_box += f"{msg['content']}\n\n"

    st.markdown(
        f"""
            <div style='height: 300px; overflow-y: auto; padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 10px;'>
            {chat_box}\n\n</div>
        """, # chr(92) == \ => works with f-string #.replace(f'{chr(92)}n', '<br>')
        unsafe_allow_html=True
    )

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = [
        {"role": "system", "content": f"{about_me_context}"}
    ]
    st.rerun()



# V1
# user_input = st.text_input("", placeholder="e.g., What projects have you worked on?")

# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # Call OpenAI's API
#     with st.spinner("Thinking..."):
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=st.session_state.messages,
#             temperature=0.1
#         )
#         mr_los_reply = response.choices[0].message.content
#         st.session_state.messages.append({"role": "assistant", "content": mr_los_reply})

# # Display the conversation
# for msg in st.session_state.messages[1:]:  # skip the system prompt
#     if msg["role"] == "user":
#         st.markdown(f"**You:** {msg['content']}")
#     else:
#         st.markdown(f"**Carlitos:** {msg['content']}")
        




