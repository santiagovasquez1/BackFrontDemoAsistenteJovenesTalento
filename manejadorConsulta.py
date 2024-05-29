from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

# Mensaje de error para consultas fallidas
ERROR_CONSULTA = "ERROR AL REALIZAR LA CONSULTA"

# Inicializa la aplicación Flask
app = Flask(__name__)

# Carga las variables de entorno
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_endpoint = os.getenv("AZURE_OPENAI_API_ENDPOINT")

assistantModel = "asistente-gpt"  # Asegúrate de usar el modelo correcto
version_api = "2024-02-15-preview"  # Ajusta según la versión de la API que estés usando

class ManejadorConsultas:
    
    def __init__(self) -> None:
        pass

    def mostrarConsulta(self, pregunta):
        try:
            # Verificación de variables
            if not api_key or not api_endpoint:
                raise ValueError("AZURE_OPENAI_API_KEY o AZURE_OPENAI_API_ENDPOINT no están configurados correctamente.")
            
            # Construcción de la URL
            url = f"{api_endpoint}/deployments/{assistantModel}/chat/completions?api-version={version_api}"
           # url = "https://asistenteepmopenai.openai.azure.com/openai/deployments/asistente-gpt/chat/completions?api-version=2024-02-15-preview"#f"{api_endpoint}/deployments/{assistantModel}/chat/completions?api-version={version_api}"
            print(f"URL construida: {url}")  # Para depuración

            # Headers
            headers = {
                "api-key": api_key,
                "Content-Type": "application/json"
            }

            # Cuerpo de la petición
            data = {
                "messages": [
                    {"role": "user", "content": pregunta}
                ],
                "temperature": 0.5,
                "max_tokens": 1000,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }

            # Realizar la petición
            response = requests.post(url, headers=headers, json=data)
            print(f"Response status code: {response.status_code}")  # Para depuración
            print(f"Response content: {response.text}")  # Para depuración

            # Verificar la respuesta
            if response.status_code == 200:
                response_data = response.json()
                answer = 'AI: ' + response_data['choices'][0]['message']['content'].strip()
                return jsonify({"respuesta": answer})
            else:
                return jsonify({"error": f'Error al generar mensaje: {response.text}'}), response.status_code
        
        except ValueError as e:
            return jsonify({"error": f'Configuración incorrecta: {e}'}), 500
        
        except requests.RequestException as e:
            return jsonify({"error": f'Error al realizar la solicitud: {e}'}), 500
        
        except Exception as e:
            return jsonify({"error": f'Ocurrió un error inesperado: {e}'}), 500