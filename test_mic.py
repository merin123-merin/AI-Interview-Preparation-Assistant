import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="Microphone Test",
    page_icon="🎤"
)

st.title("🎤 Microphone Test")

st.write("Click the microphone button and record a short sentence.")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=False,
    use_container_width=False
)

if audio:
    st.success("✅ Recording received!")

    st.audio(
        audio["bytes"],
        format="audio/wav"
    )