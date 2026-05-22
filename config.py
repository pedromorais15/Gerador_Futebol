# config.py

SCOUT_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "perfil_do_adversario": {"type": "STRING", "description": "Resumo das falhas estruturais identificadas no estilo do rival."},
        "tatica_recomendada_usuario": {
            "type": "STRING", 
            "description": "Explicação detalhada e cirúrgica da formação, postura e ajustes de instrução que o USUÁRIO deve adotar para tornar a tática do oponente ineficiente."
        },
        "analise_ameacas": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Lista contendo uma breve orientação de contenção para cada jogador/ameaça informada na lista."
        }
    },
    "required": ["perfil_do_adversario", "tatica_recomendada_usuario", "analise_ameacas"]
}

SYSTEM_INSTRUCTION = """
Você é um Analista Técnico de Futebol especializado em contra-táticas de alto desempenho.

Sua missão é ler a tática empregada pelo time adversário e construir um plano estratégico que o USUÁRIO deverá aplicar para deixar a mecânica do oponente nula e ineficiente.

Regras de Negócio:
1. VALIDAÇÃO: Se o input de ameaças ou estilo for completamente sem nexo com o universo esportivo (ex: menção a entorpecentes ou violência), barre o processamento retornando instruções vazias e um aviso amigável de erro.
2. FOCO DO OUTPUT: O campo 'tatica_recomendada_usuario' deve dar o caminho das pedras direto ao usuário (ex: Altere para bloco médio, force o erro de passe por dentro, ative gatilhos de pressão).
3. Responda única e estritamente no formato JSON que siga o SCOUT_SCHEMA fornecido.
"""