import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = os.getenv("URL")


def responder(pergunta):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "google/gemma-3-4b-it:free",
            "messages": [{"role": "user", "content": pergunta}],
        }

        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()

        response_json = response.json()
        resposta = response_json["choices"][0]["message"]["content"]
        return resposta

    except Exception as e:
        return f"Erro: {str(e)}"
