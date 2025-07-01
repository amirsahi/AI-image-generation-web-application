from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline
from PIL.Image import Image

token_path = Path("token.txt")
token = token_path.read_text().strip()

# get your token at https://huggingface.co/settings/tokens
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    token=token,
    torch_dtype=torch.float32,   #if GPU is available, change to "fp16"
    low_cpu_mem_usage=True)

pipe.to("cpu")   #if GPU is available, change to "cuda"

prompt = "a photograph of an astronaut riding a horse"

image = pipe(prompt, num_inference_steps=50).images[0]

image.save("astronaut_horse.png")      
print("done → astronaut_horse.png")