import streamlit as st
import random
from dialogue_manager import get_bot_reply  # 🔹 integrate your dialogue manager

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Global Wellness Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION ----------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'page' not in st.session_state:
    st.session_state.page = 'Login'
if 'users' not in st.session_state:
    st.session_state.users = {
        'user': {
            'password': 'pass',
            'email': 'user@example.com',
            'language': 'English',
            'full_name': 'Demo User',
            'age': 30,
            'gender': 'Male'
        }
    }

# ---------------- TRANSLATIONS ----------------
translations = {
    'English': {
        'register': 'Register','login': 'Login','profile_update': 'Profile Update','chat': 'Chat',
        'username': 'Username','password': 'Password','email': 'Email','full_name': 'Full Name',
        'age': 'Age','gender': 'Gender','male': 'Male','female': 'Female','other': 'Other',
        'submit': 'Submit','logout': 'Logout','welcome': 'Welcome','type_message': 'Type your message...',
        'send': 'Send','login_success': 'Login successful!','register_success': 'Registration successful! Please login.',
        'profile_update_success': 'Profile updated successfully!','select_language': 'Select Language'
    },
    'Telugu': {
        'register': 'నమోదు','login': 'లాగిన్','profile_update': 'ప్రొఫైల్ నవీకరణ','chat': 'చాట్',
        'username': 'వినియోగదారు పేరు','password': 'పాస్వర్డ్','email': 'ఇమెయిల్','full_name': 'పూర్తి పేరు',
        'age': 'వయస్సు','gender': 'లింగం','male': 'పురుషుడు','female': 'స్త్రీ','other': 'ఇతర',
        'submit': 'సమర్పించండి','logout': 'లాగ్అవుట్','welcome': 'స్వాగతం','type_message': 'మీ సందేశాన్ని టైప్ చేయండి...',
        'send': 'పంపండి','login_success': 'లాగిన్ విజయవంతమైనది!','register_success': 'నమోదు విజయవంతమైనది! దయచేసి లాగిన్ చేయండి.',
        'profile_update_success': 'ప్రొఫైల్ విజయవంతంగా నవీకరించబడింది!','select_language': 'భాషను ఎంచుకోండి'
    }
}

# ---------------- HELPERS ----------------
def navigate_to(page): st.session_state.page = page

def login_user(username, password):
    if username in st.session_state.users and st.session_state.users[username]['password'] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.language = st.session_state.users[username].get('language', 'English')
        navigate_to('Chat'); return True
    return False

def register_user(username, password, email, full_name, age, gender, language):
    if username in st.session_state.users: return False
    st.session_state.users[username] = {
        'password': password,'email': email,'full_name': full_name,
        'age': age,'gender': gender,'language': language
    }
    return True

def update_profile(username, email, full_name, age, gender, language):
    if username in st.session_state.users:
        st.session_state.users[username].update({
            'email': email,'full_name': full_name,'age': age,'gender': gender,'language': language
        })
        st.session_state.language = language
        return True
    return False

# ---------------- UI ----------------
def render_navigation():
    cols = st.columns([1,1,1,1,1,4])
    t = translations[st.session_state.language]

    with cols[0]:
        if st.button(t['register'], use_container_width=True): navigate_to('Register')
    with cols[1]:
        if st.button(t['login'], use_container_width=True): navigate_to('Login')
    with cols[2]:
        if st.session_state.logged_in and st.button(t['profile_update'], use_container_width=True): navigate_to('Profile Update')
    with cols[3]:
        if st.session_state.logged_in and st.button(t['chat'], use_container_width=True): navigate_to('Chat')
    with cols[4]:
        if st.session_state.logged_in and st.button("Admin", use_container_width=True): navigate_to('Admin')

    with cols[5]:
        selected_language = st.selectbox(
            "Choose Language",
            options=['English','Telugu'],
            index=['English','Telugu'].index(st.session_state.language),
            key='lang_selector'
        )
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language; st.rerun()

def render_login():
    t = translations[st.session_state.language]
    with st.form("login_form"):
        username = st.text_input(t['username'])
        password = st.text_input(t['password'], type="password")
        if st.form_submit_button(t['login']):
            if login_user(username, password): st.rerun()
            else: st.error("Invalid username or password")

def render_register():
    t = translations[st.session_state.language]
    with st.form("register_form"):
        username = st.text_input(t['username'])
        password = st.text_input(t['password'], type="password")
        email = st.text_input(t['email'])
        full_name = st.text_input(t['full_name'])
        age = st.number_input(t['age'], min_value=1, max_value=120, value=30)
        gender = st.selectbox(t['gender'], [t['male'],t['female'],t['other']])
        language = st.selectbox(t['select_language'], ['English','Telugu'])
        if st.form_submit_button(t['register']):
            if register_user(username,password,email,full_name,age,gender,language):
                st.success(t['register_success']); navigate_to('Login'); st.rerun()
            else: st.error("Username already exists")

def render_profile_update():
    if not st.session_state.logged_in: return st.warning("Please log in first")
    t = translations[st.session_state.language]
    user_data = st.session_state.users[st.session_state.username]
    with st.form("profile_form"):
        email = st.text_input(t['email'], value=user_data['email'])
        full_name = st.text_input(t['full_name'], value=user_data['full_name'])
        age = st.number_input(t['age'], min_value=1, max_value=120, value=user_data['age'])
        gender = st.selectbox(t['gender'], [t['male'],t['female'],t['other']])
        language = st.selectbox(t['select_language'], ['English','Telugu'])
        if st.form_submit_button(t['submit']):
            if update_profile(st.session_state.username,email,full_name,age,gender,language):
                st.success(t['profile_update_success']); st.rerun()

def render_chat():
    if not st.session_state.logged_in: return st.warning("Please log in to chat")
    t = translations[st.session_state.language]
    for message in st.session_state.chat_history:
        st.markdown(f"**{message['sender'].capitalize()}:** {message['text']}")
    user_input = st.chat_input(t['type_message'])
    if user_input:
        st.session_state.chat_history.append({'sender':'user','text':user_input})
        bot_reply = get_bot_reply(st.session_state.username, user_input)  # 🔹 DM integration  # 🔹 DM integration
        st.session_state.chat_history.append({'sender':'bot','text':bot_reply})
        st.rerun()

def render_admin():
    st.header("Registered Users 👥")
    if not st.session_state.users:
        st.info("No users registered yet.")
    else:
        for uname, udata in st.session_state.users.items():
            st.markdown(
                f"**{uname}** | {udata['full_name']} | {udata['email']} | Age: {udata['age']} | Gender: {udata['gender']} | Lang: {udata['language']}"
            )

# ---------------- MAIN ----------------
def main():
    render_navigation(); st.markdown("---")
    if st.session_state.page == 'Login': render_login()
    elif st.session_state.page == 'Register': render_register()
    elif st.session_state.page == 'Profile Update': render_profile_update()
    elif st.session_state.page == 'Chat': render_chat()
    elif st.session_state.page == 'Admin': render_admin()

    if st.session_state.logged_in:
        t = translations[st.session_state.language]
        if st.sidebar.button(t['logout']):
            st.session_state.logged_in=False; st.session_state.username=None
            st.session_state.chat_history=[]; navigate_to('Login'); st.rerun()

if __name__ == "__main__":
    main()
