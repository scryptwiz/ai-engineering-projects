import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

text_to_summarize = """
OpenAI's GPT series of language models have created headlines the world over. 
These models can generate text, translate languages, and answer questions. 
However, they require careful prompting to ensure accuracy and relevance.
"""

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes text.",
        },
        {
            "role": "user",
            "content": f"Summarize the following text in 10 words or less:\n\n{text_to_summarize}",
        },
    ],
)

print(response.choices[0].message.content)
