### ATENÇÃO este arquivo inicia conexão com o banco de dados, VERIFIQUE SEUS DADOS PARA AUTENTICAÇÃO no POSTGRESQL, 
# caso não tenha o banco de dados criado, siga as instruções do arquivo README.md para criar o banco e a tabela raw_vendas.


import os
import pandas as pd
from sqlalchemy import create_engine

# Configurações de Conexão com o PostgreSQL
USUARIO = "postgres"
SENHA = "990957"  # <- Altere para a sua senha do PostgreSQL
HOST = "localhost"
PORTA = "5432"
BANCO = "supermarket_db"

conexao_url = f"postgresql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"

#função que executa o processo de ETL - Lendo da Tabela Raw e gravando na Tabela Processed, além de gerar o arquivo CSV com os dados tratados.
# Criado com Try/Except para tratamento de erros, caso ocorra algum erro durante o processo de ETL, será exibida uma mensagem de erro no console.

def executar_etl():
    try:
        engine = create_engine(conexao_url)
        
        # Leitura dos dados
        print("Lendo dados da tabela 'raw_vendas' no PostgreSQL...")
        query = "SELECT * FROM raw_vendas;"
        df = pd.read_sql(query, con=engine)
        
        print(f"Registros lidos: {len(df)}")
        
        # Verificação e remoção de duplicidades -

        # Nas consultas efetuadas no arquivo Notebook, não encontrei dados duplicados, por boas práticas irei implementar aqui o codigo que verifica e remove duplicidades, caso existam.
        duplicados_antes = df.duplicated(subset=['invoice_id']).sum()
        if duplicados_antes > 0:
            print(f"Removendo {duplicados_antes} registros duplicados...")
            df.drop_duplicates(subset=['invoice_id'], inplace=True)

        #  Tratamento de tipos de dados e conversões
        df['date'] = pd.to_datetime(df['date'])

        
        # Altera o tipo de dado das colunas que para 'Numeric'
        colunas_numericas = ['unit_price', 'quantity', 'tax_5_percent', 'Sales', 'cogs', 'gross_income', 'rating']
        for col in colunas_numericas:
            df[col] = pd.to_numeric(df[col], errors='coerce')


        #  Nas consultas efetuadas no arquivo Notebook, não encontrei valores nulos, 
        # por boas práticas irei implementar aqui o codigo que trata valores ausentes, caso existam.

        #Aceita tratamento apenas para nulo na coluna 'rating', pois é a única que faz sentido preencher com a média, 
        # as demais colunas são essenciais para o negócio e não podem ser preenchidas com valores aleatórios.

        if df.isnull().sum().sum() > 0:
            print("Tratando valores ausentes...")
            df['rating'] = df['rating'].fillna(df['rating'].mean())
            df.dropna(subset=['invoice_id'], inplace=True)

        # 5. Renomear colunas conforme o Dicionário de Dados
        print("Renomeando colunas conforme o Dicionário de Dados...")
        mapeamento_tratado = {
            'invoice_id': 'id_venda',
            'branch': 'Filial',
            'city': 'Cidade',
            'customer_type': 'tipo_cliente',
            'gender': 'Gênero',
            'product_line': 'linha_produto',
            'unit_price': 'preco_unitario',
            'quantity': 'Quantidade',
            'tax_5_percent': 'Imposto',
            'Sales': 'valor_total',  
            'date': 'data_venda',
            'time': 'hora_venda',
            'payment': 'forma_pagamento',
            'cogs': 'custo_mercadoria',
            'gross_margin_percentage': 'margem_percentual',
            'gross_income': 'receita_bruta',
            'rating': 'Avaliação'
        }
        df.rename(columns=mapeamento_tratado, inplace=True)

        # 6. Exportação da Base Tratada para a camada Processed


        pasta_destino = "data/processed"
        os.makedirs(pasta_destino, exist_ok=True)
        caminho_saida = os.path.join(pasta_destino, "vendas_tratadas.csv")
        df.to_csv(caminho_saida, index=False, encoding='utf-8')

        
        # Carregar para a tabela vendas_tratadas no banco
        
        print("Inserindo dados na tabela 'vendas_tratadas' no PostgreSQL...")
        df.to_sql('vendas_tratadas', con=engine, if_exists='replace', index=False)
        
        print(f" ETL concluído com sucesso! Arquivo gerado em: {caminho_saida}")

    except Exception as e:
        print(f" Erro durante o processo de ETL: {e}")


if __name__ == "__main__":
    executar_etl()