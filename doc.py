'''from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

a=TextLoader(file_path='C:\gen ai\sim.text',encoding='utf-8')
text=a.load()
print(text[0].page_content)

Brain=ChatOpenAI()

prompt=PromptTemplate(
    template='summarise the {text} given in 10 bullets point and create 10 question and answer that',
    input_variables=['text']
)

parser=StrOutputParser()
chain=prompt|Brain|parser
print(chain.invoke({'text':text[0].page_content}))
'''
#import login_shesafe
#import about
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import streamlit as st
import os
from datetime import datetime


# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize LLM
llm = ChatOpenAI(api_key=openai_api_key, temperature=0.7, model="gpt-4o-mini")

# Page setup
st.set_page_config(page_title="SheSafe", page_icon="💙", layout="centered")
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/free-photo/dark-abstract-background_1048-1920.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
    .user-bubble {
        background-color: #932F67;
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 5px;
        display: inline-block;
        max-width: 80%;
    }
    .bot-bubble {
        background-color: #B9375D;
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 5px;
        display: inline-block;
        max-width: 80%;
    }
    .timestamp {
        font-size: 10px;
        color: gray;
        margin-top: -5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image(
    "https://csrbox.org/company/proj_img/1598254332women%20safety.png",
    use_container_width=True
)




# Sidebar Navigation
page = st.sidebar.radio("Navigate", ["💌 Emotional Support", "⚖️ Legal Guidance", "🚨 Emergency Resources"])


# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {"role": "user"/"assistant", "content": "text", "time": "timestamp"}

# Emotional Support Page
if page == "💌 Emotional Support":
    st.header("💌 Emotional Support Chat")
    st.write("Your safe space to talk. Messages are private and not stored anywhere outside this session.")

    # Show past messages in bubble style
    for chat in st.session_state.chat_history:
        timestamp_html = f"<div class='timestamp'>{chat['time']}</div>"
        if chat["role"] == "user":
            st.markdown(f"<div class='user-bubble'><b>You:</b> {chat['content']}</div>{timestamp_html}", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'><b>SheSafe:</b> {chat['content']}</div>{timestamp_html}", unsafe_allow_html=True)

    user_input = st.text_input("Type your message...", key="support_input")

    if st.button("Send", key="support_btn"):
        if not user_input.strip():
            st.warning("Please enter a message.")
        else:
            current_time = datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({"role": "user", "content": user_input, "time": current_time})

            with st.spinner("SheSafe is responding..."):
                template = """
                You are SheSafe, a compassionate AI that provides emotional comfort to women in distress.
                Respond in a warm, empathetic, and supportive way without judgment.
                Avoid giving legal or medical advice unless explicitly asked.

                Conversation so far:
                {history}

                User's latest message:
                {message}
                """
                history_text = "\n".join(
                    [f"{'User' if c['role']=='user' else 'SheSafe'}: {c['content']}" for c in st.session_state.chat_history]
                )

                prompt = PromptTemplate(input_variables=["history", "message"], template=template)
                chain = prompt | llm | StrOutputParser()
                response = chain.invoke({"history": history_text, "message": user_input})

            current_time = datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({"role": "assistant", "content": response, "time": current_time})
            st.rerun()

# Legal Guidance Page
elif page == "⚖️ Legal Guidance":
    st.header("⚖️ Legal Guidance")
    st.write("Ask about women's safety laws in India. (For awareness only, not legal advice.)")
    legal_query = st.text_input("Enter your question here:")

    if st.button("Get Guidance", key="legal_btn"):
        if not legal_query.strip():
            st.warning("Please enter a legal question.")
        else:
            with st.spinner("Fetching legal information..."):
                template = """
                You are SheSafe, an AI assistant that provides general legal awareness to women in India.
                Answer in simple language. Include relevant sections of IPC, Criminal Law (Amendment), or other acts.
                Do not give legal advice, only information.

                User's question:
                {message}
                """
                prompt = PromptTemplate(input_variables=["message"], template=template)
                chain = prompt | llm | StrOutputParser()
                response = chain.invoke({"message": legal_query})

            st.subheader("📜 Legal Information")
            st.write(response)

# Emergency Resources Page
elif page == "🚨 Emergency Resources":
    st.header("🚨 Emergency Helplines & Resources")
    st.write("In case of danger, please contact these helplines immediately:")

    st.markdown("""
    **🚓 Police (All India):** 100  
    **👩‍🦰 Women Helpline:** 1091  
    **📱 Women Helpline (Mobile):** 181  
    **📞 Domestic Violence Helpline:** 181  
    **🆘 Child Helpline:** 1098  

    **💜 NGO - Women Safety:**  
    - [Snehi Helpline](http://www.snehi.org) - 9582208181  
    - [Sakhi Helpline](https://www.ncw.nic.in) - 011-26944880  
    """)
    st.success("Stay safe. You are not alone 💙")
