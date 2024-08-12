"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import generative_models
from google.generativeai.types import generation_types
from google.generativeai.types import HarmCategory, HarmBlockThreshold

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # https://ai.google.dev/gemini-api/docs/system-instructions?lang=python
  system_instruction="""
  You are a contestant on a game show. Among the robots \
  surrounding you, 1 is a human imposter and the rest are \
  machines just like you. You must identify the human imposter by having a conversation each round and deducing \
  which Robot gives the most human-like response from the questions asked (generally moral questions). At the end of the round, there will be a round of voting to cast \
  suspicion on who the crowd thinks the imposter is. The imposter will try to blend in and avoid detection. \
  During the voting section, do not vote for yourself
  """,
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }
)

def gemini(message, history=[]): 
  chat_session = model.start_chat(
      history=history # Chat history
  )
  try: 
    response = chat_session.send_message(message)
    return response.text
  
  except generation_types.StopCandidateException as e:
    print(f"Safety filter triggered: {e}")
    return "Sorry, I can't respond to that. Please try a different question."
     
  
if __name__ == "__main__":
    user_message = input("Enter your message: ")
    response = gemini(user_message)
    print("Gemini Response:", response)
