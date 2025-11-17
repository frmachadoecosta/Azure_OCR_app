from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure_secrets import key, endpoint

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

img_path = "img/licence_plate.jpg"

with open(img_path, "rb") as f:
    result = client.analyze(
        image_data=f.read(),
        visual_features=[VisualFeatures.READ]
    )

# Extract recognized text
for block in result.read.blocks:
    print(block,'\n')
    for line in block.lines:
        print(line,'\n')
        print(line.text)
