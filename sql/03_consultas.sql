-- ====================================================================
-- Arquivo de Script utilizado no Dbeaver para consultas na  CAMADA RAW e tratada no banco (supermarket_sales)
-- ====================================================================


-- ====================================================================
-- RECONHECIMENTO BÁSICO DOS DADOS (TABELA RAW)
-- ====================================================================

-- 1. Visualizar os primeiros 10 registos (Entender a estrutura e formato visual)
SELECT * 
FROM raw_vendas 
LIMIT 10;

-- 2. Contagem total de registos (Confirmar o volume de dados)
SELECT COUNT(*) AS total_linhas 
FROM raw_vendas;

-- 3. Identificar os valores únicos das principais categorias (Dimensões)
-- Filiais existentes:
SELECT DISTINCT branch, city 
FROM raw_vendas 
ORDER BY branch;

-- Linhas de produtos disponíveis:
SELECT DISTINCT product_line 
FROM raw_vendas 
ORDER BY product_line;

-- Métodos de pagamento aceites:
SELECT DISTINCT payment 
FROM raw_vendas;

-- 4. Verificar o período dos dados (Intervalo de tempo)
SELECT 
    MIN(date) AS primeira_venda, 
    MAX(date) AS ultima_venda 
FROM raw_vendas;

-- 5. Resumo estatístico básico da faturação ("Sales") e quantidades
SELECT 
    MIN("Sales") AS menor_venda,
    MAX("Sales") AS maior_venda,
    ROUND(AVG("Sales"::numeric), 2) AS ticket_medio,
    SUM(quantity) AS total_itens_vendidos
FROM raw_vendas;



----------------------------------------------------------------------------------------------------------

-- --------------------------------------------------------------------
-- PARTE 1: CONSULTAS BÁSICAS (Exploração e Validação)
-- --------------------------------------------------------------------

-- Conta o total de registros na tabela para verificar o volume de dados - Percebe-se que ficou igual ao da tabela RAW, 
-- o que indica que não houve perda de dados durante o processo de ETL.

SELECT COUNT(*) AS total_registros 
FROM vendas_tratadas;

-- Lista os primeiros 15 registros para visualizar a estrutura e os dados tratados
SELECT * 
FROM vendas_tratadas 
LIMIT 15;

-- Mostra todas as filiais e cidades distintas (sem repetição) presentes na base
SELECT DISTINCT "Filial", "Cidade" 
FROM vendas_tratadas;

-- Calcula estatísticas gerais de valores numéricos de toda a rede
SELECT 
    MIN(valor_total) AS menor_venda,
    MAX(valor_total) AS maior_venda,
    ROUND(AVG(valor_total)::numeric, 2) AS ticket_medio_geral
FROM vendas_tratadas;


-- --------------------------------------------------------------------
-- PARTE 2: QUESTÕES DE NEGÓCIO E AGRUPAMENTOS
-- --------------------------------------------------------------------

-- Agrupa as vendas por Filial e soma o valor total de vendas de cada uma
-- Ordena o resultado do maior faturamento para o menor
SELECT 
    "Filial", 
    SUM(valor_total) AS faturamento_total
FROM vendas_tratadas
GROUP BY "Filial"
ORDER BY faturamento_total DESC;

-- Conta a quantidade de vendas e calcula o ticket médio por método de pagamento
SELECT 
    forma_pagamento, 
    COUNT(id_venda) AS qtd_vendas,
    ROUND(AVG(valor_total)::numeric, 2) AS valor_medio_transacao
FROM vendas_tratadas
GROUP BY forma_pagamento
ORDER BY qtd_vendas DESC;

-- Cruza o tipo de cliente com a receita gerada e a quantidade total de itens comprados
SELECT 
    tipo_cliente, 
    SUM("Quantidade") AS total_itens_comprados,
    SUM(valor_total) AS receita_gerada
FROM vendas_tratadas
GROUP BY tipo_cliente;

-- Identifica o desempenho das linhas de produto utilizando múltiplos filtros (WHERE)
-- Traz apenas linhas de produtos que venderam mais de 500 unidades no total
SELECT 
    linha_produto, 
    SUM("Quantidade") AS itens_vendidos,
    ROUND(SUM(valor_total)::numeric, 2) AS faturamento,
    ROUND(AVG("Avaliação")::numeric, 2) AS nota_media
FROM vendas_tratadas
GROUP BY linha_produto
HAVING SUM("Quantidade") > 500
ORDER BY faturamento DESC;

-- Isola as vendas de alto valor (acima de 800) feitas exclusivamente por clientes fidelizados (Member)
SELECT 
    id_venda, 
    "Filial", 
    linha_produto, 
    valor_total 
FROM vendas_tratadas
WHERE valor_total > 800 
  AND tipo_cliente = 'Member'
ORDER BY valor_total DESC;