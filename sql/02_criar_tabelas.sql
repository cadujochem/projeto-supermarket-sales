-- Tabela para armazenar os dados brutos (Camada Raw)
CREATE TABLE IF NOT EXISTS raw_vendas (
    invoice_id VARCHAR(30) PRIMARY KEY,
    branch VARCHAR(10) NOT NULL,
    city VARCHAR(50) NOT NULL,
    customer_type VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    product_line VARCHAR(100) NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    quantity INT NOT NULL CHECK (quantity > 0),
    tax_5_percent NUMERIC(10, 4) NOT NULL,
    total NUMERIC(10, 4) NOT NULL CHECK (total >= 0),
    date DATE NOT NULL,
    time TIME NOT NULL,
    payment VARCHAR(50) NOT NULL,
    cogs NUMERIC(10, 2) NOT NULL,
    gross_margin_percentage NUMERIC(10, 6) NOT NULL,
    gross_income NUMERIC(10, 4) NOT NULL,
    rating NUMERIC(3, 1) NOT NULL CHECK (rating BETWEEN 0 AND 10)
);



-- Tabela para armazenar os dados limpos (Camada Tratada)
CREATE TABLE IF NOT EXISTS vendas_tratadas (
    id_venda VARCHAR(50) PRIMARY KEY NOT NULL,
    "Filial" VARCHAR(10) NOT NULL,
    "Cidade" VARCHAR(100) NOT NULL,
    tipo_cliente VARCHAR(50),
    "Gênero" VARCHAR(20),
    linha_produto VARCHAR(150) NOT NULL,
    preco_unitario NUMERIC(10, 2) CHECK (preco_unitario >= 0),
    "Quantidade" INTEGER CHECK ("Quantidade" > 0),
    "Imposto" NUMERIC(10, 2) CHECK ("Imposto" >= 0),
    valor_total NUMERIC(12, 2) CHECK (valor_total >= 0),
    data_venda DATE,
    hora_venda TIME,
    forma_pagamento VARCHAR(50) NOT NULL,
    custo_mercadoria NUMERIC(12, 2) CHECK (custo_mercadoria >= 0),
    margem_percentual NUMERIC(10, 2),
    receita_bruta NUMERIC(12, 2) CHECK (receita_bruta >= 0),
    "Avaliação" NUMERIC(4, 2) CHECK ("Avaliação" >= 0 AND "Avaliação" <= 10)
);