import streamlit as st
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure_secrets import key, endpoint


client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)



def main():

    st.title("Azure Computer Vision OCR")
    st.write("This app uses Azure Computer Vision to extract text from an uploaded image.")

    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])


if __name__ == "__main__":
    main()