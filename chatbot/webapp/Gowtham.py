import streamlit as st
import sqlite3
import bcrypt

# --- Database setup and helper functions ---
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            email TEXT,
            full_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def save_user(username, password, email, full_name):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        hashed_password = hash_password(password)
        c.execute('INSERT INTO users (username, password, email, full_name) VALUES (?, ?, ?, ?)',
                  (username, hashed_password, email, full_name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Username already exists
    finally:
        conn.close()

def get_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def update_user_profile(username, full_name, email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET full_name = ?, email = ? WHERE username = ?',
              (full_name, email, username))
    conn.commit()
    conn.close()

# --- Streamlit UI functions ---
def show_login_page():
    st.title("Streamlit Authentication App")
    st.subheader("Sign In")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.form_submit_button("Sign In"):
                user = get_user(username)
                if user and check_password(password, user[1]):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = user[0]
                    st.session_state['full_name'] = user[3]
                    st.session_state['email'] = user[2]
                    st.success(f"Welcome, {st.session_state['full_name']}!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password.")

def show_signup_page():
    st.title("Streamlit Authentication App")
    st.subheader("Create a New Account")
    with st.form("signup_form"):
        full_name = st.text_input("Full Name")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.form_submit_button("Sign Up"):
            if not all([full_name, username, email, password, confirm_password]):
                st.error("Please fill in all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif save_user(username, password, email, full_name):
                st.success("Account created successfully! Please sign in.")
                st.session_state['page'] = 'Sign In'
                st.experimental_rerun()
            else:
                st.error("Username already exists. Please choose another one.")

def show_profile_page():
    st.title("User Profile")
    st.subheader(f"Welcome, {st.session_state['full_name']}")
    
    with st.form("profile_form"):
        st.write("Update your profile information:")
        new_full_name = st.text_input("Full Name", value=st.session_state['full_name'])
        new_email = st.text_input("Email", value=st.session_state['email'])
        
        if st.form_submit_button("Save Changes"):
            update_user_profile(st.session_state['username'], new_full_name, new_email)
            st.session_state['full_name'] = new_full_name
            st.session_state['email'] = new_email
            st.success("Profile updated successfully!")

# --- Main App Logic ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'Sign In'

def main():
    init_db()

    st.sidebar.title("Menu")
    
    if st.session_state['logged_in']:
        page_options = ['Profile']
        selected_page = st.sidebar.radio("Navigation", page_options, index=0)
        
        if st.sidebar.button("Sign Out"):
            st.session_state['logged_in'] = False
            st.session_state['page'] = 'Sign In'
            st.experimental_rerun()
            
    else:
        page_options = ['Sign In', 'Sign Up']
        selected_page = st.sidebar.radio("Navigation", page_options, index=['Sign In', 'Sign Up'].index(st.session_state['page']))
        st.session_state['page'] = selected_page

    if st.session_state['logged_in']:
        show_profile_page()
    elif st.session_state['page'] == 'Sign Up':
        show_signup_page()
    else:
        show_login_page()

if __name__ == "__main__":
    main()