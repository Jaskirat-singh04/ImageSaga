from dotenv import load_dotenv, find_dotenv
from transformers import pipeline
from langchain import PromptTemplate, OpenAI, LLMChain
from bardapi import Bard
import streamlit as st
import requests

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN= ""

# Img2text
def img2text(url):
 image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
 text = image_to_text(url) [0] ["generated_text"]
#  print(text)
 return text
# img2text("photo.png")


#generate text
def call_bard(scenerio):
   bard = Bard()
   template=""" You are a story teller; You can generate a short story based on a simple narrative, the story should be no more than 40 words  do not start with sure here is the story just start it and end it without asking for a feedback;"""
   answer = bard.get_answer(template+scenerio)
   return (answer['content'])





# text to speech
def text2speech (message):
 API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits" 
 headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
 payloads={
 "inputs": message
 }
 response = requests.post(API_URL, headers=headers, json=payloads)
 with open('audio.flac', 'wb') as file:
  file.write(response.content)

# scenario= img2text("photo.png")
# story=call_bard(scenario)
# text2speech(story)


def main():
 
 st.set_page_config(page_title="img 2 audio story", page_icon="🤖")
#  st.header("Turn img into audio story")

#   # Add background image using st.markdown()
#  bg_image = "photo-back.jpg"
#  bg_css = f"""
#         <style>
#         .stApp {{
#             background-image: url("{bg_image}");
#             background-size: cover;
#         }}
#         </style>
#     """
#  st.markdown(bg_css, unsafe_allow_html=True)
 st.title("Turn Image into Audio Story 📖🎧 ")

 uploaded_file = st.file_uploader("Choose an image...", type="jpg")

 if uploaded_file is not None:
  print(uploaded_file)
  bytes_data = uploaded_file.getvalue()
  with open(uploaded_file.name, "wb") as file: 
    file.write(bytes_data)
  st.image(uploaded_file, caption='Uploaded Image.',
           use_column_width=True)
  scenario=img2text (uploaded_file.name)
  story=call_bard(scenario)
  text2speech(story)

  with st.expander("scenario"):
   st.write(scenario)
  with st.expander("story"): 
   st.write(story)

  st.audio("audio.flac")
  
if __name__== '__main__':
 main()