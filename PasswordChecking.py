import streamlit as st

PASSWORD = st.secrets["PASSWORD"]

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.markdown("### Please enter the password to access the dashboard")
        st.markdown("*Contact John.Tracey@nhs.scot for the password*")
        password = st.text_input("Enter password", type="password")
        if password:
            if password == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
        return False
    return True

