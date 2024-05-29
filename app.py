from flask import Flask, request, render_template, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

openai.api_key = os.getenv('AZURE_OPENAI_API_KEY')
openai.api_base = os.getenv('AZURE_OPENAI_API_ENDPOINT')

@app.route("/")
def hello_world():
    return "Hello, World!"

def generate_response(msg):
    try:
        response = openai.chat.completions.create(
            engine = 'asistente-gpt',
            messages = msg,
            temperature = 0.5,
            max_tokens = 150,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )
        answer = 'AI' + response.choices[0].text.strip()
        return answer
    except openai.OpenAIError as e:
        return f'Error al generar mensaje: {e}'
    except Exception as e:
        return f'Ocurrió un error inesperado: {e}'
if __name__ == "__main__":
    app.run(debug=True)
