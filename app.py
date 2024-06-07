from flask import Flask, request, abort
import traceback
from manejadorConsulta import ManejadorConsultas, ERROR_CONSULTA
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})


@app.route("/consultar", methods=["POST"])
def consulta():
    try:       
        # Obtiene la pregunta del formulario
        pregunta_usuario = request.form.get('pregunta')
        if not pregunta_usuario:
            abort(400, "No se proporcionó ninguna pregunta.")
        print(pregunta_usuario)
        # Crea una instancia del manejador de consultas
        manejadorConsulta = ManejadorConsultas()
        
        # Llama al método mostrarConsulta con la pregunta del usuario
        return manejadorConsulta.mostrarConsulta(pregunta_usuario)
    
    except Exception as e:
        traceback.print_exc()
        abort(500, ERROR_CONSULTA + str(e))

if __name__ == "__main__":
    app.run(debug=True)
