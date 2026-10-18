import os
import tempfile
import gradio as gr
import torch
import torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

model = None

def get_model():
    global model
    if model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = ChatterboxMultilingualTTS.from_pretrained(device=device)
    return model

def generate_voice(text, voice_sample):
    if not text or not text.strip():
        raise gr.Error("पहले हिंदी स्क्रिप्ट लिखें।")

    if not voice_sample:
        raise gr.Error("अपनी आवाज़ का सैंपल अपलोड करें।")

    try:
        tts = get_model()
        audio = tts.generate(
            text=text.strip(),
            language_id="hi",
            audio_prompt_path=voice_sample
        )

        output_path = os.path.join(
            tempfile.gettempdir(), "hindi_voice_output.wav"
        )

        torchaudio.save(
            output_path,
            audio.detach().cpu(),
            tts.sr
        )

        return output_path

    except Exception as error:
        raise gr.Error(f"ऑडियो बनाने में समस्या: {error}")

with gr.Blocks(title="Hindi Voice Studio") as app:
    gr.Markdown("# Hindi Voice Studio")
    gr.Markdown("अपनी आवाज़ के सैंपल से हिंदी टेक्स्ट का ऑडियो बनाएँ।")

    text = gr.Textbox(
        label="हिंदी स्क्रिप्ट",
        placeholder="यहाँ अपनी स्क्रिप्ट लिखें...",
        lines=8
    )

    voice_sample = gr.Audio(
        label="अपनी आवाज़ का सैंपल अपलोड करें",
        type="filepath"
    )

    generate_button = gr.Button("आवाज़ बनाएँ")
    output_audio = gr.Audio(label="तैयार ऑडियो", type="filepath")

    generate_button.click(
        fn=generate_voice,
        inputs=[text, voice_sample],
        outputs=output_audio
    )

app.queue().launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
  )
