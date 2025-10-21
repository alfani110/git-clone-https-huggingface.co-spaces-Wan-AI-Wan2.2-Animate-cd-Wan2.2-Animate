#!/usr/bin/env python3
"""
Wan2.2-Animate UI - Character Animation & Replacement
A user-friendly interface for animating characters or replacing characters in videos
"""

import os
import sys
import gradio as gr
import subprocess
from pathlib import Path
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_preprocessing(mode, video_path, character_image, ckpt_path, output_dir,
                      resolution_w, resolution_h, use_flux, iterations, k, w_len, h_len):
    """Run the preprocessing step"""

    if not video_path or not os.path.exists(video_path):
        return None, "❌ Error: Please provide a valid video file"

    if not character_image or not os.path.exists(character_image):
        return None, "❌ Error: Please provide a valid character image"

    if not ckpt_path or not os.path.exists(ckpt_path):
        return None, "❌ Error: Checkpoint path not found. Download Wan2.2-Animate-14B first."

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Build preprocessing command
    cmd = [
        "python", "./wan/modules/animate/preprocess/preprocess_data.py",
        "--ckpt_path", f"{ckpt_path}/process_checkpoint",
        "--video_path", video_path,
        "--refer_path", character_image,
        "--save_path", output_dir,
        "--resolution_area", str(resolution_w), str(resolution_h)
    ]

    if mode == "Animation":
        cmd.append("--retarget_flag")
        if use_flux:
            cmd.append("--use_flux")
    else:  # Replacement mode
        cmd.extend([
            "--replace_flag",
            "--iterations", str(iterations),
            "--k", str(k),
            "--w_len", str(w_len),
            "--h_len", str(h_len)
        ])

    try:
        print(f"Running preprocessing command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        # Check for output files
        expected_files = ["src_face.mp4", "src_pose.mp4"]
        if mode == "Replacement":
            expected_files.extend(["src_bg.mp4", "src_mask.mp4"])

        all_exist = all(os.path.exists(os.path.join(output_dir, f)) for f in expected_files)

        if all_exist:
            preview_path = os.path.join(output_dir, "src_pose.mp4")
            log_msg = f"✅ Preprocessing successful!\n\nOutput directory: {output_dir}\n\nGenerated files: {', '.join(expected_files)}\n\nYou can now proceed to Step 2: Generate Video\n\n--- Logs ---\nStdout:\n{result.stdout[-2000:]}\n\nStderr:\n{result.stderr[-1000:]}"
            return preview_path, log_msg
        else:
            return None, f"❌ Preprocessing incomplete. Some files missing.\n\nStdout:\n{result.stdout[-2000:]}\n\nStderr:\n{result.stderr[-1000:]}"

    except subprocess.TimeoutExpired:
        return None, "❌ Preprocessing timed out (>10 minutes)"
    except Exception as e:
        return None, f"❌ Error during preprocessing: {str(e)}"


def run_generation(mode, processed_dir, ckpt_path, refert_num, seed, steps, guide_scale):
    """Run the video generation step"""

    if not processed_dir or not os.path.exists(processed_dir):
        return None, "❌ Error: Processed directory not found. Run preprocessing first!"

    if not ckpt_path or not os.path.exists(ckpt_path):
        return None, "❌ Error: Checkpoint path not found"

    # Build generation command
    cmd = [
        "python", "generate.py",
        "--task", "animate-14B",
        "--ckpt_dir", ckpt_path,
        "--src_root_path", processed_dir,
        "--refert_num", str(refert_num),
        "--offload_model", "True",
        "--convert_model_dtype"
    ]

    if mode == "Replacement":
        cmd.extend(["--replace_flag", "--use_relighting_lora"])

    if seed >= 0:
        cmd.extend(["--base_seed", str(seed)])

    if steps:
        cmd.extend(["--sample_steps", str(steps)])

    if guide_scale:
        cmd.extend(["--sample_guide_scale", str(guide_scale)])

    try:
        print(f"Running generation command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)

        # Find generated video
        output_files = sorted(Path('.').glob('animate-14B*.mp4'), key=os.path.getmtime, reverse=True)

        if output_files:
            video_path = str(output_files[0])
            log_msg = f"✅ Video generation successful!\n\nOutput: {video_path}\n\n--- Logs ---\nStdout:\n{result.stdout[-2000:]}\n\nStderr:\n{result.stderr[-1000:]}"
            return video_path, log_msg
        else:
            return None, f"❌ No output video found.\n\nStdout:\n{result.stdout[-2000:]}\n\nStderr:\n{result.stderr[-1000:]}"

    except subprocess.TimeoutExpired:
        return None, "❌ Generation timed out (>30 minutes)"
    except Exception as e:
        return None, f"❌ Error during generation: {str(e)}"


# Create Gradio Interface
with gr.Blocks(title="Wan-Animate: Character Replacement", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 🎭 Wan-Animate: Character Animation & Replacement

    Transform characters in videos using AI! Two modes available:

    - **Animation Mode**: Make your character image perform the motions from a driving video
    - **Replacement Mode**: Replace a character in a video with your character image

    ## 📋 Requirements:
    - Download **Wan2.2-Animate-14B** model first
    - GPU with 80GB VRAM (A100/H100) or use Colab
    - This is a 2-step process: Preprocessing → Generation

    ---
    """)

    # Mode selection
    mode = gr.Radio(
        choices=["Animation", "Replacement"],
        value="Replacement",
        label="Mode",
        info="Animation: Character mimics video motion | Replacement: Replace character in video"
    )

    gr.Markdown("## Step 1: Preprocessing")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Inputs")
            video_input = gr.Video(label="Driving Video", sources=["upload"])
            character_image = gr.Image(label="Character Image", type="filepath")

            ckpt_path = gr.Textbox(
                label="Checkpoint Directory",
                value="./Wan2.2-Animate-14B",
                placeholder="./Wan2.2-Animate-14B"
            )

            output_dir = gr.Textbox(
                label="Output Directory (for preprocessed files)",
                value="./preprocessed_output",
                placeholder="./preprocessed_output"
            )

            with gr.Row():
                resolution_w = gr.Slider(128, 1920, value=1280, step=64, label="Width")
                resolution_h = gr.Slider(128, 1920, value=720, step=64, label="Height")

            gr.Markdown("### Animation Mode Settings")
            use_flux = gr.Checkbox(
                label="Use FLUX for Enhanced Pose Retargeting",
                value=True,
                info="Better quality but slower"
            )

            gr.Markdown("### Replacement Mode Settings")
            with gr.Row():
                iterations = gr.Slider(1, 10, value=3, step=1, label="Iterations (larger mask)")
                k = gr.Slider(1, 20, value=7, step=1, label="K (mask size)")
            with gr.Row():
                w_len = gr.Slider(1, 5, value=1, step=1, label="W_len (width precision)")
                h_len = gr.Slider(1, 5, value=1, step=1, label="H_len (height precision)")

            preprocess_btn = gr.Button("🔄 Run Preprocessing", variant="primary", size="lg")

        with gr.Column():
            gr.Markdown("### Preview & Logs")
            preview_video = gr.Video(label="Pose Preview (src_pose.mp4)")
            preprocess_log = gr.Textbox(label="Preprocessing Log", lines=20)

    gr.Markdown("---")
    gr.Markdown("## Step 2: Generate Final Video")
    gr.Markdown("⚠️ Run this AFTER preprocessing is complete")

    with gr.Row():
        with gr.Column():
            processed_dir_input = gr.Textbox(
                label="Preprocessed Directory",
                value="./preprocessed_output",
                placeholder="./preprocessed_output"
            )

            with gr.Row():
                refert_num = gr.Slider(
                    1, 77, value=1, step=1,
                    label="Reference Frames",
                    info="1 or 5 recommended"
                )
                seed = gr.Number(label="Seed (-1 = random)", value=-1, precision=0)

            with gr.Row():
                steps = gr.Slider(10, 100, value=30, step=1, label="Sampling Steps")
                guide_scale = gr.Slider(1.0, 20.0, value=7.5, step=0.5, label="Guidance Scale")

            generate_btn = gr.Button("🎬 Generate Video", variant="primary", size="lg")

        with gr.Column():
            output_video = gr.Video(label="Generated Video")
            generation_log = gr.Textbox(label="Generation Log", lines=20)

    # Event handlers
    preprocess_btn.click(
        fn=run_preprocessing,
        inputs=[mode, video_input, character_image, ckpt_path, output_dir,
                resolution_w, resolution_h, use_flux, iterations, k, w_len, h_len],
        outputs=[preview_video, preprocess_log]
    )

    generate_btn.click(
        fn=run_generation,
        inputs=[mode, processed_dir_input, ckpt_path, refert_num, seed, steps, guide_scale],
        outputs=[output_video, generation_log]
    )

    gr.Markdown("""
    ---
    ## 💡 Tips:

    ### Animation Mode:
    - Best for: Making a character perform specific motions/dances
    - Character image should be front-facing in a T-pose or A-pose
    - Driving video should show clear body movements
    - Enable FLUX for better results (slower but more accurate)

    ### Replacement Mode:
    - Best for: Replacing a character in an existing video while preserving background/lighting
    - Works best with single-person videos
    - Adjust mask settings if character edges look wrong:
      - Larger iterations/k = bigger mask (more flexible, may affect background)
      - Smaller w_len/h_len = coarser outline (more background preserved)

    ### GPU Requirements:
    - **80GB VRAM** (A100, H100) for local use
    - Or use **Google Colab** with the Colab notebook

    ### Download Model:
    ```bash
    huggingface-cli download Wan-AI/Wan2.2-Animate-14B --local-dir ./Wan2.2-Animate-14B
    ```

    ### Resources:
    - [Project Page](https://humanaigc.github.io/wan-animate/)
    - [GitHub](https://github.com/Wan-Video/Wan2.2)
    - [Model on HuggingFace](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B)
    """)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False
    )
