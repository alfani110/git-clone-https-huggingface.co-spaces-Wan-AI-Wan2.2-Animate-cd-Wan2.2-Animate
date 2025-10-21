# Wan2.2 Web UI

<p align="center">
    <img src="assets/logo.png" width="200"/>
</p>

A user-friendly **Gradio web interface** for the Wan2.2 video generation models. Generate high-quality AI videos through an intuitive browser-based interface!

## Features

- **Text-to-Video**: Generate videos from text descriptions
- **Image-to-Video**: Animate images with motion
- **Text-Image-to-Video**: Flexible model that runs on consumer GPUs (RTX 4090)
- **Speech-to-Video**: Create talking videos from audio
- **Easy to Use**: No command-line expertise required
- **Real-time Logs**: Monitor generation progress
- **Multiple Resolutions**: Support for 480P, 720P, and custom sizes

## Quick Start

### Option 1: Run on Google Colab (FREE!)

**Don't have an NVIDIA GPU? Use Google Colab!**

1. Open the notebook: **[Wan2_2_Colab.ipynb](Wan2_2_Colab.ipynb)**
2. Upload to [Google Colab](https://colab.research.google.com/)
3. Enable GPU: Runtime → Change runtime type → T4 GPU
4. Run all cells and wait for the gradio.live link

See the [Colab Guide](COLAB_GUIDE.md) for detailed instructions.

### Option 2: Run Locally (Requires NVIDIA GPU)

#### 1. Installation

```bash
# Clone the repository (if not already done)
git clone https://github.com/Wan-Video/Wan2.2.git
cd Wan2.2

# Install dependencies
pip install -r requirements_ui.txt
```

#### 2. Download Models

Download at least one model checkpoint (TI2V-5B recommended for consumer GPUs):

```bash
# Install HuggingFace CLI
pip install "huggingface_hub[cli]"

# Download TI2V-5B (works on RTX 4090, 24GB VRAM)
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B --local-dir ./Wan2.2-TI2V-5B
```

For other models, see the [UI Guide](UI_GUIDE.md#2-download-model-checkpoints).

#### 3. Launch the UI

**Linux/Mac:**
```bash
./launch_ui.sh
```

**Windows:**
```batch
launch_ui.bat
```

**Or directly with Python:**
```bash
python app.py
```

The web interface will open at **http://localhost:7860**

## Screenshots

The UI provides tabbed interfaces for each generation mode:

- **Text-to-Video Tab**: Enter prompts and generate videos
- **Image-to-Video Tab**: Upload images and add motion
- **TI2V Tab**: Consumer GPU-friendly generation
- **Speech-to-Video Tab**: Audio-driven video generation

## Usage Examples

### Text-to-Video
1. Select the "Text-to-Video" tab
2. Enter your prompt: "A butterfly flying through a sunny garden"
3. Set checkpoint directory: `./Wan2.2-T2V-A14B`
4. Choose video size: `1280*720`
5. Click "Generate Video"

### Image-to-Video (Consumer GPU)
1. Select the "TI2V (Consumer GPU)" tab
2. Upload an image (optional)
3. Enter a prompt: "The scene comes to life with gentle movement"
4. Set checkpoint directory: `./Wan2.2-TI2V-5B`
5. Click "Generate Video"

### Speech-to-Video
1. Select the "Speech-to-Video" tab
2. Upload a reference image
3. Upload an audio file
4. Add an optional prompt
5. Click "Generate Video"

## GPU Requirements

| Model | VRAM | Best For |
|-------|------|----------|
| **TI2V-5B** | 24GB | Consumer GPUs (RTX 4090, RTX 3090) |
| T2V-A14B | 80GB | Enterprise GPUs (A100, H100) |
| I2V-A14B | 80GB | Enterprise GPUs (A100, H100) |
| S2V-14B | 80GB | Enterprise GPUs (A100, H100) |

**Recommendation:** Start with **TI2V-5B** if you have a consumer GPU!

## Advanced Options

The UI exposes all important parameters:

- **Number of Frames**: Control video length
- **Seed**: Set for reproducible results
- **Sampling Steps**: Quality vs. speed tradeoff
- **Guidance Scale**: Control adherence to prompt
- **Prompt Extension**: AI-enhanced prompts (requires additional setup)

See the [UI Guide](UI_GUIDE.md) for detailed parameter explanations.

## Troubleshooting

### "Model not found" error
- Verify you've downloaded the model checkpoint
- Check the checkpoint directory path is correct

### Out of memory error
- Use TI2V-5B model instead (only needs 24GB)
- Reduce number of frames
- Use a smaller resolution

### Slow generation
- Video generation takes time (several minutes is normal)
- Consider using fewer frames or lower resolution
- TI2V-5B: ~9 minutes for 5-second 720P video on RTX 4090

### UI won't start
```bash
# Reinstall Gradio
pip install --upgrade gradio

# Check Python version (3.8+ required)
python --version
```

## Command Line Alternative

The original command-line interface is still available via `generate.py`. See the main [README.md](README.md) for CLI usage.

## File Structure

```
Wan2.2/
├── app.py                  # Gradio web interface
├── launch_ui.sh           # Linux/Mac launcher
├── launch_ui.bat          # Windows launcher
├── UI_GUIDE.md            # Detailed UI documentation
├── requirements_ui.txt    # UI dependencies
├── generate.py            # Original CLI script
└── wan/                   # Core model code
```

## Documentation

- **[UI Guide](UI_GUIDE.md)**: Comprehensive UI usage guide
- **[Main README](README.md)**: Original project documentation
- **[Install Guide](INSTALL.md)**: Detailed installation instructions

## Links

- **GitHub**: https://github.com/Wan-Video/Wan2.2
- **Project Website**: https://wan.video
- **HuggingFace Models**: https://huggingface.co/Wan-AI
- **Research Paper**: https://arxiv.org/abs/2503.20314
- **Discord Community**: https://discord.gg/AKNgpMK4Yj

## License

This project is licensed under the Apache 2.0 License. See [LICENSE.txt](LICENSE.txt) for details.

## Citation

If you use Wan2.2 in your research, please cite:

```bibtex
@article{wan2025,
      title={Wan: Open and Advanced Large-Scale Video Generative Models},
      author={Team Wan and Ang Wang and Baole Ai and ...},
      journal = {arXiv preprint arXiv:2503.20314},
      year={2025}
}
```

---

**Made with ❤️ by the Wan Video Team**

For issues or questions, please visit our [GitHub Issues](https://github.com/Wan-Video/Wan2.2/issues) or join our [Discord](https://discord.gg/AKNgpMK4Yj).
