# Import necessary libraries
from dotenv import load_dotenv  # For loading environment variables from .env file

# Load environment variables from .env file
load_dotenv()

# Import required modules
import base64  # For encoding and decoding data
import streamlit as st  # For creating interactive web apps
import os  # For interacting with the operating system
import io  # For handling binary data
from PIL import Image  # For image processing
import pdf2image  # For converting PDF to image
import google.generativeai as genai  # For using Google's generative AI model

# Configure Google's generative AI model with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to set up input PDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        # Get the first page of the PDF
        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Encode image data to base64
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

# Set page configuration
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Text area for job description input
input_text = st.text_area("Job Description: ", key="input")

# File uploader for resume PDF
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

# Check if PDF is uploaded
if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Button to trigger response for evaluating resume
submit1 = st.button("Tell Me About the Resume")

# Button to trigger response for percentage match
submit3 = st.button("Percentage match")

# Prompt for evaluating resume against job description
input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

# Prompt for calculating percentage match
input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

# Handle submission for evaluating resume
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
