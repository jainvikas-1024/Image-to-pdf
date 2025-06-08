
import os
from fpdf import FPDF
from PIL import Image
from PyPDF2 import PdfMerger
import streamlit as st

# Function to convert images to PDF
def images_to_pdf(image_files, output_path):
    pdf = FPDF()
    for image_file in image_files:
        image = Image.open(image_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save("temp.jpg")
        pdf.add_page()
        pdf.image("temp.jpg", x=0, y=0, w=210, h=297)  # A4 size
    pdf.output(output_path)
    os.remove("temp.jpg")


# Function to merge multiple PDFs into one
def merge_pdfs(pdf_files, output_path):
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)
    merger.write(output_path)
    merger.close()

# Streamlit Interface
st.title("Image to PDF Converter & PDF Merger")

st.header("Convert Images to PDF")
image_files = st.file_uploader("Upload Images (JPEG, PNG, etc.)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
if st.button("Convert to PDF") and image_files:
    output_path = "converted_images.pdf"
    images_to_pdf([img for img in image_files], output_path)
    with open(output_path, "rb") as f:
        st.download_button("Download Converted PDF", f, file_name=output_path)

st.header("Merge Multiple PDFs")
pdf_files = st.file_uploader("Upload PDFs to Merge", type=["pdf"], accept_multiple_files=True)
if st.button("Merge PDFs") and pdf_files:
    merged_path = "merged_output.pdf"
    merge_pdfs([pdf for pdf in pdf_files], merged_path)
    with open(merged_path, "rb") as f:
        st.download_button("Download Merged PDF", f, file_name=merged_path)
