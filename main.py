import streamlit as st
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure_secrets import key, endpoint
import io
from io import BytesIO
from PIL import Image

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

def azure_extract_text(io_image)->str: #markdown output
    res=''
    try:
        
        result = client.analyze(
            image_data=BytesIO(io_image),
            visual_features=[VisualFeatures.READ]
        )
        
        for block in result.read.blocks:
            for line in block.lines:
                print('line:', line)
                res += line.text+'\n'

    except Exception as e:
        res = f"An error occurred: {e}"
    
    return res

def main():

    st.title("Azure Computer Vision OCR")
    st.write("This app uses Azure Computer Vision to extract text from an uploaded image.")
    
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file)

        image = Image.open(uploaded_file)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        image_bytes = img_byte_arr.getvalue()
        
        output = azure_extract_text(image_bytes)
        st.write(output)
    

    
if __name__ == "__main__":
    main()