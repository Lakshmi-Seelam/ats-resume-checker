import base64
import os
import io
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini
def get_gemini_response(input_prompt, pdf_content, job_description_text):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content([
        input_prompt,
        job_description_text,
        pdf_content[0]  # Passing image directly
    ])
    return response.text

# Convert uploaded PDF to first page image
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App UI
st.set_page_config(page_title="ATS Resume Expert", layout="centered")

st.markdown("<h1 style='text-align:center; color:#4B8BBE;'> ATS Tracking System</h1>", unsafe_allow_html=True)
st.markdown("Enter the Job Description Below")

# Job description input
input_text = st.text_area("Job Description:", key="input", height=200)

# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
if uploaded_file:
    st.success("PDF uploaded successfully")

# Button layout
col1, col2, col3 = st.columns(3)
with col1:
    submit1 = st.button("Tell me about the Resume")
with col2:
    submit2 = st.button("How Can I Improve my skills?")
with col3:
    submit3 = st.button("ATS Match Percentage")

# Prompts
input_prompt1 = """
You are an experienced HR with expertise in fields such as Data Science, Full Stack Development, Big Data Engineering, DevOps, and Data Analysis.
Please review the resume image and compare it with the job description.
Evaluate the candidate’s fit, strengths, and weaknesses.
"""

input_prompt2 = """
You are a Technical HR Manager with expertise in Data Science. Review the resume in light of the job description.
Provide feedback on the candidate's suitability and suggest how they can improve their skills to better match the job.
"""

input_prompt3 = """
You are an expert ATS (Applicant Tracking System) bot. Scan the resume image and compare it to the job description.
Return a percentage match and list any missing important keywords or skills.
"""

# Button logic
if submit1:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please upload the resume")

elif submit2:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please upload the resume")

elif submit3:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Percentage Match:")
        st.write(response)
    else:
        st.warning("Please upload the resume")



