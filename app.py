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

def generate_player_scout(jogador, esquema_proprio, estilo_time, caracteristicas):
    lista_caractericas = ", ".join(caracteristicas)
    conteudo_prompt = (
        f"Analise o jogador ou grupo '{jogador}' levando em consideração as seguintes características individuais informadas: {lista_caractericas}. "
        f"Considere que a nossa equipe atua estruturada em um esquema tático {esquema_proprio} "
        f"e o modelo/instruções de jogo coletivo adversário ou proposto é: {estilo_time}.\n\n"
        f"Defina obrigatoriamente no campo 'tatica_contra_alvo' qual a melhor formação tática detalhada para neutralizar o modelo '{estilo_time}'. "
        f"Preencha o array 'escalacao_sugerida' contendo exatamente 5 objetos, um para cada esquema: '4-3-3', '4-4-2', '3-5-2', '4-2-3-1', '5-3-2'."
    )
    
    # Utilizando gemini-2.5-pro devido ao tamanho e profundidade do Schema JSON exigido
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
            response_mime_type="application/json",
            response_schema=SCOUT_PLAYER_SCHEMA
        )
    )
    return response.text

@app.route("/api/scout", methods=["POST"])
def scout_player():
    data = request.get_json()
    
    if not data:
        return jsonify({
            "status": "error",
            "message": "Nenhum dado recebido pelo terminal tático."
        }), 400
        
    jogador = data.get("nome_jogador", "").strip()
    esquema_proprio = data.get("minha_formacao", "4-3-3")
    estilo_time = data.get("estilo_time", "").strip() or "Equipe equilibrada com manutenção de posse de bola."
    caracteristicas = data.get("caracteristicas_adversario", [])
    
    if not jogador:
        return jsonify({
            "status": "error",
            "message": "Identificação do jogador obrigatória para iniciar o mapeamento."
        }), 400
        
    if not isinstance(caracteristicas, list) or len(caracteristicas) == 0:
        return jsonify({
            "status": "error",
            "message": "Insira pelo menos uma característica ou comportamento de campo para análise."
        }), 400
    
    try:
        scout_json_string = generate_player_scout(jogador, esquema_proprio, estilo_time, caracteristicas)
        scout_estruturado = json.loads(scout_json_string)
        
        return jsonify({
            "status": "success",
            "dados_scout": scout_estruturado
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Falha na engine de IA: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
