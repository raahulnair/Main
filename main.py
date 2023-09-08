import openai
import pyaudio
import wave
import os
import pyttsx3

# Set up OpenAI API credentials
openai.api_key = "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"

# Set up PyAudio audio input
audio = pyaudio.PyAudio()

# Set up text-to-speech engine
engine = pyttsx3.init()


# Define function to record audio from microphone
def record_audio():
    chunk = 1024
    retake = pyaudio.paInt16
    channels = 1
    rate = 16000
    record_seconds = 5

    stream = audio.open(format=retake, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)

    print("Listening...")

    frames = []

    for i in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    # Save audio data to file
    with wave.open("input.wav", 'wb') as wave_file:
        wave_file.setnchannels(channels)
        wave_file.setsampwidth(audio.get_sample_size(retake))
        wave_file.setframerate(rate)
        wave_file.writeframes(b''.join(frames))


# Define function to generate response from OpenAI GPT-3 model
def generate_response(prompt):
    with open(prompt, "r") as f:
        prompt_text = f.read()

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_text,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


# Define function to convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()


# Define function to play audio through speaker
def play_audio(audio_data):
    filename = "output.wav"
    with wave.open(filename, 'wb') as wave_file:
        wave_file.setnchannels(1)
        wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(16000)
        wave_file.writeframes(audio_data)

    os.system("aplay output.wav")


# Main loop
while True:
    record_audio()
    text_input = generate_response("input.wav")
    text_to_speech(text_input)
    audio_output = engine.getProperty('voice')
    play_audio(audio_output)
