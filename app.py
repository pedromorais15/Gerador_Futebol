# app.py
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import SCOUT_PLAYER_SCHEMA, SYSTEM_INSTRUCTION

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

def generate_player_scout(esquema_proprio, estilo_time, estilo_adversario, ameacas):
    lista_ameacas = ", ".join(ameacas)
    conteudo_prompt = (
        f"Gere um relatório de contra-medida tática com base nos seguintes dados de confronto:\n"
        f"- Nosso Esquema Inicial da Equipe: {esquema_proprio}\n"
        f"- Nosso Estilo de Jogo Coletivo Proposto: {estilo_time}\n"
        f"- ESTILO DE JOGO TÁTICO DO ADVERSÁRIO (A SER ANULADO): {estilo_adversario}\n"
        f"- Principais Ameaças/Observações de Campo Enviadas: {lista_ameacas}\n\n"
        f"Determine especificamente no JSON a melhor abordagem tática para o usuário adotar de forma a tornar a tática do oponente ineficiente."
    )
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json", 
            response_schema=SCOUT_PLAYER_SCHEMA,       
        )
    )
    return response.text

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "message": "API Central de Scout AI online!",
        "version": "2.5"
    }), 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    
    if not data:
        return jsonify({
            "status": "error",
            "message": "Nenhum dado recebido pelo terminal tático."
        }), 400
        
    esquema_proprio = data.get("minha_formacao", "4-3-3")
    estilo_time = data.get("estilo_time", "").strip() or "Manutenção de posse de bola com linhas equilibradas."
    estilo_adversario = data.get("estilo_adversario", "").strip()
    ameacas = data.get("ameacas", [])
    
    if not estilo_adversario:
        return jsonify({
            "status": "error",
            "message": "O estilo de jogo tático do adversário é obrigatório para traçar a estratégia."
        }), 400
        
    try:
        scout_json_string = generate_player_scout(esquema_proprio, estilo_time, estilo_adversario, ameacas)
        scout_estruturado = json.loads(scout_json_string)
        
        return jsonify({
            "status": "success",
            "dados_scout": scout_estruturado
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro interno na engine analítica: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)