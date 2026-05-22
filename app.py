# app.py
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import SCOUT_SCHEMA, SYSTEM_INSTRUCTION

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)

def processar_contra_medida(minha_formacao, estilo_time, estilo_adversario, ameacas):
    prompt = f"""
    Análise de Combate de Linhas Táticas:
    - Nosso Esquema Inicial: {minha_formacao}
    - Nosso Estilo Proposto: {estilo_time}
    - ESTILO DE JOGO ADVERSÁRIO (A SER ANULADO): {estilo_adversario}
    - Lista de Peças-Chave Oponentes: {', '.join(ameacas)}

    Componha o relatório estratégico focando estritamente em como o usuário deve ajustar suas linhas para anular o estilo rival.
    """
    
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=SCOUT_SCHEMA,
        )
    )
    return response.text

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json() or {}
    
    minha_formacao = data.get("minha_formacao", "4-3-3")
    estilo_time = data.get("estilo_time", "")
    estilo_adversario = data.get("estilo_adversario", "")
    ameacas = data.get("ameacas", [])

    if not estilo_adversario:
        return jsonify({"status": "error", "message": "Preencha o estilo tático do adversário para prosseguir."}), 400

    try:
        resultado_string = processar_contra_medida(minha_formacao, estilo_time, estilo_adversario, ameacas)
        return jsonify({"status": "success", "dados_scout": json.loads(resultado_string)}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro interno do Tactical Engine: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)