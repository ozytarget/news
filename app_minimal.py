import streamlit as st
from datetime import datetime

st.title("✅ News Scanner - LIVE")
st.write(f"Current time: {datetime.now().isoformat()}")
st.success("App is working!")
