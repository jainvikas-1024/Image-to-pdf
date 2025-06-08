
import os
from fpdf import FPDF
from PIL import Image
from PyPDF2 import PdfMerger
import streamlit as st
import zipfile
import io

st.set_page_config(page_title="PDF Tools App", layout="centered")

# ---------- Function: Convert Images to PDF ----------
def images_to_pdf(image_files, output_path):
    pdf = FPDF()
    for image_file in image_files:
        image = Image.open(image_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save("temp.jpg")
        pdf.add_page()
        pdf.image("temp.jpg", x=0, y=0, w=210, h=297)  # A4
    pdf.output(output_path)
    os.remove("temp.jpg")

# ---------- Function: Merge PDFs ----------
def merge_pdfs(pdf_files, output_path):
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)
    merger.write(output_path)
    merger.close()

# ---------- Title ----------
st.title("🛠️ PDF Tools: Convert, Merge, Zip")

st.markdown("---")

# ---------- Section: Image to PDF ----------
st.subheader("🖼️ Convert Images to PDF")
image_files = st.file_uploader("Upload Images (JPEG, PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if st.button("📄 Convert to PDF") and image_files:
    output_path = "converted_images.pdf"
    images_to_pdf([img for img in image_files], output_path)
    with open(output_path, "rb") as f:
        st.download_button("⬇️ Download Converted PDF", f, file_name=output_path, mime="application/pdf")
    st.success("✅ Your image PDF is ready for download!")

st.markdown("---")

# ---------- Section: Merge PDFs ----------
st.subheader("📎 Merge Multiple PDFs")
pdf_files = st.file_uploader("Upload PDFs to Merge", type=["pdf"], accept_multiple_files=True)

if st.button("🔗 Merge PDFs") and pdf_files:
    merged_path = "merged_output.pdf"
    merge_pdfs([pdf for pdf in pdf_files], merged_path)
    with open(merged_path, "rb") as f:
        st.download_button("⬇️ Download Merged PDF", f, file_name=merged_path, mime="application/pdf")
    st.success("✅ Your merged PDF is ready for download!")

st.markdown("---")

# ---------- Section: Zip Files ----------
st.subheader("🗂️ Zip Multiple Files (Any Type)")
zip_files = st.file_uploader("Upload Files to Zip", type=None, accept_multiple_files=True)

if st.button("🧷 Create ZIP") and zip_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for uploaded_file in zip_files:
            zipf.writestr(uploaded_file.name, uploaded_file.read())

    zip_buffer.seek(0)
    st.download_button("⬇️ Download ZIP", zip_buffer, file_name="files.zip", mime="application/zip")
    st.success("✅ Your ZIP file is ready for download!")

st.markdown("---")
st.caption("Developed by Vikas Jain 💡 | Powered by Streamlit")
