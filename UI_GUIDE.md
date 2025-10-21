# Wan2.2 Web UI Guide

A user-friendly Gradio web interface for the Wan2.2 video generation models.

## Quick Start

### 1. Install Dependencies

```bash
# Install UI requirements (includes Gradio)
pip install -r requirements_ui.txt

# If flash_attn installation fails, install other packages first
pip install gradio torch torchvision torchaudio opencv-python diffusers transformers
# Then install flash_attn separately
pip install flash_attn
```

### 2. Download Model Checkpoints

You need to download at least one model checkpoint before using the UI:

```bash
# Install HuggingFace CLI
pip install "huggingface_hub[cli]"

# Download the model(s) you want to use:

# For Text-to-Video (requires ~80GB VRAM)
huggingface-cli download Wan-AI/Wan2.2-T2V-A14B --local-dir ./Wan2.2-T2V-A14B

# For Image-to-Video (requires ~80GB VRAM)
huggingface-cli download Wan-AI/Wan2.2-I2V-A14B --local-dir ./Wan2.2-I2V-A14B

# For Text-Image-to-Video (can run on RTX 4090 with 24GB VRAM) - RECOMMENDED FOR CONSUMER GPUs
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B --local-dir ./Wan2.2-TI2V-5B

# For Speech-to-Video (requires ~80GB VRAM)
huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir ./Wan2.2-S2V-14B
```

### 3. Launch the Web UI

```bash
python app.py
```

The web interface will open at `http://localhost:7860`

## Features

### Text-to-Video (T2V)
- Generate videos from text descriptions
- Supports 480P and 720P resolution
- GPU Requirements: ~80GB VRAM (A100, H100)

**Example:**
- Prompt: "Two anthropomorphic cats in comfy boxing gear and bright gloves fight intensely on a spotlighted stage."
- Size: 1280*720
- Frames: 81

### Image-to-Video (I2V)
- Animate images with text descriptions
- Maintains the composition of the input image
- GPU Requirements: ~80GB VRAM

**Example:**
- Upload an image of a cat
- Prompt: "The cat is playing with a ball of yarn"
- Size: 1280*720

### Text-Image-to-Video (TI2V) - Consumer GPU Friendly!
- Works on consumer GPUs like RTX 4090 (24GB VRAM)
- Supports both text-to-video and image-to-video
- Runs at 720P resolution with 24fps
- **Recommended for most users**

**Text-to-Video Mode:**
- Leave image field empty
- Prompt: "A butterfly flying through a garden"
- Size: 1280*704

**Image-to-Video Mode:**
- Upload an image
- Add a prompt describing the desired motion
- Size: 1280*704

### Speech-to-Video (S2V)
- Generate talking videos from audio files
- Requires a reference image and audio file
- GPU Requirements: ~80GB VRAM

**Example:**
- Upload a reference image (face/character)
- Upload an audio file (WAV, MP3)
- Optional prompt for scene description

## UI Parameters

### Common Parameters

- **Prompt**: Text description of the video you want to generate
- **Checkpoint Directory**: Path to the downloaded model weights
- **Video Size**: Resolution of the output video
- **Number of Frames**: Length of video (more frames = longer video)
- **Seed**: Random seed for reproducibility (-1 for random)
- **Sampling Steps**: Number of denoising steps (higher = better quality but slower)
- **Guidance Scale**: How closely to follow the prompt (7.5 is typical)
- **Use Prompt Extension**: Enhances prompts with AI (requires additional models)

## Tips for Best Results

1. **Start with TI2V-5B** if you have a consumer GPU (RTX 4090, etc.)
2. **Use descriptive prompts** with details about:
   - Camera movement
   - Lighting conditions
   - Scene composition
   - Subject actions
3. **Adjust frames** based on your needs:
   - 81 frames = ~3-4 seconds
   - 161 frames = ~6-7 seconds
4. **Experiment with guidance scale**:
   - Lower (5-7): More creative/varied
   - Higher (7.5-10): Stricter adherence to prompt

## Troubleshooting

### Out of Memory Errors
- Use the TI2V-5B model instead (only needs 24GB VRAM)
- Reduce the number of frames
- Use a smaller resolution

### Slow Generation
- This is normal! Video generation takes time
- T2V/I2V: Several minutes on high-end GPUs
- TI2V-5B: ~9 minutes for 5-second video on RTX 4090

### Model Not Found
- Make sure you've downloaded the checkpoint
- Check that the checkpoint directory path is correct
- Verify the model files are in the specified directory

## GPU Requirements Summary

| Model | VRAM Required | Best For |
|-------|---------------|----------|
| TI2V-5B | 24GB | Consumer GPUs, RTX 4090 |
| T2V-A14B | 80GB | High-end servers, A100/H100 |
| I2V-A14B | 80GB | High-end servers, A100/H100 |
| S2V-14B | 80GB | High-end servers, A100/H100 |

## Additional Resources

- [Wan2.2 GitHub Repository](https://github.com/Wan-Video/Wan2.2)
- [Official Documentation](https://wan.video)
- [Research Paper](https://arxiv.org/abs/2503.20314)
- [HuggingFace Models](https://huggingface.co/Wan-AI)

## Support

For issues and questions:
- GitHub Issues: https://github.com/Wan-Video/Wan2.2/issues
- Discord: https://discord.gg/AKNgpMK4Yj
