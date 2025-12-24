from dotenv import load_dotenv
load_dotenv()
import streamlit as st 
import os 
from PIL import Image
import pdf2image 
import google.generativeai as genai
import io
import base64


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input,pdf_content,prompt):
#     model=genai.GenerativeModel('gemini-2.5-pro')
#     response=model.generate_content(input,pdf_content[0],prompt)
#     return response.text

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content(
        [
            {"role": "user", "parts": [
                {"text": prompt},
                {"text": input_text},
                pdf_content[0]  # this contains the resume image
            ]}
        ]
    )
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF TO IMAGE 
        os.environ["PATH"] += os.pathsep + r"C:\poppler-24.08.0\Library\bin"
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]
        
        ## Convert to bytes 
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts=[
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode() #encode to base64 
            }
        ]
        
        return pdf_parts
    else:
        raise FileNotFoundError("No File uploded")


## streamlit App 
st.set_page_config(page_title="Ats Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploded_file=st.file_uploader("Upload your resume(PDF)....",type=["pdf"])

if uploded_file is not None:
    st.write("PDF Uploded Successfully")

submit1=st.button("Tell Me About the Resume")
#submit2=st.button("How Can I Improvise my Skills")
#submit3=st.button("What are the Keywords That are Missing")
submit3=st.button("Percentage match")

input_prompt1="""
You are an experienced HR With  Experience in the filed of Data Science , Full stack Web devlopment , Big data Engineering , Devops,Data Analyst
your task is to review the provided resume against the job description for this profiles .
Please Share your professional evaluation on whether the candidate 's profile aligns with every role
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2="""
You are an Technical Human Resource Manager with expertise in Data Science , Full stack Web devlopment , Big data Engineering , Devops,Data Analyst,
your role is to scrutinize the resume in light of the job description provided .
share your insights on the candidate 's suitability for the role from an HR perspective ,
Additionally , offer advice on enhancing the candidate's skills and identify areas 
"""


input_prompt3="""
You are an skilled ATS (Applicant Tracking System) Scanner with a deep understanding  of Data Science , Full stack Web devlopment , Big data Engineering , 
Devops,Data Analyst, and ATS functionality ,
your task is to evaluate the resume against the provided job description . give me the percentage of match if the resume matches 
the job description . First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploded_file is not None:
        pdf_content=input_pdf_setup(uploded_file)
        response=get_gemini_response(input_text,pdf_content,input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploded_file is not None:
        pdf_content=input_pdf_setup(uploded_file)
        response=get_gemini_response(input_text,pdf_content,input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")





