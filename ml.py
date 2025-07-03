from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline
from PIL.Image import Image
from IPython.display import display

token_path = Path("token.txt")
token = token_path.read_text().strip()

# get your token at https://huggingface.co/settings/tokens
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    token=token,
    torch_dtype=torch.float32,   #if GPU is available, change to "fp16"
    low_cpu_mem_usage=True)

pipe.to("cpu")   #if GPU is available, change to "cuda"

prompt = "a panda playing football"

#image = pipe(prompt, num_inference_steps=50).images[0]


def obtain_image(
    prompt: str,
    *,
    seed: int | None = None,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
) -> Image:
    # pick the right device automatically
    device = pipe.device.type           # "cpu", "cuda" if GPU is avalable
    generator = None if seed is None else torch.Generator(device).manual_seed(seed)

    print(f"Using device: {device}")
    image: Image = pipe(
        prompt,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        generator=generator,
    ).images[0]
    return image


image = obtain_image(prompt, num_inference_steps=5, seed=1024)
display(image)