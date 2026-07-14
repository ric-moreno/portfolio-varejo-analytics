import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

DATA_INICIO = datetime(2024, 1, 1)
DATA_FIM = datetime(2025, 12, 31)
N_LEADS = 5200

CATEGORIAS = [
    "Eletrônicos", "Casa e Decoração", "Moda e Vestuário", "Beleza e Higiene",
    "Papelaria e Escritório", "Ferramentas", "Brinquedos", "Alimentos e Bebidas",
    "Móveis", "Utilidades Domésticas",
]

CANAIS_ORIGEM = ["Loja Física", "E-commerce", "Marketplace", "Indicação",
                 "Instagram/Redes Sociais", "Google Ads", "Vendedor Externo (B2B)"]

VENDEDORES = ["Ana Ribeiro", "Carlos Souza", "Fernanda Lima", "João Pedro",
              "Mariana Alves", "Rafael Torres"]

CIDADES = ["Campo Grande", "Dourados", "Ponta Porã", "Três Lagoas", "Corumbá"]

MOTIVOS_PERDA = ["Preço", "Concorrente", "Sem retorno", "Desistência da compra",
                 "Fora do orçamento (B2B)", "Prazo de entrega incompatível"]


def gerar_data_aleatoria(inicio, fim):
    delta = (fim - inicio).days
    return inicio + timedelta(days=int(np.random.randint(0, delta)))

leads = []
for i in range(1, N_LEADS + 1):
    data_criacao = gerar_data_aleatoria(DATA_INICIO, DATA_FIM)
    segmento = np.random.choice(["Consumidor Final (B2C)", "Conta Corporativa (B2B)"], p=[0.82, 0.18])
    categoria = np.random.choice(CATEGORIAS)
    canal = np.random.choice(CANAIS_ORIGEM, p=[0.22, 0.20, 0.16, 0.14, 0.12, 0.10, 0.06])
    vendedor = np.random.choice(VENDEDORES)
    cidade = np.random.choice(CIDADES, p=[0.45, 0.20, 0.15, 0.12, 0.08])

    # B2B tem ciclo de venda mais consultivo e converte menos, mas com ticket maior
    prob_avanco = 0.58 if segmento == "Consumidor Final (B2C)" else 0.40
    estagio = np.random.choice(
        ["Perdido", "Lead", "Qualificado", "Proposta Enviada", "Venda Fechada"],
        p=[1 - prob_avanco,
           (prob_avanco) * 0.10,
           (prob_avanco) * 0.15,
           (prob_avanco) * 0.15,
           (prob_avanco) * 0.60]
    )

    valor_base = np.random.normal(320, 90) if segmento == "Consumidor Final (B2C)" else np.random.normal(8500, 2200)
    valor_proposta = max(50, round(valor_base, 2))

    data_fechamento = None
    motivo_perda = None
    if estagio == "Venda Fechada":
        data_fechamento = data_criacao + timedelta(days=int(np.random.randint(1, 30)))
        if data_fechamento > DATA_FIM:
            data_fechamento = DATA_FIM
    elif estagio == "Perdido":
        motivo_perda = np.random.choice(MOTIVOS_PERDA)
        data_fechamento = data_criacao + timedelta(days=int(np.random.randint(1, 20)))

    leads.append({
        "lead_id": i,
        "data_criacao": data_criacao.date(),
        "segmento": segmento,
        "categoria_produto": categoria,
        "canal_origem": canal,
        "vendedor": vendedor,
        "cidade": cidade,
        "estagio_funil": estagio,
        "valor_proposta": valor_proposta,
        "data_fechamento_ou_perda": data_fechamento.date() if data_fechamento else None,
        "motivo_perda": motivo_perda,
    })

df_funil = pd.DataFrame(leads)

# ---------------------------------------------------------------------------
# 2) VENDAS FECHADAS (subset de leads convertidos, com forma de pagamento)
# ---------------------------------------------------------------------------
vendas_fechadas = df_funil[df_funil.estagio_funil == "Venda Fechada"].copy()
vendas_fechadas["forma_pagamento"] = np.random.choice(
    ["Cartão à vista", "Cartão parcelado", "PIX", "Boleto (B2B)", "Contrato Recorrente (B2B)"],
    size=len(vendas_fechadas), p=[0.30, 0.30, 0.25, 0.08, 0.07]
)
vendas_fechadas["venda_id"] = range(1, len(vendas_fechadas) + 1)
df_vendas = vendas_fechadas[[
    "venda_id", "lead_id", "data_fechamento_ou_perda", "categoria_produto",
    "segmento", "cidade", "valor_proposta", "forma_pagamento"
]].rename(columns={"data_fechamento_ou_perda": "data_venda", "valor_proposta": "valor_venda"})

# ---------------------------------------------------------------------------
# 3) CHURN — clientes que deixaram de comprar / contratos B2B não renovados
# ---------------------------------------------------------------------------
taxa_churn = 0.14
n_churn = int(len(df_vendas) * taxa_churn)
churn_ids = np.random.choice(df_vendas["venda_id"], size=n_churn, replace=False)

cancelamentos = []
for vid in churn_ids:
    row = df_vendas[df_vendas.venda_id == vid].iloc[0]
    data_venda = pd.to_datetime(row["data_venda"])
    dias_ate_churn = int(np.random.randint(20, 300))
    data_churn = data_venda + timedelta(days=dias_ate_churn)
    cancelamentos.append({
        "venda_id": vid,
        "data_churn": data_churn.date(),
        "motivo_churn": np.random.choice(
            ["Preço da concorrência", "Insatisfação com produto/entrega",
             "Não recompra (B2C)", "Contrato não renovado (B2B)", "Motivo não informado"]
        )
    })
df_churn = pd.DataFrame(cancelamentos)

# ---------------------------------------------------------------------------
# 4) INVESTIMENTO EM MARKETING (mensal, por canal — para cálculo de CAC)
# ---------------------------------------------------------------------------
meses = pd.date_range(DATA_INICIO, DATA_FIM, freq="MS")
investimento = []
for mes in meses:
    for canal in CANAIS_ORIGEM:
        base = {"Google Ads": 5200, "Instagram/Redes Sociais": 3600, "Marketplace": 4000,
                "Vendedor Externo (B2B)": 3000, "E-commerce": 1200,
                "Loja Física": 800, "Indicação": 250}[canal]
        valor = max(0, np.random.normal(base, base * 0.15))
        investimento.append({
            "mes_referencia": mes.date(),
            "canal": canal,
            "investimento_reais": round(valor, 2)
        })
df_marketing = pd.DataFrame(investimento)

# ---------------------------------------------------------------------------
# 5) BENCHMARK SETORIAL EXTERNO (mercado/concorrência — dado sintético)
# ---------------------------------------------------------------------------
concorrentes = ["Concorrente A", "Concorrente B", "Concorrente C", "VarejoMais (nós)"]
mercado = []
ticket_medio_setor_base = 380
for mes in meses:
    tendencia = 1 + (mes.year - 2024) * 0.025 + np.random.normal(0, 0.02)
    for c in concorrentes:
        participacao = np.random.dirichlet(np.ones(len(concorrentes)))[concorrentes.index(c)]
        mercado.append({
            "mes_referencia": mes.date(),
            "rede_varejista": c,
            "participacao_mercado_pct": round(participacao * 100, 2),
            "ticket_medio_setor": round(ticket_medio_setor_base * tendencia + np.random.normal(0, 25), 2),
            "indice_confianca_consumidor": round(np.random.normal(100, 8), 1),
        })
df_mercado = pd.DataFrame(mercado)

# ---------------------------------------------------------------------------
# Salvar tudo
# ---------------------------------------------------------------------------
df_funil.to_csv("funil_vendas.csv", index=False)
df_vendas.to_csv("vendas.csv", index=False)
df_churn.to_csv("churn_clientes.csv", index=False)
df_marketing.to_csv("investimento_marketing.csv", index=False)
df_mercado.to_csv("benchmark_mercado.csv", index=False)

print("Arquivos gerados:")
print(f"  funil_vendas.csv           -> {len(df_funil)} linhas")
print(f"  vendas.csv                  -> {len(df_vendas)} linhas")
print(f"  churn_clientes.csv          -> {len(df_churn)} linhas")
print(f"  investimento_marketing.csv  -> {len(df_marketing)} linhas")
print(f"  benchmark_mercado.csv       -> {len(df_mercado)} linhas")
