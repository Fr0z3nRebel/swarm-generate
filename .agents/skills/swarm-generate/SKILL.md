---
name: swarm-generate
description: Generate high-quality images using SwarmUI. Use when asked to generate, create, or design an image, banner, or illustration with specific prompts, aspect ratios, or upscaling.
---

# SwarmUI Image Generation

This skill allows you to generate images by interfacing with a SwarmUI backend.

## Usage

To generate an image, run the `generate_image.py` script. You must always provide a `--prompt`.

### Environment Configuration
Before running the script, verify that the following environment variables are set in the `.env` file or the shell. If they are missing or if the default URL (`http://192.168.1.197:7801`) is unreachable, **ask the user for the correct SwarmUI API details**.

- `SWARM_API_URL`: The base URL of the SwarmUI instance.
- `SWARM_API_MODEL`: The model path to use for generation.
- `SWARM_UPSCALE_METHOD`: The upscaling algorithm.

```bash
python3 generate_image.py --prompt "<description>" [options]
```

### Parameters

- `--prompt` (Required): A detailed text description of the image.
- `--output` (Optional): The directory to save images. (Default: `./output`)
- `--aspect` (Optional): The aspect ratio. Common values: `1:1`, `16:9`, `9:16`, `3:2`, `2:3`. (Default: `16:9`)
- `--upscale` (Optional): Upscale factor between `1.0` and `4.0`. (Default: `1.0`)
- `--model` (Optional): The model path in SwarmUI. (Default: `ZImage/SwarmUI_Z-Image-Turbo-FP8Mix`)
- `--upscale-method` (Optional): The upscaler to use. (Default: `model-RealESRGAN_x4plus.safetensors`)

## Examples

### Generate a cinematic widescreen image
```bash
python3 generate_image.py --prompt "A futuristic city skyline at night with neon lights and flying cars, high detail, 8k" --aspect 16:9
```

### Generate a high-res square portrait
```bash
python3 generate_image.py --prompt "Portrait of a majestic lion wearing cyberpunk armor, highly detailed" --aspect 1:1 --upscale 2.0
```

## Output Locations

Images are saved to the directory specified by the `--output` argument (defaults to `./output/` in the current working directory) with filenames like `gen_<timestamp>.png`.
