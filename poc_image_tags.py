import streamlit as st
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from secrets import key, endpoint

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

img_path = 'img/licence_plate.jpg'

with open(img_path, "rb") as image_file:
    image_analysis = computervision_client.analyze_image_in_stream(
        image_file,
        visual_features=[VisualFeatureTypes.tags]
    )

for tag in image_analysis.tags:
    print(tag)