import re
import streamlit as st
import random
import string

def password_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🔒 Password length should be 8+ characters")
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("🔠 Missing uppercase letter")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("🔡 Missing lowercase letter")
    
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("🔢 Missing number")
    
    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("✨ Missing special character")
    
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium" 
    else:
        strength = "Strong"
    
    return strength, feedback, score

def generate_password(length):
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    st.set_page_config(
        page_title="Password Checker",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            background-color: #4CAF50;
            color: white;
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
        }
        .stSelectbox>div>div>select {
            border-radius: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Password Strength Meter")
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["Check Password", "Password History"])
        
        with tab1:
            st.markdown("### Enter or Generate Password")
            password = st.text_input("Password:", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                length = st.select_slider("Password Length", options=[8,12,16,20])
            with col2:
                if st.button("🎲 Generate"):
                    password = generate_password(length)
                    st.code(password)
                    if 'password_history' not in st.session_state:
                        st.session_state['password_history'] = []
                    st.session_state['password_history'].append(password)

            if st.button("🔍 Check Strength"):
                if password:
                    strength, feedback, score = password_strength(password)
                    
                    # Fancy progress bar
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.progress(score/5)
                    with col2:
                        if strength == "Weak":
                            st.error("Weak")
                        elif strength == "Medium":
                            st.warning("Medium") 
                        else:
                            st.success("Strong")
                            st.balloons()
                    
                    if feedback:
                        with st.expander("💡 Improvement Tips"):
                            for tip in feedback:
                                st.markdown(f"• {tip}")
                                
                    if 'password_history' not in st.session_state:
                        st.session_state['password_history'] = []
                    st.session_state['password_history'].append(password)
                else:
                    st.error("Please enter a password!")

        with tab2:
            if 'password_history' in st.session_state:
                st.markdown("### Recent Passwords")
                for pwd in reversed(st.session_state['password_history'][-5:]):
                    with st.container():
                        st.code(pwd)
                        strength, _, score = password_strength(pwd)
                        st.progress(score/5)
            else:
                st.info("No passwords checked yet!")
            
            if st.button("Clear History"):
                st.session_state['password_history'] = []
                st.experimental_rerun()

if __name__ == "__main__":
    main()