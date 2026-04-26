# SwarmUI Image Generator

A simple Python script to interface with the SwarmUI API and generate images from the command line.

## Prerequisites

1. **SwarmUI**: Ensure you have SwarmUI running.
2. **IP Address**: The script defaults to `http://192.168.1.197:7801`. If your SwarmUI is on a different IP or port, use the `--url` argument.
3. **Python**: Python 3.7+ installed.

## Setup

1. **Navigate to the project directory:**
   ```bash
   cd /Users/john/Development/my-repos/my-swarm-ui
   ```

2. **Setup environment variables:**
   Copy the example file and edit it with your settings:
   ```bash
   cp .env.example .env
   ```
   *Note: Edit `.env` to set your SwarmUI URL and default model.*

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic usage (uses defaults):
```bash
python generate_image.py
```

### Custom prompt:
```bash
python generate_image.py --prompt "A serene lake at sunrise, cinematic lighting, 8k"
```

### Custom SwarmUI URL:
```bash
python generate_image.py --url "http://localhost:7801" --prompt "Cyberpunk cat"
```

### Options:
- `--prompt`: The text description of the image (Default: Cyberpunk city).
- `--url`: The base URL of your SwarmUI instance (Default: http://192.168.1.197:7801).
- `--output` (Optional): The directory to save images. (Default: `./output`)
- `--model` (Optional): The model path in SwarmUI. (Default: `ZImage/SwarmUI_Z-Image-Turbo-FP8Mix`)
- `--aspect`: The aspect ratio to use (Default: 16:9).
- `--upscale`: The upscale factor (1-4, Default: 1).
- `--upscale-method`: The method used for upscaling (Default: `model-RealESRGAN_x4plus.safetensors`).

Generated images are automatically decoded from base64 (since `donotsave: True` is active) and saved to the directory specified by `--output` (defaults to `./output`).

The script performs two steps:
1. Calls `/API/GetNewSession` to obtain a session ID.
2. Calls `/API/GenerateText2Image` with relevant parameters (steps, cfg, aspect ratio, etc.) to trigger generation.
3. Prints the resulting image URL.
