<!DOCTYPE html>
<html lang="en">


<h1>🎵 Audio-Based Song Identification System 🎤</h1>


<p><strong>Identify songs by simply singing or speaking the lyrics!</strong></p>

<p>This system allows users to input a segment of song lyrics through audio, transcribes it using Google's Speech Recognition API, and finds the closest matching songs using the Genius API. The system ranks the top 3 matching songs based on the similarity of lyrics and metadata.</p>

<h2>🚀 Features</h2>
<ul>
    <li><strong>Real-time Speech Recognition</strong>: Sing or speak a part of the song and get real-time transcription.</li>
    <li><strong>Top 3 Song Matches</strong>: Accurately identify the top 3 songs based on user input.</li>
    <li><strong>Genius API Integration</strong>: Fetch song lyrics and metadata to enhance the song search.</li>
    <li><strong>Partial Match Handling</strong>: Smart matching algorithm that compares input against song titles and lyrics even with partial or noisy inputs.</li>
</ul>

<h2>🛠️ Technologies Used</h2>
<ul>
    <li><strong>Python 3.7+</strong>: Core language.</li>
    <li><strong>SpeechRecognition</strong>: For converting spoken lyrics to text.</li>
    <li><strong>Genius API</strong>: To search for songs and retrieve lyrics.</li>
    <li><strong>Streamlit</strong>: For building the web interface.</li>
    <li><strong>Google Speech API</strong>: For handling audio transcription.</li>
</ul>

<h2>🎯 How It Works</h2>
<ol>
    <li><strong>Audio Input:</strong> The system prompts the user to sing or speak a segment of song lyrics using their microphone.</li>
    <li><strong>Speech to Text:</strong> The audio is transcribed using Google's Speech Recognition engine.</li>
    <li><strong>Lyrics Matching:</strong> The system sends the transcribed lyrics to the Genius API, searching for potential song matches.</li>
    <li><strong>Top 3 Matches:</strong> The results are processed and the top 3 closest matches (with similarity scores) are displayed along with links to the song lyrics.</li>
</ol>

</body>
</html>
