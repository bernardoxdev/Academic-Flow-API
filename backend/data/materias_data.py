# Dicionário com nomes das disciplinas
NOMES_MATERIAS = {
    # Extras
    'atividades_complementares': 'Atividades Complementares',
    'formacao_extensao': 'Formação em Extensão',
    'tcc': 'Trabalho de Conclusão de Curso',
    'eletiva': 'Eletiva',
    'optativa': 'Optativa',
    
    # 1° Semestre
    'icc': 'Introdução a Ciência da Computação',
    'logica': 'Introdução a Lógica',
    'matI': 'Matemática I',
    'algoritmos': 'Algoritmos',
    'labI': 'Laboratório de Programação I',
    
    # 2° Semestre
    'e_dados': 'Estrutura de Dados',
    'labII': 'Laboratório de Programação II',
    'ga': 'Geometria Análitica',
    'lgpa': 'Leitura e Produção de Gêneros Acadêmicos',
    'sistemas_logicos': 'Introdução a Sistemas Lógicos Digitais',
    'matII': 'Matemática II',
    
    # 3° Semestre
    'arquiteturaI': 'Arquitetura e Organização de Computadores I',
    'lab_si': 'Laboratório de Sistemas Digitais e Computacionais',
    'mat_discreta': 'Matemática Discreta',
    'matIII': 'Matemática III',
    'p_modular': 'Programação Modular',
    
    # 4° Semestre
    'algebra': 'Álgebra Linear',
    'analise_software': 'Análise e Projeto de Software',
    'arquiteturaII': 'Arquitetura e Organização de Computadores II',
    'estatistica': 'Estatística e Probabilidade',
    'analise_algoritmos': 'Projeto e Análise de Algoritmos',
    
    # 5° Semestre
    'banco_dados': 'Banco de Dados',
    'calculo_numerico': 'Cálculo Númerico',
    'conceitos_linguagens': 'Conceitos de Linguagens de Programação',
    'ia': 'Inteligência Artificial',
    'teoria_linguagens': 'Teoria de Linguagens',
    
    # 6° Semestre
    'computacao_grafica': 'Computação Gráfica',
    'eng_software': 'Engenharia de Software',
    'ihc': 'Interação Humano-Computador',
    'pesquisa_operacional': 'Pesquisa Operacional',
    'so': 'Sistemas Operacionais',
    
    # 7° Semestre
    'compiladores': 'Compiladores',
    'metodologia_cientifica': 'Metodologia Científica',
    'oficina_software': 'Oficina de Desenvolvimento de Software',
    'redes_computadores': 'Redes de Computadores',
    
    # 9° Semestre
    'computadores_sociedade': 'Computadores e Sociedade'
}

MATERIAS_ENUMERADAS = {
    0: 'atividades_complementares',
    1: 'formacao_extensao',
    2: 'tcc',
    3: 'eletiva',
    4: 'optativa',
    5: 'icc',
    6: 'logica',
    7: 'matI',
    8: 'algoritmos',
    9: 'labI',
    10: 'e_dados',
    11: 'labII',
    12: 'ga',
    13: 'lgpa',
    14: 'sistemas_logicos',
    15: 'matII',
    16: 'arquiteturaI',
    17: 'lab_si',
    18: 'mat_discreta',
    19: 'matIII',
    20: 'p_modular',
    21: 'algebra',
    22: 'analise_software',
    23: 'arquiteturaII',
    24: 'estatistica',
    25: 'analise_algoritmos',
    26: 'banco_dados',
    27: 'calculo_numerico',
    28: 'conceitos_linguagens',
    29: 'ia',
    30: 'teoria_linguagens',
    31: 'computacao_grafica',
    32: 'eng_software',
    33: 'ihc',
    34: 'pesquisa_operacional',
    35: 'so',
    36: 'compiladores',
    37: 'metodologia_cientifica',
    38: 'oficina_software',
    39: 'redes_computadores',
    40: 'computadores_sociedade'
}

# Dicionário de pré-requisitos
FLUXOGRAMA_MATERIAS = {
    # 1° Semestre
    'icc': [],
    'logica': [],
    'matI': [],
    'algoritmos': [],
    'labI': [],
    
    # 2° Semestre
    'e_dados': ['algoritmos'],
    'labII': ['algoritmos', 'e_dados'],
    'ga': [],
    'lpga': [],
    'sistemas_logicos': ['icc'],
    'matII': ['matI'],
    
    # 3° Semestre
    'arquiteturaI': ['sistemas_logicos'],
    'lab_si': ['sistemas_logicos'],
    'grafos': ['e_dados'],
    'mat_discreta': ['logica'],
    'matIII': ['matII'],
    'p_modular': ['e_dados'],
    
    # 4̣° Semestre
    'algebra': [],
    'analise_software': ['p_modular'],
    'arquiteturaII': ['arquiteturaI'],
    'estatistica': ['matII'],
    'analise_algoritmos': ['grafos'],
    'eletiva': [],
    
    # 5° Semestre
    'banco_dados': ['p_modular'],
    'calculo_numerico': ['ga', 'algebra'],
    'conceitos_linguagens': ['p_modular'],
    'ia': ['grafos', 'mat_discreta'],
    'teoria_linguagens': ['e_dados', 'mat_discreta'],
    'eletiva': [],
    
    # 6° Semestre
    'computacao_grafica': ['e_dados', 'ga', 'algebra'],
    'eng_software': ['analise_software', 'banco_dados'],
    'ihc': ['analise_software', 'banco_dados'],
    'pesquisa_operacional': ['e_dados', 'algebra'],
    'so': ['arquiteturaI'],
    
    # 7° Semestre
    'compiladores': ['conceitos_linguagens', 'teoria_linguagens'],
    'metodologia_cientifica': ['banco_dados', 'teoria_linguagens', 'algebra', 'arquiteturaI', 'lgpa'],
    'oficina_software': ['eng_software'],
    'redes_computadores': ['arquiteturaII'],
    'optativa': [],
    
    # 8° Semestre
    'optativa': [],
    'optativa': [],
    'optativa': [],
    'eletiva': [],
    
    # 9° Semestre
    'optativa': [],
    'optativa': [],
    'eletiva': [],
    'computadores_sociedade': ['metodologia_cientifica']
}

FLUXOGRAMA_EXTRAS = {
    'atividades_complementares': 270,
    'formacao_extensao': 330,
    'tcc': 150
}

if __name__ == '__main__':
    pass