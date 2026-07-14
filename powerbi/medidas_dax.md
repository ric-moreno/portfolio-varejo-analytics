# Medidas DAX — Dashboard "Inteligência de Dados e Mercado - Varejo"

Estrutura sugerida do modelo (esquema estrela):
- **Fato**: `funil_vendas`, `vendas`, `churn_clientes`, `investimento_marketing`
- **Dimensões**: `dCalendario` (criar tabela calendário), `categoria_produto`, `canal_origem`, `cidade`, `segmento`

---

## KPIs comerciais

```dax
Total Leads =
COUNTROWS(funil_vendas)

Total Vendas =
CALCULATE(
    COUNTROWS(funil_vendas),
    funil_vendas[estagio_funil] = "Venda Fechada"
)

Taxa de Conversao % =
DIVIDE([Total Vendas], [Total Leads], 0)

Ticket Medio =
AVERAGE(vendas[valor_venda])

Receita Total =
SUM(vendas[valor_venda])
```

## Churn

```dax
Total Clientes Perdidos =
COUNTROWS(churn_clientes)

Taxa de Churn % =
DIVIDE([Total Clientes Perdidos], [Total Vendas], 0)

Tempo Medio ate Churn (dias) =
AVERAGEX(
    churn_clientes,
    DATEDIFF(RELATED(vendas[data_venda]), churn_clientes[data_churn], DAY)
)
```

## CAC (Custo de Aquisição de Cliente)

```dax
Investimento Total =
SUM(investimento_marketing[investimento_reais])

CAC =
DIVIDE([Investimento Total], [Total Vendas], 0)
```

## Comparação com mercado (benchmark)

```dax
Nosso Ticket Medio =
CALCULATE([Ticket Medio])

Ticket Medio Setor =
CALCULATE(
    AVERAGE(benchmark_mercado[ticket_medio_setor]),
    benchmark_mercado[rede_varejista] = "VarejoMais (nós)"
)

Gap vs Mercado % =
DIVIDE([Nosso Ticket Medio] - [Ticket Medio Setor], [Ticket Medio Setor], 0)
```

## Análise temporal (medida com inteligência de tempo)

```dax
Vendas Mes Anterior =
CALCULATE(
    [Total Vendas],
    DATEADD(dCalendario[Data], -1, MONTH)
)

Variacao MoM % =
DIVIDE([Total Vendas] - [Vendas Mes Anterior], [Vendas Mes Anterior], 0)
```

---

## Sugestão de páginas do dashboard

1. **Visão Executiva** — KPIs principais (vendas, receita, ticket médio, churn, CAC) com variação MoM
2. **Funil Comercial** — funil visual por estágio, segmentado por B2B/B2C e por vendedor
3. **Mercado & Concorrência** — participação de mercado, ticket médio setor vs. nosso, série histórica
4. **Churn & Retenção** — taxa de churn, motivos de perda de cliente, tempo médio até churn
5. **Projeções** — resultado do modelo de forecasting (Python/Prophet), com os 3 cenários
