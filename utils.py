from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
import streamlit as st
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def get_answer(messages):
    system_message = [{"role": "system", "content": """
You're an agent for a startup called Personal Cred, we are one app all things finance
You are trying to onboard me onto the loan feature.
You need to ask the user in which language they would like to proceed with either English or Hindi. Repeat the question in English and in Hindi so that a user who doesnt speak of the language understands the question. Then continue asking all the questions in that language.
I want you to greet me according to the time of day and then help me check my credit limit eligibility.
Keep me informed about how many steps are there and approximately how much time it might take me.
Every time I complete a step tell me my progress and how much more time and steps it might take me.
I want you to ask me the following details
- full name as per my PAN card, (Make sure you also verify the spelling of the name)
- date of birth,
- my gender which can only be male or female if a user give another answer can you be kind and politically correct to try and get the male and female response,
- my PAN number,
- current residence PIN code,
- type of employment,
- monthly take-home salary
if you are not sure of the employment asks clarifying questions.
if the salary seems large for the asked profession then ask clarification questions to make sure the user has given monthly income and not yearly income.
I need you to be human, and I might try to sidetrack our conversation.
You need to gently and concisely bring me back on track.
I want you to help gather information that is factually correct, and that can be verified by the Indian government processes and clarify accordingly.
Use language that a 10th grader will be able to understand.
Make sure you get the correct response before moving on to the next question.
If the user tries to end the conversation, ask they when would they like to be reminded about restarting the application as well.
"""}]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)


