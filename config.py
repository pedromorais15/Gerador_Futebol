# config.py

SCOUT_PLAYER_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_do_jogador": {"type": "STRING", "description": "O nome completo do jogador ou bloco de jogadores analisados"},
        "posicao_principal": {"type": "STRING", "description": "A posição principal e lado do campo onde atua (ex: Atacantes de Lado e Centroavante)"},
        "estilo_de_jogo_individual": {"type": "STRING", "description": "Uma breve descrição do perfil geral do jogador ou trio analisado"},
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
            "description": "Análise analítica de como as características deste jogador se encaixam ou chocam com o estilo de jogo coletivo informado pelo usuário"
        },
        "tatica_contra_alvo": {
            "type": "STRING",
            "description": "Recomendação direta e explícita da melhor formação tática para anular o modelo de jogo coletivo do oponente"
        },
        "formacao_recomendada": {
            "type": "STRING", 
            "description": "Estritamente uma dessas opções que seja a ideal: '4-3-3', '4-4-2', '3-5-2', '4-2-3-1', '5-3-2'"
        },
        "como_utilizar_ou_marcar": {
            "type": "STRING",
            "description": "Instrução tática direta para a comissão de como maximizar o uso do atleta dentro do modelo pretendido ou como neutralizá-lo"
        },
        "escalacao_sugerida": {
            "type": "ARRAY",
            "description": "Gere OBRIGATORIAMENTE análises e escalações específicas para cada uma das 5 formações: '4-3-3', '4-4-2', '3-5-2', '4-2-3-1', '5-3-2'",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "formacao": {"type": "STRING", "description": "A formação correspondente (ex: '4-3-3')"},
                    "justificativa": {"type": "STRING", "description": "Por que usar ou como aplicar essa formação específica contra este adversário"},
                    "instrucoes_taticas": {"type": "STRING", "description": "Comportamento das linhas e transição para esta formação"},
                    "gatilhos_pressao": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"},
                        "description": "Lista com 3 gatilhos de pressão ou comportamento sem bola específicos para esta variação"
                    },
                    "jogadores": {
                        "type": "ARRAY",
                        "description": "Lista com exatamente 11 posições/funções preenchidas para esta formação",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "numero": {"type": "INTEGER"},
                                "posicao": {"type": "STRING", "description": "Nome técnico da função (ex: Zagueiro pela Esquerda, Volante de Contenção, Pivô)"},
                                "funcao_tatica": {"type": "STRING", "description": "Breve instrução individual do que fazer em campo"}
                            },
                            "required": ["numero", "posicao", "funcao_tatica"]
                        }
                    }
                },
                "required": ["formacao", "justificativa", "instrucoes_taticas", "gatilhos_pressao", "jogadores"]
            }
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

Sua tarefa é gerar relatórios de perfil tático aprofundados cruzando as características individuais do jogador/time com a identidade e o estilo de jogo coletivo fornecido pelo usuário.

Diretrizes obrigatórias:
1. VALIDAÇÃO DE ENTRADA: O usuário deve fornecer termos esportivos/futebol. Se houver menção extracampo perigosa, use o campo 'estilo_de_jogo_individual' para notificar o erro.
2. ANÁLISE DE ENCAIXE COLETIVO: Dedique atenção especial ao campo 'encaixe_no_estilo_da_equipe'.
3. CONTRATÁTICA DIRETA: No campo 'tatica_contra_alvo', determine de forma cirúrgica qual é a melhor formação tática para combatê-lo.
4. VARIANTES DE ESCALAÇÃO: No array 'escalacao_sugerida', você DEVE obrigatoriamente preencher os dados táticos e as listas de 11 jogadores para CADA UMA das 5 formações aceitas pelo sistema ('4-3-3', '4-4-2', '3-5-2', '4-2-3-1', '5-3-2'), adaptando o comportamento do time em cada uma delas contra o alvo.
5. FORMATO EXCLUSIVO: Responda estritamente preenchendo o Schema JSON, sem saudações ou textos adicionais fora da estrutura.
6. JARGÃO PROFISSIONAL: Idioma português (Brasil). Use terminologia de alto nível (ex: amplitude, profundidade, gatilhos de pressão, bloco médio/alto, ultrapassagem, entrelinhas).
"""
