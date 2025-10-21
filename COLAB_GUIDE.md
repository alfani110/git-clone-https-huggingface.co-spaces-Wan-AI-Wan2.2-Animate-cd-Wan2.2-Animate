# Running Wan2.2 on Google Colab

This guide shows you how to run Wan2.2 video generation on Google Colab for **FREE** (with limitations).

## 🚀 Quick Start (3 Steps)

### Step 1: Upload the Notebook to Colab

1. Download the notebook file: **`Wan2_2_Colab.ipynb`**
2. Go to [Google Colab](https://colab.research.google.com/)
3. Click **File** → **Upload notebook**
4. Select the `Wan2_2_Colab.ipynb` file

**OR** open directly from GitHub:
1. Go to [Google Colab](https://colab.research.google.com/)
2. Click **File** → **Open notebook** → **GitHub** tab
3. Paste this URL: `https://github.com/Wan-Video/Wan2.2`
4. Select the `Wan2_2_Colab.ipynb` file

### Step 2: Enable GPU

**This is CRITICAL - the code won't work without a GPU!**

1. In Colab, click **Runtime** → **Change runtime type**
2. Under **Hardware accelerator**, select **T4 GPU** (or **L4** if available)
3. Click **Save**

### Step 3: Run All Cells

1. Click **Runtime** → **Run all** (or press `Ctrl+F9`)
2. Wait for all cells to complete (15-20 minutes total)
3. Look for the **gradio.live** link in the last cell output
4. Click the link to open the UI

That's it! You can now generate videos in your browser! 🎉

---

## 📊 What to Expect

### Free Tier (No Payment Required)
- **GPU**: T4 with 16GB VRAM
- **Model**: TI2V-5B (720P, 24fps)
- **Generation Time**: 10-20 minutes per video
- **Limitations**:
  - Usage limits per day
  - May disconnect after 90 minutes of inactivity
  - Limited to shorter videos (81-161 frames)

### Colab Pro (~$10/month)
- **GPU**: Better GPUs (L4, A100)
- **Longer sessions**: Up to 24 hours
- **Faster generation**: 5-10 minutes per video
- **Worth it if**: You plan to generate many videos

### Colab Pro+ (~$50/month)
- **GPU**: A100 with 40-80GB VRAM
- **All models**: Can run T2V-A14B, I2V-A14B, S2V-14B
- **Priority access**: Background execution
- **Worth it if**: Professional use, many videos

---

## 📝 Cell-by-Cell Breakdown

### Cell 1: Check GPU
- Verifies you have a GPU enabled
- Shows GPU name and VRAM
- **If it fails**: Go back to Step 2 and enable GPU

### Cell 2: Install Dependencies (3-5 minutes)
- Installs Python packages
- Downloads flash_attn
- **May show warnings** - this is normal!

### Cell 3: Clone Repository (30 seconds)
- Downloads Wan2.2 code from GitHub
- Only runs once

### Cell 4: Download Model (10-15 minutes)
- Downloads TI2V-5B (~15GB)
- **This is the longest step**
- Only runs once (model is cached)

### Cell 5: Create UI
- Creates a Colab-optimized Gradio interface
- Instant

### Cell 6: Launch UI
- Starts the web interface
- Gives you a **public link** (gradio.live)
- **Keep this cell running** while you use the UI

---

## 💡 Using the UI

### Text-to-Video Mode
1. Leave the **Image** field empty
2. Enter a detailed prompt
3. Choose settings:
   - **Size**: 1280*704 (landscape) or 704*1280 (portrait)
   - **Frames**: 81 (start here, ~3 seconds)
   - **Seed**: -1 for random, or a number for reproducibility
4. Click **Generate Video**
5. Wait 10-20 minutes

### Image-to-Video Mode
1. Upload an image
2. Describe the motion you want
3. Same settings as above
4. Generate!

### Example Prompts

**Good prompts are detailed:**
- ✅ "A golden retriever puppy playing in a field of wildflowers, sunny day, camera slowly panning around the dog, shallow depth of field"
- ❌ "dog playing"

**More examples:**
- "Aerial drone shot flying over a tropical beach with turquoise water and white sand, sunset lighting, cinematic"
- "Close-up of raindrops falling on a window, bokeh city lights in the background, moody atmosphere"
- "A steaming cup of coffee on a wooden table, morning light streaming through window, cozy cafe aesthetic"

---

## ⚠️ Troubleshooting

### "RuntimeError: CUDA out of memory"
**Solution:**
- Reduce frames to 81
- Restart runtime: **Runtime** → **Restart runtime**
- Re-run all cells
- If still fails: Your GPU quota may be exhausted (try again tomorrow)

### "No GPU detected"
**Solution:**
- **Runtime** → **Change runtime type** → **T4 GPU** → **Save**
- Re-run all cells

### Session Disconnected
**Solution:**
- Colab disconnects after 90 minutes of inactivity
- Just re-run Cell 6 (Launch UI) - models are still cached
- If that fails, re-run all cells

### Download Stuck / Very Slow
**Solution:**
- Google's servers may be slow
- Be patient, it can take 15-20 minutes
- If stuck for >30 minutes, restart and try again

### "Generation timed out"
**Solution:**
- T4 GPUs are slower
- Reduce frames to 81
- Consider upgrading to Colab Pro for faster GPUs

### UI Link Not Working
**Solution:**
- Make sure Cell 6 is still running (spinning icon)
- If it stopped, run Cell 6 again
- The gradio.live link expires after 72 hours

---

## 💰 Cost Comparison

| Option | Cost | Speed | Best For |
|--------|------|-------|----------|
| **Colab Free** | $0 | Slow (20min/video) | Testing, learning |
| **Colab Pro** | $10/mo | Medium (8min/video) | Regular use |
| **Colab Pro+** | $50/mo | Fast (5min/video) | Professional |
| **Local RTX 4090** | $1600 one-time | Fast (9min/video) | Heavy users |
| **RunPod** | $0.30/hour | Fast | Pay as you go |

---

## 🎓 Tips for Success

### 1. Start Small
- Use 81 frames first
- Test your prompt
- Then increase to 121 or 161 frames

### 2. Save Your Work
- Download videos immediately
- Colab deletes files when session ends
- Right-click video → Save

### 3. Monitor Usage
- Google tracks your GPU usage
- Free tier has daily limits
- If you hit limits, wait 24 hours or upgrade

### 4. Write Better Prompts
Include:
- Subject (what)
- Action (doing what)
- Setting (where)
- Lighting (when/mood)
- Camera (angle, movement)
- Style (cinematic, artistic, etc.)

### 5. Use Seeds
- Find a good result? Note the seed number!
- Use the same seed with different prompts
- Creates consistent style

---

## 🔗 Additional Resources

- **Wan2.2 GitHub**: https://github.com/Wan-Video/Wan2.2
- **Official Website**: https://wan.video
- **Research Paper**: https://arxiv.org/abs/2503.20314
- **HuggingFace Demos**: https://huggingface.co/Wan-AI
- **Discord Community**: https://discord.gg/AKNgpMK4Yj

---

## ❓ FAQ

**Q: Is this really free?**
A: Yes! Google Colab offers free GPU access with usage limits.

**Q: How long can I use it?**
A: Sessions last up to 12 hours, but may disconnect after 90 min of inactivity.

**Q: Can I use my own images?**
A: Yes! Upload images in the UI for Image-to-Video mode.

**Q: Why is it so slow?**
A: Free tier uses T4 GPUs. Upgrade to Colab Pro for 2-3x speedup.

**Q: Can I run this on my Mac mini M2?**
A: No, unfortunately. Wan2.2 requires NVIDIA GPUs. Colab is your best option!

**Q: Will my data/videos be private?**
A: Gradio links are public but random. Don't generate sensitive content.

**Q: Can I run multiple videos at once?**
A: No, only one generation at a time. Be patient!

---

**Happy generating! 🎬✨**

If you encounter issues not covered here, check the [main README](README.md) or ask in the [Discord](https://discord.gg/AKNgpMK4Yj).
