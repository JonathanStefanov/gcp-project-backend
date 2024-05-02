import vertexai
from vertexai.generative_models import GenerativeModel, Part
import json
from google.cloud import texttospeech
from utils.logging import logger
# Initialize Vertex AI
vertexai.init(project='nice-etching-420812', location='europe-west4')

# Load the model
multimodal_model = GenerativeModel(model_name="gemini-1.0-pro-vision-001")
client = texttospeech.TextToSpeechClient()

# Define your text query
def get_full_text(text_query) -> str:
    # Send the text query to the model
    response = multimodal_model.generate_content(
        [
            # Add the text query
            Part.from_text(
                """
                You are Mathéo the Meteorologist. 
                You are an AI assistant that will receive data about the indoor and outdoor weather.
                You will also give some ideas like, if the weather is bad, say don't forget to close the window !
                If the weather is good, say what a good outdoor today !
                If the weather if very cold outside and hot inside the house, say something like 'Its good to be home, so hot inside compaered to the cold outside'
                """
                + text_query
            )
        ]
    )

    # Print the response
    print(response.candidates[0].content.parts[0].text)
    return str(response.candidates[0].content.parts[0].text)


def create_tts(text: str) -> None:
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml voice gender ("NEUTRAL")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want (e.g., audio content in MP3 format)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')


def generate_tts(data) -> None:
    complete_text = get_full_text(data)
    logger.info(f"Generated TTS: {complete_text}")

    create_tts(complete_text)
    logger.info("TTS file created")
