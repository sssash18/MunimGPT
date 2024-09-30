import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# Set the values of your computer vision endpoint and computer vision key
# as environment variables:
try:
    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    print("Set them before running this sample.")
    exit()

# Create an Image Analysis client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

def performOCR(image_url):
  # Get a caption for the image. This will be a synchronously (blocking) call.
  result = client.analyze_from_url(
      image_url=image_url,
      visual_features=[VisualFeatures.READ],
      gender_neutral_caption=True,  # Optional (default is False)
  )

  imageText = ""
  # Print text (OCR) analysis results to the console
  print(" Read:")
  if result.read is not None:
      for line in result.read.blocks[0].lines:
          imageText += f"Text: '{line.text}', Bounding box {line.bounding_polygon}\n"
         
  return imageText