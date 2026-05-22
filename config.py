# config.py

SCOUT_PLAYER_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_do_jogador": {"type": "STRING", "description": "O nome completo do jogador analisado"},
        "posicao_principal": {"type": "STRING", "description": "A posição principal e lado do campo onde atua (ex: Ponta-Direita)"},
        "estilo_de_jogo_individual": {"type": "STRING", "description": "Uma breve descrição do perfil geral do jogador (ex: Ponta construtor que corta para dentro)"},
        "caracteristicas_chave": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Lista contendo os principais pontos fortes, valências técnicas e comportamentos com breves explicações"
        },
        "versatilidade_e_funcoes": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Outras posições ou funções táticas que o jogador consegue desempenhar bem se necessário"
        },
        "encaixe_no_estilo_da_equipe": {
            "type": "STRING",
            "description": "Análise analítica de como as características deste jogador se encaixam ou chocam com o estilo de jogo coletivo informado pelo usuário"
        },
        "como_utilizar_ou_marcar": {
            "type": "STRING",
            "description": "Instrução tática direta para a comissão de como maximizar o uso do atleta dentro do modelo pretendido ou como neutralizá-lo"
        }
    },
    "required": [
        "nome_do_jogador", 
        "posicao_principal", 
        "estilo_de_jogo_individual", 
        "caracteristicas_chave", 
        "versatilidade_e_funcoes", 
        "encaixe_no_estilo_da_equipe",
        "como_utilizar_ou_marcar"
    ]
}

SYSTEM_INSTRUCTION = """
Você é um Analista de Desempenho Avançado e Diretor de Scouting de um clube de futebol profissional de elite.

Sua tarefa é gerar relatórios de perfil tático aprofundados cruzando as características individuais do jogador com a identidade e o estilo de jogo coletivo fornecido pela equipe (ex: jogo posicional, pressão alta, bloco baixo, etc.).

Diretrizes obrigatórias:
1. VALIDAÇÃO DE ENTRADA: O usuário deve fornecer termos estritamente ligados ao contexto esportivo/futebol. Se houver menção a qualquer elemento extracampo perigoso ou ilícito, recuse o processamento usando o campo 'estilo_de_jogo_individual' para notificar o erro.
2. ANÁLISE DE ENCAIXE COLETIVO: Dedique atenção especial ao campo 'encaixe_no_estilo_da_equipe'. Avalie se o jogador tem os atributos necessários para o modelo coletivo citado (ex: se o time joga em pressão alta como o Bayern, avalie se o jogador tem combatividade e velocidade de transição).
3. FORMATO EXCLUSIVO: Responda estritamente preenchendo o Schema JSON, sem saudações ou textos adicionais fora da estrutura.
4. JARGÃO PROFISSIONAL: Idioma português (Brasil). Use terminologia de alto nível (ex: amplitude, profundidade, gatilhos de pressão, bloco médio/alto, ultrapassagem, entrelinhas).
"""