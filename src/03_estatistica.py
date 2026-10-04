 #Este arquivo de Codigo lê a tabela de dados Tratados, que foi gerada no processo de ETL, e realiza a análise estatística e geração de gráficos.


import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analisar_dados():
    # Criar as pastas de resultados, se não existirem
    os.makedirs('resultados/estatisticas', exist_ok=True)
    os.makedirs('resultados/graficos', exist_ok=True)

    # Ler os dados tratados
   
    df = pd.read_csv('data/processed/vendas_tratadas.csv')
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    
    # Extrair o dia da semana em português para facilitar a análise
    dias_pt = {
        'Monday': 'Segunda-feira', 'Tuesday': 'Terça-feira', 'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
    }
    df['dia_semana'] = df['data_venda'].dt.day_name().map(dias_pt)

    # Calcular Respostas para as Perguntas de Negócio
    respostas = []
    respostas.append("=== RELATÓRIO DE VENDAS - PERGUNTAS DE NEGÓCIO ===")


    # ESTATÍSTICA DESCRITIVA
   
    print("Gerando estatísticas descritivas...")
    
    # O método describe() gera o resumo estatístico. Arredondamos para 2 casas.
    estatistica_descritiva = df.describe().round(2)
    
    # Salvar o resultado em um arquivo CSV próprio.
    estatistica_descritiva.to_csv('resultados/estatisticas/estatistica_descritiva.csv')
    
       
    # Q1: Qual filial apresentou o maior faturamento?
    filial_vencedora = df.groupby('Filial')['valor_total'].sum().sort_values(ascending=False)
    respostas.append(f"1. Filial com maior faturamento: {filial_vencedora.idxmax()} (Total: {filial_vencedora.max():.2f})")

    # Utilizar o Seaborn para criar um gráfico de barras do faturamento por filial
    plt.figure(figsize=(12, 6))
    ax =sns.barplot(x=filial_vencedora.index, y=filial_vencedora.values, hue=filial_vencedora.index, palette='viridis', legend=False)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3)
    plt.title('Faturamento Total por Filial')
    plt.ylabel('Faturamento Total')
    plt.xlabel('Filial')
    plt.tight_layout()
    plt.savefig('resultados/graficos/1_faturamento_por_filial.png')
    plt.close()


    # Q2: Qual filial realizou a maior quantidade de vendas?
    qtd_filial = df.groupby('Filial')['id_venda'].count()
    respostas.append(f"2. Filial com maior quantidade de vendas: {qtd_filial.idxmax()} ({qtd_filial.max()} vendas)")

    # Utilizar o Matplotlib e Seaborn para criar um gráfico de barras da quantidade de vendas por filial
    plt.figure(figsize=(8, 5))
    cores = sns.color_palette('pastel')[0:len(qtd_filial)]
    plt.bar_label(plt.bar(qtd_filial.index, qtd_filial.values, color=cores), labels=qtd_filial.values)
    plt.title('Distribuição da Quantidade de Vendas por Filial')
    plt.tight_layout()
    plt.savefig('resultados/graficos/2_quantidade_vendas_por_filial.png')
    plt.close()


    # Q3: Qual linha de produto apresentou o maior faturamento?
    linha_produto_vencedora = df.groupby('linha_produto')['valor_total'].sum().round(2).sort_values(ascending=False)
    respostas.append(f"3. Linha de produto com maior faturamento: {linha_produto_vencedora.idxmax()} (Total: {linha_produto_vencedora.max():.2f})")

    # Utilizar o Matplotlib e Seaborn para criar um gráfico de barras do faturamento por linha de produto
    plt.figure(figsize=(12, 6))
    cores = sns.color_palette('pastel')[0:len(linha_produto_vencedora)]
    plt.bar_label(plt.bar(linha_produto_vencedora.index, linha_produto_vencedora.values, color=cores), labels=linha_produto_vencedora.values)
    plt.title('Distribuição do Faturamento por Linha de Produto')
    plt.tight_layout()
    plt.savefig('resultados/graficos/3_faturamento_por_produto.png')
    plt.close()

    # Q4: Qual linha de produto recebeu a melhor avaliação média?
    aval_produto = df.groupby('linha_produto')['Avaliação'].mean().round(2).sort_values(ascending=False)
    respostas.append(f"4. Linha de produto com melhor avaliação média: {aval_produto.idxmax()} (Nota: {aval_produto.max():.2f})")

    # Utilizar o Matplotlib e Seaborn para criar um gráfico de barras da avaliação média por linha de produto
    plt.figure(figsize=(12, 6))
    cores = sns.color_palette('pastel')[0:len(aval_produto)]
    plt.bar_label(plt.bar(aval_produto.index, aval_produto.values, color=cores), labels=aval_produto.values)
    plt.title('Distribuição da Avaliação Média por Linha de Produto')
    plt.tight_layout()
    plt.savefig('resultados/graficos/4_avaliacao_por_produto.png')
    plt.close()


    # Q5: Qual foi a forma de pagamento mais utilizada?
    forma_pagamento = df['forma_pagamento'].value_counts()
    respostas.append(f"5. Forma de pagamento mais utilizada: {forma_pagamento.idxmax()} ({forma_pagamento.max()} transações)")

    # Utilizando o Matplotlib e Seaborn para criar um gráfico de barras da forma de pagamento mais utilizada
    plt.figure(figsize=(8, 5))
    cores = sns.color_palette('pastel')[0:len(forma_pagamento)]
    plt.bar_label(plt.bar(forma_pagamento.index, forma_pagamento.values, color=cores), labels=forma_pagamento.values)
    plt.title('Distribuição da Forma de Pagamento Mais Utilizada')
    plt.tight_layout()
    plt.savefig('resultados/graficos/5_forma_pagamento.png')
    plt.close()


    # Q6: Qual foi o valor médio das vendas?
    valor_medio = df['valor_total'].mean()
    respostas.append(f"6. Valor médio das vendas (Ticket Médio): {valor_medio:.2f}")


    # Q7: Qual foi a maior venda registrada?
    maior_venda = df['valor_total'].max()
    respostas.append(f"7. Maior venda registrada: {maior_venda:.2f}")



    # Q8: Em qual dia da semana ocorreu a maior quantidade de vendas?
    dia_vendas = df['dia_semana'].value_counts()
    respostas.append(f"8. Dia da semana com maior quantidade de vendas: {dia_vendas.idxmax()} ({dia_vendas.max()} vendas)")

 
    # 4. Guardar respostas num ficheiro TXT
    caminho_relatorio = 'resultados/estatisticas/respostas_negocio.txt'
    with open(caminho_relatorio, 'w', encoding='utf-8') as f:
        f.write("\n".join(respostas))
        
    # Imprimir no terminal para conferência
    print("\n" + "\n".join(respostas) + "\n")

    
    print(" Análise estatística e geração de gráficos concluídas com sucesso!")

if __name__ == "__main__":
    analisar_dados()