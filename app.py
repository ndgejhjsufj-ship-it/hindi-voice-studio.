import gradio as gr

def test_voice(text, audio):
    if not text.strip():
        raise gr.Error("पहले हिंदी स्क्रिप्ट लिखें।")
    if audio is None:
        raise gr.Error("अपनी आवाज़ की फाइल अपलोड करें।")
    return "स्क्रिप्ट और आवाज़ की फाइल मिल गई!"

with gr.Blocks(title="Hindi Voice Studio") as app:
    gr.Markdown("# Hindi Voice Studio")
    text = gr.Textbox(label="हिंदी स्क्रिप्ट लिखें", lines=6)
    audio = gr.Audio(label="अपनी आवाज़ अपलोड करें", type="filepath")
    button = gr.Button("टेस्ट करें")
    result = gr.Textbox(label="स्थिति")
    button.click(test_voice, inputs=[text, audio], outputs=result)

app.launch()
