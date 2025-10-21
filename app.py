#!/usr/bin/env python3
"""
Wan2.2 Gradio UI
A user-friendly interface for the Wan2.2 video generation models
"""

import os
import sys
import gradio as gr
import subprocess
import shutil
from pathlib import Path

# Add the wan directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_generation(task, prompt, image_path, audio_path, size, ckpt_dir,
                   num_frames, seed, use_prompt_extend, steps, guide_scale):
    """Run the video generation using the generate.py script"""

    if not ckpt_dir or not os.path.exists(ckpt_dir):
        return None, "Error: Please specify a valid checkpoint directory"

    # Build command
    cmd = [
        "python", "generate.py",
        "--task", task,
        "--size", size,
        "--ckpt_dir", ckpt_dir,
        "--prompt", prompt or "",
        "--offload_model", "True",
        "--convert_model_dtype",
        "--t5_cpu"
    ]

    # Add optional parameters
    if image_path and os.path.exists(image_path):
        cmd.extend(["--image", image_path])

    if audio_path and os.path.exists(audio_path) and task == "s2v-14B":
        cmd.extend(["--audio", audio_path])

    if num_frames:
        cmd.extend(["--frame_num", str(num_frames)])

    if seed >= 0:
        cmd.extend(["--base_seed", str(seed)])

    if use_prompt_extend:
        cmd.extend(["--use_prompt_extend", "--prompt_extend_method", "local_qwen"])

    if steps:
        cmd.extend(["--sample_steps", str(steps)])

    if guide_scale:
        cmd.extend(["--sample_guide_scale", str(guide_scale)])

    # Run the command
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes timeout
        )

        # Find the generated video file
        output_files = sorted(Path('.').glob(f'{task}*.mp4'), key=os.path.getmtime, reverse=True)

        if output_files:
            video_path = str(output_files[0])
            log_message = f"Generation successful!\n\nStdout:\n{result.stdout}\n\nStderr:\n{result.stderr}"
            return video_path, log_message
        else:
            return None, f"No output video found.\n\nStdout:\n{result.stdout}\n\nStderr:\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return None, "Error: Generation timed out after 10 minutes"
    except Exception as e:
        return None, f"Error: {str(e)}"


def t2v_generate(prompt, size, ckpt_dir, num_frames, seed, use_prompt_extend, steps, guide_scale):
    """Text-to-Video generation"""
    return run_generation("t2v-A14B", prompt, None, None, size, ckpt_dir,
                         num_frames, seed, use_prompt_extend, steps, guide_scale)


def i2v_generate(prompt, image, size, ckpt_dir, num_frames, seed, use_prompt_extend, steps, guide_scale):
    """Image-to-Video generation"""
    if image is None:
        return None, "Error: Please provide an input image"
    return run_generation("i2v-A14B", prompt, image, None, size, ckpt_dir,
                         num_frames, seed, use_prompt_extend, steps, guide_scale)


def ti2v_generate(prompt, image, size, ckpt_dir, num_frames, seed, use_prompt_extend, steps, guide_scale):
    """Text-Image-to-Video generation (can run on consumer GPUs)"""
    return run_generation("ti2v-5B", prompt, image, None, size, ckpt_dir,
                         num_frames, seed, use_prompt_extend, steps, guide_scale)


def s2v_generate(prompt, image, audio, size, ckpt_dir, num_frames, seed, use_prompt_extend, steps, guide_scale):
    """Speech-to-Video generation"""
    if image is None:
        return None, "Error: Please provide a reference image"
    if audio is None:
        return None, "Error: Please provide an audio file"
    return run_generation("s2v-14B", prompt, image, audio, size, ckpt_dir,
                         num_frames, seed, use_prompt_extend, steps, guide_scale)


# Create Gradio Interface
with gr.Blocks(title="Wan2.2 Video Generator", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # Wan2.2 Video Generator

    Generate high-quality videos using the Wan2.2 AI models from Alibaba.

    **Important:** You need to download the model checkpoints first:
    - T2V-A14B: `huggingface-cli download Wan-AI/Wan2.2-T2V-A14B --local-dir ./Wan2.2-T2V-A14B`
    - I2V-A14B: `huggingface-cli download Wan-AI/Wan2.2-I2V-A14B --local-dir ./Wan2.2-I2V-A14B`
    - TI2V-5B: `huggingface-cli download Wan-AI/Wan2.2-TI2V-5B --local-dir ./Wan2.2-TI2V-5B`
    - S2V-14B: `huggingface-cli download Wan-AI/Wan2.2-S2V-14B --local-dir ./Wan2.2-S2V-14B`
    """)

    with gr.Tabs():
        # Text-to-Video Tab
        with gr.Tab("Text-to-Video"):
            gr.Markdown("### Generate videos from text descriptions")
            with gr.Row():
                with gr.Column():
                    t2v_prompt = gr.Textbox(
                        label="Prompt",
                        placeholder="Two anthropomorphic cats in comfy boxing gear...",
                        lines=3
                    )
                    t2v_ckpt = gr.Textbox(
                        label="Checkpoint Directory",
                        placeholder="./Wan2.2-T2V-A14B",
                        value="./Wan2.2-T2V-A14B"
                    )
                    with gr.Row():
                        t2v_size = gr.Dropdown(
                            choices=["1280*720", "832*480", "720*1280", "480*832"],
                            value="1280*720",
                            label="Video Size"
                        )
                        t2v_frames = gr.Slider(1, 241, value=81, step=4, label="Number of Frames")
                    with gr.Row():
                        t2v_seed = gr.Number(label="Seed (-1 for random)", value=-1, precision=0)
                        t2v_steps = gr.Slider(1, 100, value=30, step=1, label="Sampling Steps")
                        t2v_guide = gr.Slider(1.0, 20.0, value=7.5, step=0.5, label="Guidance Scale")
                    t2v_extend = gr.Checkbox(label="Use Prompt Extension", value=False)
                    t2v_btn = gr.Button("Generate Video", variant="primary")

                with gr.Column():
                    t2v_output = gr.Video(label="Generated Video")
                    t2v_log = gr.Textbox(label="Log", lines=10)

            t2v_btn.click(
                fn=t2v_generate,
                inputs=[t2v_prompt, t2v_size, t2v_ckpt, t2v_frames, t2v_seed, t2v_extend, t2v_steps, t2v_guide],
                outputs=[t2v_output, t2v_log]
            )

        # Image-to-Video Tab
        with gr.Tab("Image-to-Video"):
            gr.Markdown("### Animate images with text descriptions")
            with gr.Row():
                with gr.Column():
                    i2v_image = gr.Image(label="Input Image", type="filepath")
                    i2v_prompt = gr.Textbox(
                        label="Prompt",
                        placeholder="A white cat wearing sunglasses on a surfboard...",
                        lines=3
                    )
                    i2v_ckpt = gr.Textbox(
                        label="Checkpoint Directory",
                        placeholder="./Wan2.2-I2V-A14B",
                        value="./Wan2.2-I2V-A14B"
                    )
                    with gr.Row():
                        i2v_size = gr.Dropdown(
                            choices=["1280*720", "832*480", "720*1280", "480*832"],
                            value="1280*720",
                            label="Video Size"
                        )
                        i2v_frames = gr.Slider(1, 241, value=81, step=4, label="Number of Frames")
                    with gr.Row():
                        i2v_seed = gr.Number(label="Seed (-1 for random)", value=-1, precision=0)
                        i2v_steps = gr.Slider(1, 100, value=30, step=1, label="Sampling Steps")
                        i2v_guide = gr.Slider(1.0, 20.0, value=7.5, step=0.5, label="Guidance Scale")
                    i2v_extend = gr.Checkbox(label="Use Prompt Extension", value=False)
                    i2v_btn = gr.Button("Generate Video", variant="primary")

                with gr.Column():
                    i2v_output = gr.Video(label="Generated Video")
                    i2v_log = gr.Textbox(label="Log", lines=10)

            i2v_btn.click(
                fn=i2v_generate,
                inputs=[i2v_prompt, i2v_image, i2v_size, i2v_ckpt, i2v_frames, i2v_seed, i2v_extend, i2v_steps, i2v_guide],
                outputs=[i2v_output, i2v_log]
            )

        # Text-Image-to-Video Tab (Consumer GPU friendly)
        with gr.Tab("TI2V (Consumer GPU)"):
            gr.Markdown("""
            ### Text-Image-to-Video (5B Model)
            This model can run on consumer GPUs like RTX 4090 (24GB VRAM).
            Leave image empty for Text-to-Video mode.
            """)
            with gr.Row():
                with gr.Column():
                    ti2v_prompt = gr.Textbox(
                        label="Prompt",
                        placeholder="Two anthropomorphic cats boxing...",
                        lines=3
                    )
                    ti2v_image = gr.Image(label="Input Image (Optional)", type="filepath")
                    ti2v_ckpt = gr.Textbox(
                        label="Checkpoint Directory",
                        placeholder="./Wan2.2-TI2V-5B",
                        value="./Wan2.2-TI2V-5B"
                    )
                    with gr.Row():
                        ti2v_size = gr.Dropdown(
                            choices=["1280*704", "704*1280"],
                            value="1280*704",
                            label="Video Size"
                        )
                        ti2v_frames = gr.Slider(1, 241, value=81, step=4, label="Number of Frames")
                    with gr.Row():
                        ti2v_seed = gr.Number(label="Seed (-1 for random)", value=-1, precision=0)
                        ti2v_steps = gr.Slider(1, 100, value=30, step=1, label="Sampling Steps")
                        ti2v_guide = gr.Slider(1.0, 20.0, value=7.5, step=0.5, label="Guidance Scale")
                    ti2v_extend = gr.Checkbox(label="Use Prompt Extension", value=False)
                    ti2v_btn = gr.Button("Generate Video", variant="primary")

                with gr.Column():
                    ti2v_output = gr.Video(label="Generated Video")
                    ti2v_log = gr.Textbox(label="Log", lines=10)

            ti2v_btn.click(
                fn=ti2v_generate,
                inputs=[ti2v_prompt, ti2v_image, ti2v_size, ti2v_ckpt, ti2v_frames, ti2v_seed, ti2v_extend, ti2v_steps, ti2v_guide],
                outputs=[ti2v_output, ti2v_log]
            )

        # Speech-to-Video Tab
        with gr.Tab("Speech-to-Video"):
            gr.Markdown("### Generate talking videos from audio and reference image")
            with gr.Row():
                with gr.Column():
                    s2v_image = gr.Image(label="Reference Image", type="filepath")
                    s2v_audio = gr.Audio(label="Audio File", type="filepath")
                    s2v_prompt = gr.Textbox(
                        label="Prompt (Optional)",
                        placeholder="A person talking...",
                        lines=2
                    )
                    s2v_ckpt = gr.Textbox(
                        label="Checkpoint Directory",
                        placeholder="./Wan2.2-S2V-14B",
                        value="./Wan2.2-S2V-14B"
                    )
                    with gr.Row():
                        s2v_size = gr.Dropdown(
                            choices=["1024*704", "704*1024"],
                            value="1024*704",
                            label="Video Size"
                        )
                        s2v_frames = gr.Slider(1, 241, value=80, step=4, label="Number of Frames")
                    with gr.Row():
                        s2v_seed = gr.Number(label="Seed (-1 for random)", value=-1, precision=0)
                        s2v_steps = gr.Slider(1, 100, value=30, step=1, label="Sampling Steps")
                        s2v_guide = gr.Slider(1.0, 20.0, value=7.5, step=0.5, label="Guidance Scale")
                    s2v_extend = gr.Checkbox(label="Use Prompt Extension", value=False)
                    s2v_btn = gr.Button("Generate Video", variant="primary")

                with gr.Column():
                    s2v_output = gr.Video(label="Generated Video")
                    s2v_log = gr.Textbox(label="Log", lines=10)

            s2v_btn.click(
                fn=s2v_generate,
                inputs=[s2v_prompt, s2v_image, s2v_audio, s2v_size, s2v_ckpt, s2v_frames, s2v_seed, s2v_extend, s2v_steps, s2v_guide],
                outputs=[s2v_output, s2v_log]
            )

    gr.Markdown("""
    ---
    ### Notes:
    - **GPU Requirements:** T2V, I2V, and S2V models require ~80GB VRAM. TI2V-5B can run on 24GB VRAM.
    - **Model Download:** Use `pip install huggingface_hub[cli]` then download models with `huggingface-cli download`
    - **Processing Time:** Generation can take several minutes depending on your GPU
    - **Prompt Extension:** Improves video quality but requires additional models

    For more information, visit the [Wan2.2 GitHub Repository](https://github.com/Wan-Video/Wan2.2)
    """)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
