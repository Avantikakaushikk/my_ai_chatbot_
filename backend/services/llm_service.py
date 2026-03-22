import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY", "missing_key"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async def get_response(messages):
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"