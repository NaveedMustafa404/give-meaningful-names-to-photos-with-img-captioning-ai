import requests
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

# Here we load the pretrained processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load our image
img_path = "19568.jpg"
# convert it into an RGB format 
image = Image.open(img_path).convert('RGB')

# Prefix caption add
text = "the image of"
inputs = processor(images=image, text=text, return_tensors="pt")

# Caption generating 
#BLIP model runs a transformer decoder that predicts the caption word by word
outputs = model.generate(**inputs, max_length=50)

# Here decoding the generated tokens to readable text 
caption = processor.decode(outputs[0], skip_special_tokens=True)
# Print the caption
print(caption)