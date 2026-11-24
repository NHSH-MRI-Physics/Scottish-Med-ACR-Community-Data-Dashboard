import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
from scipy import stats
import pandas as pd
import pickle
st.title("Scottish Medium ACR Community Data Dashboard")

from PasswordChecking import check_password
if not check_password():
    st.stop()

st.markdown("""
This page allows authorised users to upload new ACR data to the database. Please ensure data is correct and from a functioning system prior to uploading.

This page is currently under construction
""")

st.stop()

uploaded_file = st.file_uploader("Choose a file",type=["docx"])

if uploaded_file is not None:
    print("Hello")
    data = pickle.load(uploaded_file)
    st.write(data)
    #Check against the standard 