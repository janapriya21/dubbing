import streamlit as st
from pytube import YouTube
import time
import requests
from pytube.exceptions import PytubeError
import yt_dlp

# Get YouTube video link from Streamlit input
link = st.text_input("Link to Youtube Video", key="link")

# Function to attempt fetching title using pytube
def get_title_with_pytube(link):
    try:
        yt = YouTube(link)
        return yt.title, yt.thumbnail_url
    except PytubeError as e:
        st.error(f"PytubeError: {e}")
        print(f"PytubeError: {e}")
        return None, None
    except Exception as e:
        st.error(f"An error occurred while fetching the title: {e}")
        print(f"Error: {e}")
        return None, None

# Function to attempt fetching title using yt-dlp as a fallback
def get_title_with_yt_dlp(link):
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,  # Only extract metadata
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            title = info_dict.get('title', 'No title available')
            thumbnail_url = info_dict.get('thumbnail', '')
            return title, thumbnail_url
    except Exception as e:
        st.error(f"Error fetching title using yt-dlp: {e}")
        print(f"Error with yt-dlp: {e}")
        return None, None

# Handle the case when the user clicks the button
if st.button("Transcribe!"):
    st.write(f"Downloading video from link: {link}")

    # First, attempt to fetch the title using pytube
    title, thumbnail_url = get_title_with_pytube(link)

    # If Pytube fails, fall back to yt-dlp
    if title is None:
        st.write("Falling back to yt-dlp to fetch video metadata...")
        title, thumbnail_url = get_title_with_yt_dlp(link)

    if title:
        st.subheader(f"Video Title: {title}")  # Display the title of the video
        if thumbnail_url:
            st.image(thumbnail_url)  # Display the thumbnail
    else:
        st.error("Failed to fetch video title using both Pytube and yt-dlp.")
        
    # Retry logic (optional)
    if title is None:
        st.write("Retrying to fetch the video title...")
        time.sleep(5)  # Wait for 5 seconds before retrying

        # Retry fetching using Pytube or yt-dlp
        title, thumbnail_url = get_title_with_pytube(link)
        if title is None:
            st.write("Retrying using yt-dlp...")
            title, thumbnail_url = get_title_with_yt_dlp(link)
        
        if title:
            st.subheader(f"Video Title (Retry): {title}")
            if thumbnail_url:
                st.image(thumbnail_url)
