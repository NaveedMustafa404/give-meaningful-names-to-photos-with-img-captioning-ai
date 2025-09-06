import requests
import threading
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration, TextStreamer, TextIteratorStreamer

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

# Using TextStreamer to create a streamer that prints tokens as they are generated
streamer = TextStreamer(processor.tokenizer, skip_special_tokens=True)

# Caption generating 
# BLIP model runs a transformer decoder that predicts the caption word by word
outputs = model.generate(**inputs, max_length=50, streamer=streamer)

token_ids = outputs[0]

print("Streaming caption:")
words = []
for i in range(len(token_ids)):
    chunk = processor.decode(token_ids[:i+1], skip_special_tokens=True)
    if chunk and (not words or chunk != " ".join(words)):  
        words = chunk.split()
        print(" ".join(words))

# Here decoding the generated tokens to readable text 
caption = processor.decode(outputs[0], skip_special_tokens=True)
# Print the caption
print("\nFinal Caption:", caption)

