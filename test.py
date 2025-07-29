
import os
from openai import OpenAI
from dotenv import load_dotenv
# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
load_dotenv()
client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ["OPENAI_API_KEY"],
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "",
        },
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
    model="openai/gpt-4o-mini",
    temperature=1,
    max_tokens=256,
    top_p=1
)

print(response.choices[0].message.content)