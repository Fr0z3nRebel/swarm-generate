import requests
import json
import argparse
import sys
import os
import base64
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configuration Defaults (Loaded from .env if present)
DEFAULT_BASE_URL = os.getenv("SWARM_API_URL", "http://192.168.1.197:7801")
DEFAULT_MODEL = os.getenv("SWARM_API_MODEL", "ZImage/SwarmUI_Z-Image-Turbo-FP8Mix")
DEFAULT_UPSCALE_METHOD = os.getenv("SWARM_UPSCALE_METHOD", "model-RealESRGAN_x4plus.safetensors")
DEFAULT_PROMPT = "A futuristic cyberpunk city at sunset, highly detailed, 8k"

def generate_image(prompt, base_url, model, aspect, upscale, upscale_method, output_dir):
    """
    Triggers an image generation on a SwarmUI instance.
    """
    print(f"Connecting to SwarmUI at {base_url}...")
    
    # 1. Get a Session ID
    try:
        session_resp = requests.post(f"{base_url}/API/GetNewSession", json={})
        session_resp.raise_for_status()
        session_id = session_resp.json().get("session_id")
    except Exception as e:
        print(f"Error connecting to SwarmUI: {e}")
        return

    if not session_id:
        print("Failed to get session ID from SwarmUI.")
        return

    # 2. Define parameters
    payload = {
        "session_id": session_id,
        "prompt": prompt,
        "model": model,
        "images": 1,
        "seed": -1,
        "steps": 12,
        "cfgscale": 1,
        "aspectratio": aspect,
        "sidelength": 1024,
        "sampler": "Euler",
        "scheduler": "Normal",
        "donotsave": True,
        "refinerUpscale": upscale,
        "refinerUpscaleMethod": upscale_method,
        "refinerModel": model,
        "refinerControlPercentage": 0.2,
        "refinerMethod": "PostApply"
    }

    # 3. Trigger the generation
    print(f"Generating image with prompt: '{prompt}'...")
    try:
        gen_resp = requests.post(f"{base_url}/API/GenerateText2Image", json=payload)
        gen_resp.raise_for_status()
        gen_data = gen_resp.json()
    except Exception as e:
        print(f"Error during generation request: {e}")
        return

    if "error" in gen_data:
        print(f"SwarmUI Error: {gen_data['error']}")
    else:
        # The API returns a list of image paths (e.g., /View/local/raw/...)
        image_urls = gen_data.get("images", [])
        if not image_urls:
            print("No images returned in response.")
            return
            
        # 4. Download images locally
        os.makedirs(output_dir, exist_ok=True)

        for img_url in image_urls:
            try:
                # Case 1: Base64 data (used when donotsave is True)
                if img_url.startswith('data:image'):
                    header, encoded = img_url.split(",", 1)
                    file_ext = header.split("/")[1].split(";")[0] # e.g. png
                    img_data = base64.b64decode(encoded)
                    
                    # Generate a filename since none is provided in base64
                    import time
                    filename = f"gen_{int(time.time())}.{file_ext}"
                    save_path = os.path.join(output_dir, filename)
                    
                    print(f"Decoding base64 image to {save_path}...")
                    with open(save_path, 'wb') as f:
                        f.write(img_data)
                    print(f"Saved: {filename}")
                
                # Case 2: Standard URL
                else:
                    if not img_url.startswith('/'):
                        img_url = '/' + img_url
                    full_url = f"{base_url.rstrip('/')}{img_url}"
                    print(f"Success! Image available at: {full_url}")
                    
                    filename = img_url.split('/')[-1]
                    save_path = os.path.join(output_dir, filename)
                    print(f"Downloading to {save_path}...")
                    img_data = requests.get(full_url).content
                    with open(save_path, 'wb') as f:
                        f.write(img_data)
                    print(f"Saved: {filename}")
            except Exception as e:
                print(f"Failed to download image: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate images via SwarmUI API")
    parser.add_argument("--prompt", type=str, default=DEFAULT_PROMPT, help="The prompt for image generation")
    parser.add_argument("--url", type=str, default=DEFAULT_BASE_URL, help="The SwarmUI Base URL")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="The model to use")
    parser.add_argument("--aspect", type=str, default="16:9", help="The aspect ratio (e.g. 1:1, 16:9, etc.)")
    parser.add_argument("--upscale", type=float, default=1.0, help="The upscale factor (1-4, Default: 1)")
    parser.add_argument("--upscale-method", type=str, default=DEFAULT_UPSCALE_METHOD, help=f"Upscale method (Default: {DEFAULT_UPSCALE_METHOD})")
    parser.add_argument("--output", type=str, default="output", help="The output directory to save images (Default: ./output)")
    
    args = parser.parse_args()
    
    generate_image(args.prompt, args.url, args.model, args.aspect, args.upscale, args.upscale_method, args.output)

if __name__ == "__main__":
    main()
