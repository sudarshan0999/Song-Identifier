import streamlit as st
import speech_recognition as sr
from ImprovedAudioSongIdentificationSystem import get_song

# Set the page configuration for better appearance
st.set_page_config(page_title="Live Audio Song Recognition", page_icon="🎵", layout="centered")

# Custom CSS for background image and button styling
st.markdown("""
    <style>
    /* Full-page background image */
    body {
        background-image: url("https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?crop=entropy&fit=crop&w=1200&h=800");
        background-size: cover;
    }

    /* Center the app content */
    .stApp {
        background-color: rgba(0, 0, 0, 0.5);  /* Semi-transparent background for contrast */
        border-radius: 15px;
        padding: 30px;
    }

    /* Button styling */
    button[aria-label="Start Recording"] {
        background-color: #ff0000;
        color: red;
        font-size: 24px;
        padding: 12px 30px;
        border-radius: 10px;
    }

    button[aria-label="Submit"] {
        background-color: #28a745;
        color: white;
        font-size: 24px;
        padding: 12px 30px;
        border-radius: 10px;
    }

    /* Adjust fonts */
    h1, h2, h3 {
        color: white;
    }

    h1 {
        font-size: 50px;
    }

    p {
        font-size: 18px;
        color: white;
    }

    /* Footer styling */
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables for recording
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'recognizer' not in st.session_state:
    st.session_state.recognizer = sr.Recognizer()

# Function to capture audio input using speech_recognition
def get_audio_input():
    recognizer = st.session_state.recognizer
    with sr.Microphone() as source:
        st.write("🎤 Please sing or speak a part of the song lyrics...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
    return audio

# Streamlit UI setup
st.markdown("<h1 style='text-align: center;'>Live Audio Song Recognition</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>🎶 Discover Your Favorite Songs with Your Voice 🎶</h3>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center;'>Press <strong>Start Recording</strong> to sing or hum a song, then press <strong>Submit</strong> to get the best match.</p>", unsafe_allow_html=True)

# Add decorative containers for better layout
with st.container():
    st.write("---")  # Adds a horizontal line for separation

    # Centered buttons for Start Recording and Submit
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h3 style='text-align: center;'>Ready to Sing?</h3>", unsafe_allow_html=True)

        if st.button("🎙️ Start Recording"):
            if not st.session_state.is_recording:
                st.session_state.is_recording = True
                try:
                    with st.spinner('Recording... 🎤'):
                        st.session_state.audio_data = get_audio_input()  # Capture audio input
                    st.success("Recording complete! 🎉")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error while recording: {e}")

    st.write("---")

    with col2:
        st.markdown("<h3 style='text-align: center;'>Finished Singing?</h3>", unsafe_allow_html=True)

        if st.button("🚀 Submit"):
            if st.session_state.is_recording:
                st.session_state.is_recording = False
                if st.session_state.audio_data:
                    st.write("🎧 **Top 3 Matching Songs:**")
                    with st.spinner('Identifying songs...'):
                        matching_songs = get_song(st.session_state.audio_data)
                    st.success("Song identification complete!")
                    st.write(matching_songs)  # Display the songs in a nice format
                else:
                    st.warning("No audio data to process.")
                    
            else:
                st.warning("You must start recording before submitting audio!")

# Information if recording hasn't been started
if not st.session_state.is_recording and st.session_state.audio_data is None:
    st.info("🎶 **No audio recorded yet**. Press the **Start Recording** button above to begin.")

st.write("---")  # Another separator

# # Footer
# st.markdown(
#     """
#     <div style="text-align:center; color:lightgray; font-size:small;">
   
#     </div>
#     """, 
#     unsafe_allow_html=True
# )

