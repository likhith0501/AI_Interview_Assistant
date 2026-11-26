import streamlit as st
from groq import Groq
st.set_page_config(page_title='AI Interview Assistant', layout='centered')
st.title(' AI Interview Assistant')
st.caption('Practice interviews with AI-generated questions and constructive feedback.')
st.caption(' lanchued by LIKHITH HP')
st.write("Deparement of AI&DS")
try:
    client = Groq(api_key=st.secrets['GROQ_API_KEY'])
    st.write("API connection successful")
except (KeyError, FileNotFoundError):
    st.error('GROQ_API_KEY is missing. Add it to Streamlit Cloud → App settings → Secrets.')
    st.stop()
    role = st.selectbox('Job role', ['Python Developer', 'Data Analyst', 'Java Developer', 'Machine Learning Engineer', 'Software Engineer', 'HR Executive'])


    
