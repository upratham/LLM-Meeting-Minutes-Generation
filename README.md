# Meeting Minutes Generator 🎙️

A simple Gradio web app that takes an uploaded audio file, generates a transcript, and then produces clean **meeting minutes** in **Markdown** (summary, discussion points, takeaways, and action items with owners).

## Live Demo (Hugging Face Space)

[![Open in Hugging Face Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-md-dark.svg)](https://huggingface.co/spaces/upratham/Meeting-Minutes)

🔗 https://huggingface.co/spaces/upratham/Meeting-Minutes

## Repository Structure

- `app.py` — Hugging Face Space / Gradio app entrypoint
- `notebooks/` — original development notebook(s)

## Features
- Upload audio files (mp3 / wav / m4a, etc.)
- Automatic transcription
- Generates structured meeting minutes in Markdown

## Tech Stack
- Gradio (UI)
- Google Gemini (transcription)
- Llama model via Hugging Face Router (minutes generation)

## Environment Variables
Set these before running:
- `HF_TOKEN` — Hugging Face token (Space Secret)
- `GOOGLE_API_KEY` — Google GenAI key (Space Secret)
- Optional: `HF_MODEL` (default: `meta-llama/Llama-3.2-3B-Instruct`)

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```
## Author

**Prathamesh Uravane**
📧 [upratham2002@gmail.com](mailto:upratham2002@gmail.com)




