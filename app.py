import streamlit as st

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("AI Interview Preparation Assistant")

st.write("Welcome to your AI-powered interview coach!")

st.markdown("---")

st.subheader("Features")

st.write("📋 Generate interview questions")

st.write("📝 AI answer evaluation")

st.write("🎙️ Voice mock interview")

st.write("📊 Performance report")

st.markdown("---")

if st.button("🚀Start Interview"):
    st.success("Project setup completed successfully!")