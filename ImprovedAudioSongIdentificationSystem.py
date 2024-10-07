import speech_recognition as sr
import requests
from difflib import SequenceMatcher
import re

class ImprovedAudioSongIdentificationSystem:
    def __init__(self, genius_api_key):
        self.genius_api_key = genius_api_key
        self.base_url = "https://api.genius.com"
        self.headers = {"Authorization": f"Bearer {self.genius_api_key}"}
        self.recognizer = sr.Recognizer()

    def get_audio_input(self):
        with sr.Microphone() as source:
            print("Please sing or speak a part of the song lyrics...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
        return audio

    def transcribe_audio(self, audio):
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"Transcribed text: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service; {e}")
        return None

    def clean_text(self, text):
        cleaned = re.sub(r'[^\w\s]', '', text.lower())
        return ' '.join(cleaned.split())

    def search_song(self, lyrics):
        search_url = f"{self.base_url}/search"
        params = {"q": lyrics}
        response = requests.get(search_url, headers=self.headers, params=params)
        print(lyrics)
        matches = []
        if response.status_code == 200:
            data = response.json()
            hits = data["response"]["hits"]
            cleaned_input = self.clean_text(lyrics)
            
            for hit in hits:
                title = hit["result"]["title"]
                artist = hit["result"]["primary_artist"]["name"]
                full_title = f"{title} {artist}"
                cleaned_title = self.clean_text(full_title)
                
                if cleaned_input in cleaned_title:
                    matches.append((hit["result"], 1.0))
                else:
                    title_ratio = self.partial_ratio(cleaned_input, cleaned_title)
                    lyrics_ratio = self.check_lyrics(cleaned_input, hit["result"]["id"])
                    ratio = max(title_ratio, lyrics_ratio)
                    if ratio > 0.4:  # Lower threshold for audio input
                        matches.append((hit["result"], ratio))
            
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:3]

    def partial_ratio(self, a, b):
        shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
        matches = []
        for i in range(len(longer) - len(shorter) + 1):
            matches.append(SequenceMatcher(None, shorter, longer[i:i+len(shorter)]).ratio())
        return max(matches) if matches else 0

    def check_lyrics(self, input_text, song_id):
        lyrics_url = f"{self.base_url}/songs/{song_id}"
        response = requests.get(lyrics_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            lyrics = data["response"]["song"].get("lyrics", "")
            cleaned_lyrics = self.clean_text(lyrics)
            return self.partial_ratio(input_text, cleaned_lyrics)
        return 0

    def get_lyrics_url(self, song_id):
        song_url = f"{self.base_url}/songs/{song_id}"
        response = requests.get(song_url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            return data["response"]["song"]["url"]

        return None

    # def identify_song(self,audio):
    #     # audio = self.get_audio_input()
    #     transcribed_text = self.transcribe_audio(audio)
    #     if transcribed_text:
    #         matches = self.search_song(transcribed_text)
    #         if matches:
    #             print("\nTop 3 matching songs:")
    #             for i, (song, score) in enumerate(matches, 1):
    #                 print(f"{i}. {song['title']} by {song['primary_artist']['name']} (Match score: {score:.2f})")
    #                 lyrics_url = self.get_lyrics_url(song['id'])
    #                 if lyrics_url:
    #                     print(f"   Lyrics: {lyrics_url}")
    #                 print()
    #         else:
    #             print("Could not identify any matching songs. Try singing a different part of the song.")
    #     else:
    #         print("No lyrics were transcribed. Please try again.")


    def identify_song(self, audio):
    # audio = self.get_audio_input()
        transcribed_text = self.transcribe_audio(audio)
        result = ""

        if transcribed_text:
            print("got transcribe text")
            matches = self.search_song(transcribed_text)
            print(matches)
            if matches:
                result += "\nTop 3 matching songs:\n"
                for i, (song, score) in enumerate(matches, 1):
                    result += f"{i}. {song['title']} by {song['primary_artist']['name']} "
                    # (Match score: {score:.2f})\n"
                    lyrics_url = self.get_lyrics_url(song['id'])
                    # if lyrics_url:
                        # result += f"   Lyrics: {lyrics_url}\n"
                    result += "\n"
            else:
                result += "Could not identify any matching songs. Try singing a different part of the song.\n"
        else:
            result += "No lyrics were transcribed. Please try again.\n"
        
        return result

def get_song(audio):
    genius_api_key = "_DXvMUsp8CCaL50y9jfjnJN1gFxovl0RbQT7th5Yzfp-PdWXd4s9DvKpu7axIh1g"  # Replace with your actual Genius API key
    song_system = ImprovedAudioSongIdentificationSystem(genius_api_key)
    return song_system.identify_song(audio)