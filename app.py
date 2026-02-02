import os
import time
import gradio as gr
from openai import OpenAI
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)
hf_api_key = os.getenv("HF_TOKEN")
genai_api_key = os.getenv("GOOGLE_API_KEY")

if not hf_api_key:
    raise RuntimeError("HF_TOKEN is missing. Add it as a Space Secret.")
if not genai_api_key:
    raise RuntimeError("GOOGLE_API_KEY is missing. Add it as a Space Secret.")

hf_client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_api_key,
)

LLAMA = os.environ.get("HF_MODEL", "meta-llama/Llama-3.2-3B-Instruct")

genai_client = genai.Client(api_key=genai_api_key)

trascription_prompt = """Generate a verbatim transcript of this audio.
- Preserve the speaker turns if possible (Speaker 1, Speaker 2, etc. or names of speakers)
- Add punctuation and paragraph breaks
"""

def get_transcription(audio_path: str) -> str:
    audio_file = genai_client.files.upload(file=audio_path)
    resp = genai_client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[trascription_prompt, audio_file],
    )
    return resp.text or ""

def get_messages(transcription: str):
    system_message = (
        "You produce minutes of meetings from transcripts, with summary, key discussion points, "
        "takeaways and action items with owners, in markdown format without code blocks."
    )

    user_prompt = f"""
Below is an extract transcript of a Denver council meeting.
Please write minutes in markdown without code blocks, including:
- a summary with attendees, location and date
- discussion points
- takeaways
- action items with owners

Transcription:
{transcription}
"""

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt},
    ]

def generate_meeting_minutes(audio_filename):
    transcription = get_transcription(audio_filename)
   

    stream = hf_client.chat.completions.create(
        model=LLAMA,
        messages=get_messages(transcription),
        stream=True,
    )

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        yield response
        time.sleep(0.02)
    

with gr.Blocks(title="Meeting Minutes Generator") as demo:
    gr.Markdown("# 🎙️ Meeting Minutes Generator\nDrop audio → transcript + minutes")

    audio = gr.Audio(sources=["upload"], type="filepath",
                     label="Drag & drop an audio file (mp3/wav/m4a/etc.)")

    btn = gr.Button("Generate Meeting minutes")

    with gr.Tab("Meeting Minutes (Markdown)"):
        minutes_out = gr.Markdown()

    btn.click(fn=generate_meeting_minutes, inputs=[audio], outputs=[minutes_out])

if __name__ == "__main__":
    demo.queue().launch(
        share=True,
    )
