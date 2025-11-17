import streamlit as st
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure_secrets import key, endpoint
from sup_utils import threshold_colors
import io
from io import BytesIO
from PIL import Image

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

def confidence_to_color(conf):
    
    sorted_thresholds = sorted(threshold_colors.keys())
    
    # find the highest threshold <= confidence
    for t in reversed(sorted_thresholds):
        if conf >= t:
            return threshold_colors[t]

def format_to_confidence(text_dict):
    text = ''
    for word_listdict in text_dict.words:
        color = confidence_to_color(word_listdict.confidence)
        suffix = ':%s-background['%color
        prefix = ']'
        text += suffix + word_listdict.text + prefix
    return text


def convert_to_bytes(uploaded_file):
    '''Convert uploaded file to bytes for Azure'''
    image = Image.open(uploaded_file)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    image_bytes = img_byte_arr.getvalue()
    
    return image_bytes

def azure_extract_text(io_image)->str: #markdown output
    res=''
    try:
        
        result = client.analyze(
            image_data=BytesIO(io_image),
            visual_features=[VisualFeatures.READ]
        )
        
        for block in result.read.blocks:
            for line in block.lines:
                formated_text = format_to_confidence(line)
                res += formated_text

    except Exception as e:
        res = f"An error occurred: {e}"
    
    return res

def main():

    st.title("Azure Computer Vision OCR")
    st.write("This app uses Azure Computer Vision to extract text from an uploaded image.")
    
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file)
        processed_img = convert_to_bytes(uploaded_file)
        
        output = azure_extract_text(processed_img)
        st.markdown(output)
    

    
if __name__ == "__main__":
    main()