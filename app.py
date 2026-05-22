# app.py
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Importando a nova estrutura de Scouting atualizada com o estilo coletivo
from config import SCOUT_PLAYER_SCHEMA, SYSTEM_INSTRUCTION

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

def generate_player_scout(jogador, esquema_proprio, estilo_time, caracteristicas):
    # Organiza os inputs textuais para guiar a análise contextualmente
    lista_caractericas = ", ".join(caracteristicas)
    conteudo_prompt = (
        f"Analise o jogador '{jogador}' levando em consideração as seguintes características individuais informadas: {lista_caractericas}. "
        f"Projete essa análise considerando que a nossa equipe atua estruturada em um esquema tático {esquema_proprio} "
        f"e adota a seguinte identidade/estilo de jogo coletivo: {estilo_time}."
    )
    
    response = client.models.generate_content(
        model="gemini-3.5-flash",
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
        "version": "2.0"
    }), 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    
    # Valida se os dados estruturados chegaram corretamente
    if not data:
        return jsonify({
            "status": "error",
            "message": "Nenhum dado recebido pelo terminal tático."
        }), 400
        
    jogador = data.get("nome_jogador", "").strip()
    esquema_proprio = data.get("minha_formacao", "4-3-3")
    # Captura o novo campo de estilo coletivo (como o exemplo do Bayern) ou define um padrão sutil
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
        # Aciona o modelo passando agora também o estilo coletivo do time
        scout_json_string = generate_player_scout(jogador, esquema_proprio, estilo_time, caracteristicas)
        
        # Desserializa a string JSON retornada pelo Gemini em formato nativo
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