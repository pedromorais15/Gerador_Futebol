# app.py
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Importando a nova configuração tática do config.py
from config import SCOUT_SCHEMA, SYSTEM_INSTRUCTION

# Carrega as variáveis de ambiente e inicia o cliente do Gemini
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Inicializa o Flask com suporte a CORS
app = Flask(__name__)
CORS(app)


def generate_scout_report(caracteristicas, formacao):
    # Junta as características enviadas em tópicos para o prompt
    lista_caracteristicas = ", ".join(caracteristicas)
    
    conteudo_prompt = (
        f"Gere um plano de jogo contra um adversário com estas características: {lista_caracteristicas}. "
        f"A nossa equipe joga rigidamente no esquema tático: '{formacao}'. "
        f"Monte a estratégia baseando-se em como o nosso esquema pode neutralizar as forças deles e explorar as fraquezas."
    )
    
    # Faz a chamada para o modelo pedindo a resposta estruturada em JSON
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json", # Força a saída em formato JSON string
            response_schema=SCOUT_SCHEMA,          # Aplica o esquema do Scout
        )
    )
    return response.text


@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "message": "API Scout AI funcionando!",
        "version": "1.0"
    }), 200


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    
    # Validação 1: O JSON foi enviado com todas as chaves obrigatórias?
    if not data or "caracteristicas_adversario" not in data or "minha_formacao" not in data:
        return jsonify({
            "status": "error",
            "message": "Por favor, envie 'caracteristicas_adversario' (lista) e 'minha_formacao' (string) no formato JSON."
        }), 400
        
    caracteristicas = data.get("caracteristicas_adversario", [])
    formacao = data.get("minha_formacao", "").strip()
    
    # Validação 2: É uma lista e possui no mínimo 2 características? A formação foi enviada?
    if not isinstance(caracteristicas, list) or len(caracteristicas) < 2 or len(formacao) < 3:
        return jsonify({
            "status": "error",
            "message": "Você precisa fornecer no mínimo 2 características do adversário e informar a sua formação tática."
        }), 400
    
    try:
        # Pede para o Gemini gerar o relatório estratégico
        scout_json_string = generate_scout_report(caracteristicas, formacao)
        
        # Converte a string JSON em Dicionário Python para o Flask responder adequadamente
        scout_estruturado = json.loads(scout_json_string)
        
        return jsonify({
            "status": "success",
            "dados_enviados": {
                "caracteristicas_adversario": caracteristicas,
                "minha_formacao": formacao
            },
            "dados_scout": scout_estruturado
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar o relatório tático: {str(e)}"
        }), 500


# Executa o servidor local para desenvolvimento
if __name__ == "__main__":
    app.run(debug=True)