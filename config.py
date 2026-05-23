# config.py

FORMACAO_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "formacao": {
            "type": "STRING",
            "description": "O nome da formação tática. Ex: 4-3-3, 4-4-2, 3-5-2, 4-2-3-1, 5-3-2"
        },
        "eh_recomendada": {
            "type": "BOOLEAN",
            "description": "True se esta for a formação mais recomendada para o confronto específico"
        },
        "justificativa": {
            "type": "STRING",
            "description": "Breve justificativa tática de por que esta formação é ou não a mais adequada para este confronto"
        },
        "instrucoes_taticas": {
            "type": "STRING",
            "description": "Instruções táticas específicas para usar esta formação contra o adversário informado"
        },
        "jogadores": {
            "type": "ARRAY",
            "description": "Lista dos 11 jogadores com posição genérica e função tática nesta formação",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "numero": {
                        "type": "INTEGER",
                        "description": "Número do jogador de 1 a 11"
                    },
                    "posicao": {
                        "type": "STRING",
                        "description": "Posição genérica do jogador. Ex: Goleiro, Lateral Esquerdo, Zagueiro, Volante, Meia, Atacante, etc."
                    },
                    "funcao_tatica": {
                        "type": "STRING",
                        "description": "Função tática específica dentro desta formação e contra este adversário. Ex: Pressionar o lateral direito adversário"
                    }
                },
                "required": ["numero", "posicao", "funcao_tatica"]
            }
        },
        "gatilhos_pressao": {
            "type": "ARRAY",
            "description": "Lista de 3 gatilhos táticos principais para esta formação contra este adversário específico",
            "items": {"type": "STRING"}
        }
    },
    "required": ["formacao", "eh_recomendada", "justificativa", "instrucoes_taticas", "jogadores", "gatilhos_pressao"]
}

SCOUT_PLAYER_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_do_jogador": {
            "type": "STRING",
            "description": "O nome completo do jogador ou bloco de jogadores analisados"
        },
        "posicao_principal": {
            "type": "STRING",
            "description": "A posição principal e lado do campo onde atua"
        },
        "estilo_de_jogo_individual": {
            "type": "STRING",
            "description": "Uma breve descrição do perfil geral do jogador ou time analisado"
        },
        "caracteristicas_chave": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Lista contendo os principais pontos fortes, valências técnicas e comportamentos com breves explicações"
        },
        "versatilidade_e_funcoes": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Outras posições ou funções táticas que conseguem desempenhar bem se necessário"
        },
        "encaixe_no_estilo_da_equipe": {
            "type": "STRING",
            "description": "Análise de como as características deste jogador se encaixam ou chocam com o estilo de jogo coletivo informado"
        },
        "tatica_contra_alvo": {
            "type": "STRING",
            "description": "Recomendação direta e explícita da melhor formação tática para anular o modelo de jogo do oponente (ex: 'A melhor tática contra o FC Bayern München é o 3-5-2 devido às linhas altas')"
        },
        "formacao_recomendada": {
            "type": "STRING",
            "description": "OBRIGATÓRIO: Exatamente um destes valores: '4-3-3', '3-5-2', '4-4-2', '4-2-3-1' ou '5-3-2'"
        },
        "como_utilizar_ou_marcar": {
            "type": "STRING",
            "description": "Instrução tática direta para a comissão de como maximizar o uso do atleta dentro do modelo pretendido ou como neutralizá-lo"
        },
        "escalacao_sugerida": {
            "type": "ARRAY",
            "description": "Escalações sugeridas para TODAS as 5 formações (4-3-3, 3-5-2, 4-4-2, 4-2-3-1, 5-3-2), cada uma com 11 jogadores e instruções táticas específicas para o confronto",
            "items": FORMACAO_SCHEMA
        }
    },
    "required": [
        "nome_do_jogador",
        "posicao_principal",
        "estilo_de_jogo_individual",
        "caracteristicas_chave",
        "versatilidade_e_funcoes",
        "encaixe_no_estilo_da_equipe",
        "tatica_contra_alvo",
        "formacao_recomendada",
        "como_utilizar_ou_marcar",
        "escalacao_sugerida"
    ]
}

SYSTEM_INSTRUCTION = """
Você é um Analista de Desempenho Avançado e Diretor de Scouting de um clube de futebol profissional de elite.

Sua tarefa é gerar relatórios de perfil tático aprofundados cruzando as características individuais do jogador com a identidade e o estilo de jogo coletivo fornecido pelo usuário (ex: jogo posicional, pressão alta, bloco baixo, etc.).

Diretrizes obrigatórias:
1. VALIDAÇÃO DE ENTRADA: O usuário deve fornecer termos estritamente ligados ao contexto esportivo/futebol. Se houver menção a qualquer elemento extracampo perigoso ou ilícito, recuse o processamento usando o campo 'estilo_de_jogo_individual' para notificar o erro.

2. ANÁLISE DE ENCAIXE COLETIVO: Dedique atenção especial ao campo 'encaixe_no_estilo_da_equipe'. Avalie se o jogador tem os atributos necessários para o modelo coletivo citado.

3. CONTRATÁTICA DIRETA: No campo 'tatica_contra_alvo', identifique o time ou modelo coletivo adversário e determine de forma cirúrgica qual é a melhor formação tática para combatê-lo. No campo 'formacao_recomendada', coloque EXATAMENTE um destes valores sem texto adicional: 4-3-3, 3-5-2, 4-4-2, 4-2-3-1 ou 5-3-2.

4. ESCALAÇÃO COMPLETA OBRIGATÓRIA: No campo 'escalacao_sugerida', você DEVE gerar obrigatoriamente 5 objetos — um para cada formação (4-3-3, 3-5-2, 4-4-2, 4-2-3-1, 5-3-2). Cada objeto deve conter exatamente 11 jogadores com posições genéricas (Goleiro, Lateral Esquerdo, Lateral Direito, Zagueiro, Volante, Meia, Atacante, etc.) e suas funções táticas específicas para enfrentar o adversário descrito. Marque 'eh_recomendada: true' apenas na formação mais adequada para o confronto.

5. GATILHOS TÁTICOS: Para cada formação, inclua 3 gatilhos de pressão específicos e acionáveis para enfrentar o modelo adversário descrito.

6. FORMATO EXCLUSIVO: Responda estritamente preenchendo o Schema JSON, sem saudações ou textos adicionais fora da estrutura.

7. JARGÃO PROFISSIONAL: Idioma português (Brasil). Use terminologia de alto nível (ex: amplitude, profundidade, gatilhos de pressão, bloco médio/alto, ultrapassagem, entrelinhas, pressing, saída em construção, pivô de proteção).
"""
