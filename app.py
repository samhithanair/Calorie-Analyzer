import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"]=st.secrets["GOOGLE_API_KEY"]
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt,image[0]])
    return response.text

def prepro_image(file):
    if file is not None:
        bytes_data = file.getvalue()

        image_parts = [
            {
                "mime_type":file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    
    else:
        raise FileNotFoundError("No file uploaded")

st.title("Nutrition Tracker!")

up_file = st.file_uploader("Choose an image!",type=["jpg","jpeg","png"])
image = ""
if up_file is not None:
    image = Image.open(up_file)
    st.image(image, caption="Uploaded Image",use_column_width=True)

submit = st.button("Calorie Analyze this meal")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----

               Show the total calories at the end in the following formate

               Total Calories - 
    
    Explain which foods are carbohydrates, proteins and fats on separate lines.

    Give 5 alternate dishes the user can eat with the same ingrediants that aren't the same as the image.

"""

if submit:
    image_data=prepro_image(up_file)
    response=gemini_response(input_prompt,image_data)
    st.subheader("Calorie Analyzer")
    st.write(response)
