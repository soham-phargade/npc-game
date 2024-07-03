"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

import asyncio
from concurrent.futures import ThreadPoolExecutor


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
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

def gemini_sync(message):
  chat_session = model.start_chat(
      history=[] # Chat history
  )
  response = chat_session.send_message(message)
  return response.text

async def gemini(message):
  loop = asyncio.get_running_loop()
  with ThreadPoolExecutor() as pool:
      response = await loop.run_in_executor(pool, gemini_sync, message)
  return response
  
if __name__ == "__main__":
  async def main():
    user_message = input("Enter your message: ")
    response = await gemini(user_message)
    print("Gemini Response:", response)
    
  asyncio.run(main())