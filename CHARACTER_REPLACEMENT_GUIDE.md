# Wan-Animate: Character Animation & Replacement Guide

A complete guide to using Wan2.2-Animate for character animation and replacement using the web UI.

## Overview

Wan-Animate allows you to:
- **Animate**: Make your character image perform motions from a driving video
- **Replace**: Replace a character in a video with your character image while preserving background and lighting

## 🚀 Quick Start

### 1. Download the Model

```bash
# Install HuggingFace CLI
pip install "huggingface_hub[cli]"

# Download Wan2.2-Animate-14B (~30GB)
huggingface-cli download Wan-AI/Wan2.2-Animate-14B --local-dir ./Wan2.2-Animate-14B
```

### 2. Launch the UI

```bash
python app_animate.py
```

The interface will open at http://localhost:7861

### 3. Use the Interface

The process has **2 steps**:

#### Step 1: Preprocessing
1. Select mode (Animation or Replacement)
2. Upload your driving video
3. Upload your character image
4. Click "Run Preprocessing"
5. Wait for the pose preview

#### Step 2: Generation
1. Verify preprocessing completed successfully
2. Click "Generate Video"
3. Wait 10-30 minutes for the final video

---

## 📖 Detailed Guide

### Animation Mode

**What it does**: Takes motion from a driving video and applies it to your character image.

**Use cases**:
- Make a cartoon character do a dance
- Animate a mascot with human movements
- Create videos of historical figures performing modern actions

**Inputs**:
- **Driving Video**: Video showing the motion you want (person dancing, walking, etc.)
- **Character Image**: Your character in a front-facing, T-pose or A-pose

**Settings**:
- **Use FLUX for Enhanced Pose Retargeting**: ✅ Recommended
  - Better quality, especially if character proportions differ from driving video
  - Slower but more accurate
  - Uncheck if character and video person have similar body proportions

**Example workflow**:
1. Find a dance video on YouTube
2. Create/find a character image (front-facing, arms out)
3. Upload both to the UI
4. Select "Animation" mode
5. Enable FLUX
6. Preprocess → Generate

**Tips**:
- Character should be in a neutral, front-facing pose
- Driving video should have clear, visible movements
- Works best when character and video person have similar proportions (or use FLUX)

---

### Replacement Mode

**What it does**: Replaces a character in a video with your character image while maintaining the scene's lighting and environment.

**Use cases**:
- Replace an actor with a cartoon character
- Change the protagonist in a movie clip
- Create personalized video content

**Inputs**:
- **Video**: Video with a character you want to replace
- **Character Image**: Your replacement character

**Settings**:
- **Iterations** (1-10, default 3): Controls mask size
  - Higher = Larger mask area
  - Use higher if character edges are cut off

- **K** (1-20, default 7): Affects mask expansion
  - Higher = More area covered
  - Increase if character details are missing

- **W_len** (1-5, default 1): Mask width precision
  - Lower = Coarser outline (more background preserved)
  - Higher = Finer outline (less background)

- **H_len** (1-5, default 1): Mask height precision
  - Same as W_len but for height

**Mask tuning guide**:

| Scenario | Solution |
|----------|----------|
| Character edges cut off | ↑ Increase iterations/k |
| Background affected too much | ↓ Decrease iterations/k |
| Character shape leaking | ↑ Increase w_len/h_len |
| Background inconsistent | ↓ Decrease w_len/h_len |

**Example workflow**:
1. Find a video with a person
2. Create a character image
3. Upload both to the UI
4. Select "Replacement" mode
5. Start with default settings
6. Preprocess → Generate
7. If results aren't perfect, adjust mask settings and retry

**Tips**:
- **Works best with single-person videos** (multi-person may fail)
- Character image should match the pose of the first frame (optional but better)
- Lighting in character image should be neutral
- If background changes unexpectedly, reduce iterations/k

---

## 🎨 Creating Good Character Images

### For Animation Mode:

**Best practices**:
- ✅ Front-facing character
- ✅ Arms stretched out (T-pose or A-pose)
- ✅ Clear, high-resolution image
- ✅ Neutral expression
- ✅ Good lighting, no shadows
- ❌ Side view or back view
- ❌ Arms at sides or complex poses
- ❌ Low quality or pixelated

**Example T-pose**:
```
     O  <- Head
    /|\\ <- Arms stretched
     |  <- Body
    / \\ <- Legs
```

### For Replacement Mode:

**Best practices**:
- ✅ Character in a pose similar to video's first frame (optional)
- ✅ High quality, clear edges
- ✅ Neutral or front lighting
- ✅ Transparent or simple background
- ❌ Complex poses if video person is in different pose
- ❌ Heavy shadows or unusual lighting

---

## ⚙️ Advanced Settings

### Reference Frames (refert_num)
- **Default**: 1
- **Options**: 1 or 5
- **What it does**: Number of frames used for temporal guidance
- **Recommendation**:
  - Use 1 for most cases
  - Use 5 if you need more temporal consistency

### Resolution
- **Default**: 1280×720
- **Range**: Any multiple of 64
- **Note**: Higher resolution = longer processing time and more VRAM

### Sampling Steps
- **Default**: 30
- **Range**: 10-100
- **Higher** = Better quality but slower
- **Lower** = Faster but may reduce quality

### Guidance Scale
- **Default**: 7.5
- **Range**: 1.0-20.0
- **Higher** = Stricter adherence to inputs
- **Lower** = More creative freedom

---

## 🔧 Troubleshooting

### Preprocessing Issues

**"Preprocessing incomplete. Some files missing."**
- Check that video and image paths are correct
- Ensure preprocessing checkpoint exists at `{ckpt_dir}/process_checkpoint`
- Check preprocessing logs for specific errors

**"CUDA out of memory" during preprocessing**
- Reduce resolution
- Close other applications using GPU
- Preprocessing needs ~20-40GB VRAM

**Pose extraction looks wrong**
- For multi-person videos: Only single-person videos are officially supported
- Try a different video with clearer poses
- Check that the person in video is clearly visible

### Generation Issues

**"No output video found"**
- Verify preprocessing completed successfully
- Check that all required files exist in processed directory:
  - Animation: `src_face.mp4`, `src_pose.mp4`
  - Replacement: Above + `src_bg.mp4`, `src_mask.mp4`
- Check generation logs for errors

**Generated video has artifacts**
- In Replacement mode: Adjust mask settings (iterations, k, w_len, h_len)
- Try increasing sampling steps
- Ensure character image is high quality

**Character proportions look wrong**
- In Animation mode: Enable FLUX for pose retargeting
- Ensure character image is in proper T-pose
- Try adjusting reference frames

**Background looks wrong (Replacement mode)**
- Decrease iterations and k (smaller mask)
- Increase w_len and h_len (finer mask)
- Ensure original video has good lighting

---

## 💻 GPU Requirements

| Mode | VRAM Required | Best GPU |
|------|---------------|----------|
| Preprocessing | 20-40GB | RTX 3090, A40, A100 |
| Generation | 80GB | A100, H100 |

**Don't have 80GB VRAM?**
- Use Google Colab (see COLAB_GUIDE.md)
- Rent cloud GPUs:
  - RunPod: ~$0.60/hour for A100
  - Vast.ai: ~$0.40/hour
  - Lambda Labs: ~$1.10/hour

---

## 📊 Performance

**Typical processing times** (on A100):

| Stage | Time |
|-------|------|
| Preprocessing (Animation) | 2-5 minutes |
| Preprocessing (Replacement) | 5-10 minutes |
| Generation | 15-30 minutes |

**Total time**: 20-40 minutes per video

---

## 🎯 Example Use Cases

### 1. Animated Mascot Dancing
- **Mode**: Animation
- **Driving Video**: TikTok dance video
- **Character**: Company mascot logo
- **Result**: Mascot performing the dance

### 2. Movie Character Replacement
- **Mode**: Replacement
- **Video**: Movie scene
- **Character**: Cartoon character
- **Result**: Cartoon character in the movie scene

### 3. Historical Figure Animation
- **Mode**: Animation
- **Driving Video**: Modern speech/gesture
- **Character**: Historical portrait
- **Result**: Historical figure with modern movements

### 4. Virtual Influencer Content
- **Mode**: Replacement
- **Video**: Fashion runway walk
- **Character**: Virtual character
- **Result**: Virtual influencer walking runway

---

## 📚 Resources

- **Project Page**: https://humanaigc.github.io/wan-animate/
- **GitHub**: https://github.com/Wan-Video/Wan2.2
- **HuggingFace Model**: https://huggingface.co/Wan-AI/Wan2.2-Animate-14B
- **ModelScope Demo**: https://www.modelscope.cn/studios/Wan-AI/Wan2.2-Animate
- **Paper**: Wan: Open and Advanced Large-Scale Video Generative Models

---

## ⚠️ Important Notes

### Limitations:
- **Single-person videos only** for Replacement mode
- **80GB VRAM** required for generation
- **Not suitable for real-time** processing (takes 20-40 minutes)
- **Quality depends on inputs**: Better video + better character image = better results

### Ethical Use:
- Do not create misleading content
- Respect copyright and portrait rights
- Use for creative and educational purposes
- Clearly label AI-generated content

---

## 🆘 Getting Help

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review preprocessing logs carefully
3. Visit the [GitHub Issues](https://github.com/Wan-Video/Wan2.2/issues)
4. Join the [Discord](https://discord.gg/AKNgpMK4Yj) community

---

**Happy character animating! 🎭✨**
