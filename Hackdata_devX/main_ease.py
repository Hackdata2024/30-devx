import streamlit as st
from streamlit_option_menu import option_menu
import time
from main_csv import Scraped_data
from openai import OpenAI
from main_user import user


client = OpenAI(api_key="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")


st.set_page_config(page_title="LegalEase", page_icon=":student:")


def main():
    st.title('LegalEase')
    st.subheader("Your Solution To Legal Troubles")

    st.markdown(
    """
    <style>
        .title {
            font-family: 'Arial', sans-serif;
            font-size: 10px;
            color: #3498db;
        }
        body {
            color: #333;
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
        }
        .sidebar .sidebar-content {
            background-color: #2c3e50;
            color: #ecf0f1;
        }
        .sidebar .sidebar-content .stButton {
            background-color: #3498db;
            color: #ecf0f1;
        }
        .sidebar .sidebar-content .stButton:hover {
            background-color: #2980b9;
        }
        .main .block-container {
            max-width: 900px;
            margin: 0 auto;
        }
        .main .block-container img {
            max-width: 100%;
            height: auto;
        }
        .main .st-file-uploader span {
            color: #3498db;
        }
        .footer {
            background-color: #2c3e50;
            color: #ecf0f1;
            text-align: center;
            padding: 10px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
    )
    
    selected = option_menu(
        menu_title=None, #required
        options=["Home","Analysis","Chatbot", "About Us", "Contact"], #required
        icons=["house","pencil","chat", "book", "phone"], #optional
        menu_icon="cast", #optional
        default_index=0,
        orientation="horizontal",
    )

    if selected == "Home":
        home()

    elif selected == "Analysis":
        analysis()

    elif selected == "About Us":
        about_us()

    elif selected == "Chatbot":
        chatbot()

def home():
    user()


def analysis():
    st.subheader('Perform an Analysis of your legal issue')
    Scraped_data()

def about_us():
    st.write('''LegalEase is your solution to legal problems through our Analysis Tool and AI Law Assistant.
                 \n The Virtual Law Assistant, a chatbot-like feature, provides immediate, step-by-step guidance to individuals facing legal incidents, 
                helping them navigate their way to justice. 
                 \n The Analysis Tool is a robust resource for legal professionals, 
                conducting comprehensive research on previous cases related to specific legal sections and providing case analyses to aid lawyers 
                in court proceedings. 
                 \n LegalEase aims to democratize access to legal information, empower individuals to understand their 
                rights, and equip lawyers with data-driven insights to enhance their legal strategies \n\n\n\n
                 \n\n\n\n\n Built by Team DevX during Hackdata\n\n Team members: Kunal Sharan, Sanskar Sugandhi, Rachit Anand, Akansh Saraf''')
    
def chatbot():
    st.subheader('LegalEase AI ChatBot: Your Personal Law Assistant')
    user_emoji='\U0001F464'
    chatbot_emoji='\U0001F468\U0001F3FC\u200D\u2696\uFE0F'
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.chat_message(chatbot_emoji):
        st.markdown("How can I help solve your legal trouble today?")

    for message in st.session_state.messages[1:]:
        role_icon = user_emoji if message["role"] == "user" else chatbot_emoji
        with st.chat_message(role_icon):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message(user_emoji):
            st.markdown(prompt)

        with st.chat_message(chatbot_emoji):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

def openAPI(user_input):

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Work as a legal assistant. I will give you the problem statement in the next prompt. First, just in case its an emergency, give the local police contact details according to the kind of the problem. Give it in the following format - ' In case of an emergency, please contact your local police station using the following number under Section PCR: 112'.  Then, provide under which section\sections of the Indian Penal Code the issue could fall under. After this, provide a roadmap with roughly 4-6 detailed steps as to how the user should proceed with their legal issue. Do not include anything about this not constituting legal advice and dont include anything like ' remember its crucial to consult a lawyer' or anything like that after the roadmap steps please. I will give the problem statement in the next prompt so respond then"},
        {"role": "user", "content": user_input},])

    res = response.choices[0].message.content
    return res

main()