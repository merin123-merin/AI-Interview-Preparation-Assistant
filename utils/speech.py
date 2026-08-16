import whisper
import tempfile
import os


# Load Whisper model once
print("Loading Whisper model...")

model = whisper.load_model("base")

print("Whisper loaded successfully!")


def transcribe_audio(audio_file):
    """
    Convert Streamlit UploadedFile audio into text using Whisper.
    """

    # Read the uploaded audio as bytes
    audio_bytes = audio_file.getvalue()

    # Save audio temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp_audio:

        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

    try:

        # Transcribe the temporary audio file
        result = model.transcribe(
            temp_audio_path
        )

        return result["text"].strip()

    finally:

        # Delete temporary file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
