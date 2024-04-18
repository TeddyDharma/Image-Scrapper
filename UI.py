import streamlit as st
import time
from main import download_image

if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button

st.title('Welcome to Image Scrapper')
st.subheader('Automatic Image Downloader to make your life easier:sunglasses:')

image_name = st.text_input("Image Name","rendang")
width = st.number_input("Image Width", 180)
height = st.number_input("Image Height", 180)

st.button('Start', on_click=click_button, type="primary")
if st.session_state.button: 
    st.text("Start scrapping..........")
    download_image(image_name, width, height)
    st.success("Success to college the image")
