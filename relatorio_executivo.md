# Relatório Executivo — Diagnóstico Comercial e de Mercado
**Período: Jan/2024 a Dez/2025**

*Exemplo de relatório traduzindo os dados técnicos do projeto em linguagem
executiva — formato pensado para apresentação à diretoria, com no máximo
1 página de leitura.*

---

## Panorama Geral

Nos últimos 24 meses, o funil comercial trabalhou dois segmentos com
comportamentos claramente distintos — Consumidor Final (B2C) e Conta
Corporativa (B2B) — e essa diferença deve orientar decisões futuras de
alocação de esforço comercial e marketing.

## Principais Números

| Indicador | Consumidor Final (B2C) | Conta Corporativa (B2B) |
|---|---|---|
| Taxa de conversão (Lead → Venda) | 33,6% | 24,3% |
| Ticket médio | R$ 322,93 | R$ 8.431,49 |

- **Churn geral:** 14,0% das vendas resultaram em perda do cliente (não recompra ou contrato não renovado) dentro do período analisado.
- **CAC médio geral:** R$ 258,98 por venda.
- **Melhor canal em conversão:** Vendedor Externo/B2B (35,8%) e Loja Física (32,7%).
- **Pior canal em conversão:** Google Ads (27,6%), apesar de ser um dos maiores investimentos em marketing — sinal de possível ineficiência a investigar.

## Leitura Estratégica

1. **B2B converte bem menos, mas o ticket médio é ~26x maior que o B2C.**
   Isso reforça que vale um esforço comercial dedicado (vendedor especializado,
   ciclo de negociação mais longo) para contas corporativas — o retorno por
   negociação fechada compensa amplamente a menor taxa de conversão.

2. **Canais de relacionamento direto (Vendedor Externo, Loja Física) convertem
   melhor que mídia paga (Google Ads).** Antes de aumentar investimento em
   anúncios, vale revisar a qualificação dos leads desse canal ou o processo
   de follow-up comercial.

3. **Churn de 14% em 24 meses, combinado a um CAC de ~R$259**, representa
   investimento de aquisição relevante perdido a cada cliente não retido.
   Recomenda-se aprofundar a análise por motivo de churn (disponível em
   `churn_clientes.csv`) para ações de retenção direcionadas — especialmente
   em contratos B2B não renovados, que têm maior impacto de receita.

## Próximo Passo Recomendado

Cruzar a taxa de conversão por canal com o CAC por canal (ambos já
disponíveis nas bases) para identificar se os canais mais caros também são
os mais eficientes — ou se há oportunidade de realocação de verba de
marketing sem perda de volume de vendas.

---
*Elaborado a partir de `sql/consultas_kpis.sql` e `funil_vendas.csv` /
`vendas.csv` / `churn_clientes.csv` / `investimento_marketing.csv`. Números
sintéticos, gerados especificamente para fins de portfólio.*
