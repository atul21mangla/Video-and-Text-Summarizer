import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re

# Load environment variables
load_dotenv()

# Configure the Google Generative AI API key
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# Define the prompt
prompt = """You are a YouTube summarizer. You will be taking transcript text and 
summarizing the entire video and providing the important summary in points within 250 words.
Please provide the summary of the text given: """

# Function to extract video ID from YouTube URL
def extract_video_id(youtube_video_url):
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/.*v=([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)'
    ]
    for pattern in patterns:
        match = re.match(pattern, youtube_video_url)
        if match:
            return match.group(1)
    return None

# Function to get available transcript languages
def get_available_languages(video_id):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        return {t.language_code: t.language for t in transcripts}
    except Exception as e:
        st.error("Error retrieving available languages: " + str(e))
        return None

# Function to extract transcript details from YouTube video
def extract_transcript_details(youtube_video_url, language_code='en'):
    try:
        video_id = extract_video_id(youtube_video_url)
        if not video_id:
            st.error("Invalid YouTube URL.")
            return None

        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        
        transcript_text = " ".join([item["text"] for item in transcript_data])
        return transcript_text
    except NoTranscriptFound:
        st.error(f"Could not retrieve a transcript for the video {youtube_video_url}. No transcripts were found for the requested language code: {language_code}.")
        return None
    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video.")
        return None
    except Exception as e:
        st.error("Error extracting transcript: " + str(e))
        return None

# Function to generate summary using Google Generative AI
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error("Error generating summary: " + str(e))
        return None
st.image('logodone.png',use_column_width=True)
# Streamlit app layout
st.title("Video Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter video link:")

if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        
        available_languages = get_available_languages(video_id)
        if available_languages:
            language_code = st.selectbox("Select Transcript Language", list(available_languages.keys()), format_func=lambda x: available_languages[x])
        else:
            st.error("No available transcripts found for this video.")
    else:
        st.error("Invalid YouTube URL.")
else:
    language_code = 'en'

if st.button("Get detailed notes"):
    transcript_text = extract_transcript_details(youtube_link, language_code)
    
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        if summary:
            st.markdown("# Detailed Notes:")
            st.write(summary)
