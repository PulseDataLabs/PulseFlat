import csv

fpath = '/home/rodrigo/projects/PulseFlat/data/anbima_ranking_global.csv'

mapping = {
    "data_captura": "data_captura",
    "dt_referencia": "dt_referencia",
    "tipo_ativo": "tipo_ativo",
    "Ordem": "ordem",
    "Administrador": "administrador",
    "Total Global de Ativos (*) - (a) - k-l = m+n": "total_global_ativos",
    "Clubes de Investimento e Carteiras Administradas - (b) - Ativos (-) cotas de Fundos": "clubes_carteiras_administradas_ativos",
    "nan - (c) - Cotas de Fundos Próprios": "clubes_carteiras_administradas_cotas_fundos_proprios",
    "nan - (d) - Cotas de Fundos Terceiros": "clubes_carteiras_administradas_cotas_fundos_terceiros",
    "Fundos em Cotas - (e) - Ativos (-) cotas de Fundos": "fundos_em_cotas_ativos",
    "nan - (f) - Cotas de Fundos Próprios": "fundos_em_cotas_cotas_fundos_proprios",
    "nan - (g) - Cotas de Fundos Terceiros": "fundos_em_cotas_cotas_fundos_terceiros",
    "Fundos de Investimento - (h) - Ativos (-) cotas de Fundos": "fundos_investimento_ativos",
    "nan - (i) - Cotas de Fundos Próprios": "fundos_investimento_cotas_fundos_proprios",
    "nan - (j) - Cotas de Fundos Terceiros": "fundos_investimento_cotas_fundos_terceiros",
    "Sub Total - (k) - b+c+d+e+ f+g+h+i+j": "sub_total_k",
    "Dupla Contagem - (l) - c+d+ f+g+i+j": "dupla_contagem_l",
    "Origem dos recursos (da coluna a) - (m) - Do Grupo": "origem_recursos_do_grupo",
    "nan - (n) - Clientes": "origem_recursos_clientes",
    "Total Global de Ativos (*) - nan": "total_global_ativos_nan",
    "(a) - EFPC Emp.Públicas": "investidor_efpc_emp_publicas",
    "(b) - EFPC Emp. Privadas": "investidor_efpc_emp_privadas",
    "(c) - Seguradora": "investidor_seguradora",
    "(d) - EAPC": "investidor_eapc",
    "(e) - Capitalização": "investidor_capitalizacao",
    "(f) - Corporate": "investidor_corporate",
    "(g) - Middle Market": "investidor_middle_market",
    "(h) - Private": "investidor_private",
    "(i) - Varejo Alta Renda": "investidor_varejo_alta_renda",
    "(j) - Varejo": "investidor_varejo",
    "(k) - Poder Público": "investidor_poder_publico",
    "(l) - RPPS": "investidor_rpps",
    "(m) - Fundos de Investimento": "investidor_fundos_investimento",
    "(n) - Estrangeiros": "investidor_estrangeiros",
    "(o) - Por Conta e Ordem": "investidor_por_conta_ordem",
    "(p) - Outros": "investidor_outros",
    "Renda Fixa - (a) Operação Compromissada - Lastro em Tít. Públ. Federais": "renda_fixa_oper_compromissada_tit_publicos_federais",
    "nan - Lastro em Tít. Est., Municipais e Privados": "renda_fixa_oper_compromissada_tit_estaduais_municipais_privados",
    "nan - (b) - Tít. Públ. Federais": "renda_fixa_tit_publicos_federais",
    "nan - (c) - CDB/RDB": "renda_fixa_cdb_rdb",
    "nan - (d) - Notas Promissórias": "renda_fixa_notas_promissorias",
    "nan - (e) - Debêntures": "renda_fixa_debentures",
    "nan - (f) - Direitos Creditórios": "renda_fixa_direitos_creditorios",
    "nan - (g) - DPGE": "renda_fixa_dpge",
    "nan - (h) - CCB / CCCB": "renda_fixa_ccb_cccb",
    "nan - (i) - Títulos Imobiliários": "renda_fixa_titulos_imobiliarios",
    "nan - (j) - Letras Financeiras": "renda_fixa_letras_financeiras",
    "nan - (k) - Investimento no Exterior": "renda_fixa_investimento_exterior",
    "nan - (l) - Outros": "renda_fixa_outros",
    "nan - (m) - Sub Total Renda Fixa": "renda_fixa_sub_total",
    "Renda Variável - (a) - Ações": "renda_variavel_acoes",
    "nan - (b) - Opções": "renda_variavel_opcoes",
    "nan - (c) - Outros": "renda_variavel_outros",
    "nan - (d) - Sub Total Renda Variável": "renda_variavel_sub_total",
    "(a) - Clubes de Investimento": "clientes_clubes_investimento",
    "(b) - Carteiras Administradas": "clientes_carteiras_administradas",
    "(c) - Fundos em Cotas": "clientes_fundos_em_cotas",
    "(d) - Fundos de Investimento": "clientes_fundos_investimento",
    "(e) - Sut Total (a+b+c+d)": "clientes_sub_total",
    "(f) - Dupla Contagem": "clientes_dupla_contagem",
    "(g) - Total de Clientes (e-f)": "clientes_total",
}

with open(fpath, newline='') as f:
    reader = csv.DictReader(f)
    old_headers = reader.fieldnames
    rows = list(reader)

new_headers = [mapping[h] for h in old_headers]

with open(fpath, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=new_headers)
    writer.writeheader()
    for row in rows:
        new_row = {mapping[k]: v for k, v in row.items()}
        writer.writerow(new_row)

print("Rename mapping applied:")
for old, new in mapping.items():
    print(f"  {old[:65]:65s} -> {new}")
