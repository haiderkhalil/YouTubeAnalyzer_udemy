# app.py
import os
import streamlit as st
import textwrap
import requests
from io import BytesIO
from PIL import Image
from pytube import YouTube
import create_vector_db as mydb
from dotenv import load_dotenv



load_dotenv()
openai_api_key=""
video_url=""
video_id=""
st.set_page_config(layout="wide")

# st.header("YouTube Video Analyzer")
st.write("Provide YouTube URL, I will analyze it and give you a brief summary of the contents.")
openai_api_key=os.environ["OPENAI_API_KEY"]
 # Create the main content area
col1, col2 = st.columns([1,1])

def analyze_video():
    os.environ["OPENAI_API_KEY"] = openai_api_key

    with col1:
        # Extract the YouTube video ID from the URL
        video_id = YouTube(video_url).video_id
        # Construct the URL of the thumbnail image
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

        # Download the thumbnail image and convert it to a PIL Image object
        response = requests.get(thumbnail_url)
        img = Image.open(BytesIO(response.content))

        # Display the thumbnail image in Streamlit
        st.image(img)

    # Column 2
    with col2:
        with st.spinner("Analyzing Video contents..."):
            response = mydb.create_db_and_analye(video_url)
            try:
                st.subheader("Video Summary")
                st.write(textwrap.fill(response, width=50))
            except:
                st.write("Something went wrong!")
            st.markdown(f"Developed By [Haider Ali]({'https://www.linkedin.com/in/haiderkhalil/'})")
            hit_counter()
    
def hit_counter():
    with open("hit_count.txt", "r") as file:
        hit_count = int(file.read())

        # Increment the hit count
        hit_count += 1

        # Update the hit count in the file
        with open("hit_count.txt", "w") as file:
            file.write(str(hit_count))

        # Display the hit count
        st.write(f"Page Hits: {hit_count}")

# Column 1 
with col1:
    c1, c2, c3 = st.columns([3,1,1])
    with c1:
        openai_api_key = st.text_input("OpenAI API Key", value=os.environ["OPENAI_API_KEY"])
    with c2:
        st.markdown(f"[Get API Key]({'https://platform.openai.com/account/api-keys'})")
    with c3:
        st.markdown(f"[How to Get?]({'https://www.youtube.com/watch?v=iRVsV9RVaMQ&t=22s'})")
    video_url = st.text_input("YouTube Video URL", value=video_url)
    button_disabled = len(video_url.strip()) == 0
    submit_button = st.button("Submit", on_click=analyze_video, disabled=button_disabled)
