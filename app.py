# imports
import os
from IPython.display import Markdown, display, update_display
from openai import OpenAI
from huggingface_hub import login
from dotenv import load_dotenv
import os
from google import genai
import gradio as gr
import time
LLAMA =  os.environ.get("HF_MODEL", "meta-llama/Llama-3.2-3B-Instruct")

load_dotenv(override=True)
hf_api_key=os.getenv("HF_TOKEN")
hf_client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_api_key,  # set this as a Space Secret
)

#######Genai#########
genai_api_key=os.getenv('GOOGLE_API_KEY')
genai_client = genai.Client(api_key=genai_api_key)

login(hf_api_key, add_to_git_credential=True)


trascription_prompt = """Generate a verbatim transcript of this audio.
- Preserve the speaker turns if possible (Speaker 1, Speaker 2, etc. or names of speackers)
- Add punctuation and paragraph breaks
"""

def get_transcription(audio_path):
    audio_file =  genai_client.files.upload(file=audio_path)
    resp = genai_client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[trascription_prompt, audio_file],)
    transcription = resp.text
    return transcription

def get_messages(transcription):
      system_message = """
      You produce minutes of meetings from transcripts, with summary, key discussion points,
      takeaways and action items with owners, in markdown format without code blocks.
      """

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

      messages = [
          {"role": "system", "content": system_message},
          {"role": "user", "content": user_prompt}
        ]

      return messages

def generate_meeting_minutes(audio_filename):
    transcription=get_transcription(audio_filename)  
    stream = hf_client.chat.completions.create(
        model=LLAMA,
        messages=get_messages(transcription),
        stream=True
       # streanms one by one in chunks (parts)
    )    
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
      
    yield response
    time.sleep(0.04)
   
with gr.Blocks(title="Meeting Minutes Generator") as demo:
    gr.Markdown("# 🎙️ Meeting Minutes Generator\nDrop audio → transcript + minutes")

    audio = gr.Audio(
        sources=["upload"],
        type="filepath",
        label="Drag & drop an audio file (mp3/wav/m4a/etc.)",
    )


    btn = gr.Button("Generate Meeting minutes")

    with gr.Tab("Meeting Minutes (Markdown)"):
        minutes_out = gr.Markdown()

    btn.click(
        fn=generate_meeting_minutes,
        inputs=[audio],
        outputs=[minutes_out],
    )

if __name__ == "__main__":
    demo.queue().launch(share=True)




