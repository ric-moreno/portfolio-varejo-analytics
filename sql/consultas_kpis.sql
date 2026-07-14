-- -----------------------------------------------------------------------------
-- 1) TAXA DE CONVERSÃO DO FUNIL (por estágio e por segmento B2B/B2C)
-- -----------------------------------------------------------------------------
SELECT
    segmento,
    estagio_funil,
    COUNT(*) AS total_leads,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY segmento), 2) AS pct_do_segmento
FROM funil_vendas
GROUP BY segmento, estagio_funil
ORDER BY segmento, estagio_funil;

SELECT
    segmento,
    ROUND(100.0 * SUM(CASE WHEN estagio_funil = 'Venda Fechada' THEN 1 ELSE 0 END) / COUNT(*), 2) AS taxa_conversao_pct
FROM funil_vendas
GROUP BY segmento;


-- -----------------------------------------------------------------------------
-- 2) TICKET MÉDIO (geral, por categoria de produto, por segmento)
-- -----------------------------------------------------------------------------
SELECT
    categoria_produto,
    segmento,
    ROUND(AVG(valor_venda), 2) AS ticket_medio,
    COUNT(*) AS qtd_vendas
FROM vendas
GROUP BY categoria_produto, segmento
ORDER BY ticket_medio DESC;


-- -----------------------------------------------------------------------------
-- 3) CHURN (taxa de perda de clientes e tempo médio até deixar de comprar)
-- -----------------------------------------------------------------------------
SELECT
    ROUND(100.0 * COUNT(DISTINCT c.venda_id) / (SELECT COUNT(*) FROM vendas), 2) AS taxa_churn_pct,
    ROUND(AVG(julianday(c.data_churn) - julianday(v.data_venda)), 0) AS media_dias_ate_churn
FROM churn_clientes c
JOIN vendas v ON v.venda_id = c.venda_id;

SELECT
    motivo_churn,
    COUNT(*) AS qtd,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM churn_clientes), 2) AS pct
FROM churn_clientes
GROUP BY motivo_churn
ORDER BY qtd DESC;


-- -----------------------------------------------------------------------------
-- 4) CAC — CUSTO DE AQUISIÇÃO DE CLIENTE (investimento / vendas, por mês e canal)
-- -----------------------------------------------------------------------------
WITH vendas_por_mes AS (
    SELECT
        strftime('%Y-%m-01', data_venda) AS mes_referencia,
        COUNT(*) AS qtd_vendas
    FROM vendas
    GROUP BY 1
),
investimento_por_mes AS (
    SELECT
        mes_referencia,
        SUM(investimento_reais) AS investimento_total
    FROM investimento_marketing
    GROUP BY mes_referencia
)
SELECT
    i.mes_referencia,
    i.investimento_total,
    v.qtd_vendas,
    ROUND(i.investimento_total / NULLIF(v.qtd_vendas, 0), 2) AS cac
FROM investimento_por_mes i
LEFT JOIN vendas_por_mes v ON v.mes_referencia = i.mes_referencia
ORDER BY i.mes_referencia;


-- -----------------------------------------------------------------------------
-- 5) DESEMPENHO POR CANAL DE ORIGEM (eficiência comercial)
-- -----------------------------------------------------------------------------
SELECT
    canal_origem,
    COUNT(*) AS total_leads,
    SUM(CASE WHEN estagio_funil = 'Venda Fechada' THEN 1 ELSE 0 END) AS total_vendas,
    ROUND(100.0 * SUM(CASE WHEN estagio_funil = 'Venda Fechada' THEN 1 ELSE 0 END) / COUNT(*), 2) AS taxa_conversao_pct
FROM funil_vendas
GROUP BY canal_origem
ORDER BY taxa_conversao_pct DESC;


-- -----------------------------------------------------------------------------
-- 6) BENCHMARK DE MERCADO (participação e ticket médio setorial ao longo do tempo)
-- -----------------------------------------------------------------------------
SELECT
    mes_referencia,
    rede_varejista,
    participacao_mercado_pct,
    ticket_medio_setor
FROM benchmark_mercado
WHERE rede_varejista = 'VarejoMais (nós)'
ORDER BY mes_referencia;

SELECT
    strftime('%Y-%m-01', v.data_venda) AS mes,
    ROUND(AVG(v.valor_venda), 2) AS nosso_ticket_medio,
    b.ticket_medio_setor
FROM vendas v
JOIN benchmark_mercado b
    ON b.mes_referencia = strftime('%Y-%m-01', v.data_venda)
    AND b.rede_varejista = 'VarejoMais (nós)'
GROUP BY mes, b.ticket_medio_setor
ORDER BY mes;
