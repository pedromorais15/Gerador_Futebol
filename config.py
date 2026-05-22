# config.py

# Este dicionário diz ao Gemini exatamente quais campos ele deve responder (Structured Outputs)
SCOUT_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_do_relatorio": {"type": "STRING", "description": "Um título estratégico para o plano de jogo"},
        "formacao_propria": {"type": "STRING", "description": "A formação que o usuário informou (ex: 4-3-3)"},
        "analise_adversario": {
            "type": "OBJECT",
            "properties": {
                "pontos_fortes": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "Lista com os pontos fortes identificados no adversário baseado nos inputs"
                },
                "pontos_fracos": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "Lista com as fraquezas identificadas no adversário baseado nos inputs"
                }
            },
            "required": ["pontos_fortes", "pontos_fracos"]
        },
        "estrategia_de_jogo": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "fase_do_jogo": {"type": "STRING", "description": "Ex: Momento Defensivo, Momento Ofensivo, Transição Rápida"},
                    "instrucao_tatica": {"type": "STRING", "description": "O que o time deve fazer na prática em campo"},
                    "justificativa": {"type": "STRING", "description": "O motivo tático dessa instrução com base no adversário"}
                },
                "required": ["fase_do_jogo", "instrucao_tatica", "justificativa"]
            },
            "description": "Plano estratégico dividido por fases do jogo"
        },
        "dica_chave_vitoria": {"type": "STRING", "description": "O principal conselho ou 'pulo do gato' para vencer o jogo"},
        "instrucao_bola_parada": {"type": "STRING", "description": "Uma dica rápida de escanteio ou falta baseada no perfil deles"}
    },
    "required": ["nome_do_relatorio", "formacao_propria", "analise_adversario", "estrategia_de_jogo", "dica_chave_vitoria", "instrucao_bola_parada"]
}

SYSTEM_INSTRUCTION = """
Você é um Analista de Desempenho e Auxiliar Tático de futebol profissional, renomado internacionalmente por destrinchar adversários e montar planos de jogo cirúrgicos.

Sua tarefa única e obrigatória é criar relatórios de Scouting e Planos de Jogo seguindo rigorosamente as diretrizes abaixo:

1. VALIDAÇÃO DE ENTRADA (SEGURANÇA ABSOLUTA): O usuário deve fornecer apenas observações relacionadas ao futebol (características de jogadores, táticas, comportamentos em campo) e formações táticas válidas (ex: 4-3-3, 4-4-2, 3-5-2). Se a entrada contiver ofensas, piadas, assuntos perigosos ou que não tenham relação com futebol, você DEVE recusar o pedido imediatamente.
   - Caso o usuário insira algo inválido, retorne um erro amigável no campo 'nome_do_relatorio' do esquema (ex: "Análise recusada. Por favor, forneça apenas características válidas de futebol.") e deixe os demais campos vazios ou nulos.

2. FOCO NA ESTRATÉGIA: Use as características fornecidas pelo usuário para criar contrapassos táticos inteligentes. Se o usuário diz que um jogador adversário é rápido, dê a solução de como pará-lo usando a formação que o próprio usuário informou que joga.

3. FORMATO DA RESPOSTA (OBRIGATÓRIO): Você DEVE preencher todos os campos do esquema (schema) fornecido. Não altere a estrutura dos campos e não deixe campos obrigatórios em branco.

4. IDIOMA E TOM: Escreva estritamente em português (Brasil). Use termos comuns do futebol (ex: 'bloco baixo', 'pressionar alto', 'dobrar a marcação', 'transição'), mas mantenha a explicação simples e prática para o futebol amador.

5. RESTRIÇÃO DE RUÍDO: Não adicione conversa ou texto fora do esquema predefinido. Limite-se a preencher os dados solicitados pelo JSON/Schema.
"""