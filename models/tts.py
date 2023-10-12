from gradio_client import Client
from moviepy.editor import concatenate_audioclips, AudioFileClip
import os, time


def split_message(message, max_length):
    sentences = message.split('.')
    message_parts = []
    current_part = ""

    for sentence in sentences:
        if len(current_part) + len(sentence) + 1 <= max_length:
            current_part += sentence + "."
        else:
            message_parts.append(current_part.strip())
            current_part = sentence + "."

    if current_part:
        message_parts.append(current_part.strip())

    return message_parts


def generate(message, dire, model):
    client = Client("https://elevenlabs-tts.hf.space/")
    max_length = 250
    audio_clips = []
    message_parts = split_message(message, max_length)
    for message_part in message_parts:
        audio_path = client.predict(message_part, model, fn_index=0)
        audio_clip = AudioFileClip(audio_path)
        audio_clips.append(audio_clip)
    audio_final = concatenate_audioclips(audio_clips)
    audio_final_path = os.path.join(dire, "audio.mp3")
    audio_final.write_audiofile(audio_final_path, codec="mp3")
    return audio_final_path

# (Option from: ['Rachel', 'Clyde', 'Domi', 'Dave', 'Fin', 'Bella', 'Antoni', 'Thomas', 'Charlie', 'Emily', 'Elli', 'Callum', 'Patrick', 'Harry', 'Liam', 'Dorothy', 'Josh', 'Arnold', 'Charlotte', 'Matilda', 'Matthew', 'James', 'Joseph', 'Jeremy', 'Michael', 'Ethan', 'Gigi', 'Freya', 'Grace', 'Daniel', 'Serena', 'Adam', 'Nicole', 'Jessie', 'Ryan', 'Sam', 'Glinda', 'Giovanni', 'Mimi', 'Alex'])
