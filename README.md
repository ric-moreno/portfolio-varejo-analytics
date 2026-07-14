# Inteligência de Dados e Mercado — Varejo (Projeto de Portfólio)

**Autor:** Pedro Ricardo Moreno · [LinkedIn](https://www.linkedin.com/in/pedroricardomoreno) · [GitHub](https://github.com/ric-moreno)

## Sobre o projeto

Simulação completa de um ambiente de **Análise de Dados e Mercado** aplicado
a uma rede de varejo fictícia, atuando em dois canais
comerciais — varejo tradicional (B2C) e contas corporativas/atacado (B2B).

O projeto cobre o ciclo completo de um analista de dados voltado a mercado e
estratégia comercial: geração/organização de dados de fontes internas (CRM,
funil de vendas) e externas (benchmark setorial/concorrência), modelagem em
SQL, cálculo de KPIs comerciais, dashboard em Power BI/DAX, e projeções de
cenário com Python.

> ⚠️ Todos os dados usados neste projeto são **100% sintéticos**, gerados
> por script Python com `numpy`/`pandas`. Não representam nenhuma empresa real.

---

## O que este projeto demonstra

| Competência | Onde está no projeto |
|---|---|
| Coleta e organização de dados de fontes internas e externas | `gerar_dataset.py` (CRM interno) + `benchmark_mercado.csv` (dado externo setorial) |
| Modelagem de dados e SQL | `sql/consultas_kpis.sql` |
| Power BI / DAX / Power Query | `powerbi/medidas_dax.md` — medidas e estrutura de 5 páginas de dashboard |
| Análise de grandes volumes, padrões e tendências de mercado | `sql/consultas_kpis.sql` (seções 5 e 6) |
| Tradução de dados técnicos em linguagem executiva | `relatorio_executivo.md` |
| Acompanhamento de KPIs e benchmarks históricos | Medida `Variacao MoM %` + seção 6 do SQL |
| CRM, funil de vendas e ciclo comercial B2B/B2C | `funil_vendas.csv` com segmentação explícita |
| Análise de mercado (participação, tendências, concorrência) | `benchmark_mercado.csv` com 3 concorrentes fictícios |
| Indicadores comerciais (ticket médio, conversão, churn, CAC) | `sql/consultas_kpis.sql` (seções 1 a 4) + `powerbi/medidas_dax.md` |
| Cenários e projeções de mercado | `python/forecasting_vendas.py` — 3 cenários + validação de erro (MAE/RMSE) |
| Governança e boas práticas no uso de dados | Dados 100% sintéticos/anonimizados por design |

---

## Estrutura do repositório

```
projeto_varejo/
├── README.md                       <- este arquivo
├── gerar_dataset.py                <- gera todos os dados sintéticos
├── funil_vendas.csv                <- 5.200 leads, funil B2B/B2C completo
├── vendas.csv                      <- vendas fechadas
├── churn_clientes.csv              <- base de churn (clientes perdidos)
├── investimento_marketing.csv      <- investimento mensal por canal (para CAC)
├── benchmark_mercado.csv           <- dados sintéticos de mercado/concorrência
├── relatorio_executivo.md          <- exemplo de leitura executiva dos dados
├── sql/
│   └── consultas_kpis.sql          <- todos os KPIs em SQL puro
├── python/
│   └── forecasting_vendas.py       <- projeção de vendas com 3 cenários
└── powerbi/
    └── medidas_dax.md              <- medidas DAX + estrutura das páginas do dashboard
```

---

## Como reproduzir

```bash
# 1. Gerar os dados sintéticos
python3 gerar_dataset.py

# 2. Rodar as consultas de KPI (exemplo com SQLite)
sqlite3 dados.db < sql/consultas_kpis.sql

# 3. Rodar a projeção de vendas
pip install prophet pandas numpy
python3 python/forecasting_vendas.py

# 4. Importar os .csv no Power BI e aplicar as medidas de powerbi/medidas_dax.md
```

---

## Principais insights (exemplo de leitura executiva dos dados gerados)

- **Conversão B2C é maior que B2B**, mas o **ticket médio B2B é dezenas de
  vezes maior** — reforça que os dois funis exigem estratégias comerciais
  diferentes, não a mesma régua de qualificação e follow-up.
- O **CAC varia por canal**: canais de relacionamento direto (vendedor
  externo, loja física) convertem melhor que mídia paga, sugerindo
  oportunidade de revisão de alocação de verba de marketing.
- A **projeção de vendas** vem sempre acompanhada de intervalo de confiança
  (cenário conservador/base/otimista) e da margem de erro do modelo
  (MAE/RMSE) — nunca um número seco, para dar segurança à tomada de decisão.

---

## Próximos passos (roadmap do projeto)

- [ ] Adicionar página de Power BI publicada (print/gif do dashboard)
- [ ] Incluir análise de coorte de retenção de clientes recorrentes
- [ ] Testar modelo de clusterização (K-Means) para segmentar perfis de cliente por comportamento de compra
- [ ] Publicar relatório executivo em PDF formatado
