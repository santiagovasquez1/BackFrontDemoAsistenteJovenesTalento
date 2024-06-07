from flask import Flask, jsonify, request, session, abort
import requests
import os
import traceback
from dotenv import load_dotenv

# Mensaje de error para consultas fallidas
ERROR_CONSULTA = "ERROR AL REALIZAR LA CONSULTA"

# Inicializa la aplicación Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para la sesión
session = {}  # Inicializa la sesión

# Carga las variables de entorno
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_endpoint = os.getenv("AZURE_OPENAI_API_ENDPOINT")
assistantModel = os.getenv("AZURE_OPENAI_API_MODEL")
version_api = os.getenv("AZURE_OPENAI_API_VERSION")

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
            print(f"URL construida: {url}")  # Para depuración

            # Headers
            headers = {
                "api-key": api_key,
                "Content-Type": "application/json"
            }

            # Obtener historial de la sesión
            if 'historial' not in session:
                session['historial'] = []

            # Agregar la nueva pregunta al historial
            session['historial'].append({"role": "user", "content": pregunta})

            # Cuerpo de la petición
            data = {
                "messages": session['historial'],
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
                respuesta = response_data['choices'][0]['message']['content'].strip()
                
                # Agregar la respuesta al historial
                session['historial'].append({"role": "assistant", "content": respuesta})
                
                return jsonify({"respuesta": respuesta})
            else:
                return jsonify({"error": f'Error al generar mensaje: {response.text}'}), response.status_code
        
        except ValueError as e:
            return jsonify({"error": f'Configuración incorrecta: {e}'}), 500
        
        except requests.RequestException as e:
            return jsonify({"error": f'Error al realizar la solicitud: {e}'}), 500
        
        except Exception as e:
            return jsonify({"error": f'Ocurrió un error inesperado: {e}'}), 500


# Versión anterior sin contexto de respuesta
"""
    def mostrarConsulta(self, pregunta):
        try:
            # Verificación de variables
            if not api_key or not api_endpoint:
                raise ValueError("AZURE_OPENAI_API_KEY o AZURE_OPENAI_API_ENDPOINT no están configurados correctamente.")
            
            # Construcción de la URL
            url = f"{api_endpoint}/deployments/{assistantModel}/chat/completions?api-version={version_api}"
           
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
"""