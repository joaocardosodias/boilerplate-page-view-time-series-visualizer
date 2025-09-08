import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# Eu vou importar os dados do arquivo CSV e definir a coluna 'date' como índice
# O parâmetro parse_dates converte a coluna 'date' para o formato datetime do pandas
# Isso é importante porque facilita a manipulação de datas depois
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Vou limpar os dados removendo os dias com visualizações nos 2,5% superiores ou inferiores
# Isso vai ajudar a remover outliers que podem distorcer as visualizações
# Uso o método quantile() para encontrar os valores que representam os percentis 2,5% e 97,5%
# Depois filtro o DataFrame para manter apenas os valores dentro desse intervalo
# Essa técnica é comum em análise de dados para remover valores extremos
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    
    # Vou criar um gráfico de linha simples mostrando as visualizações ao longo do tempo
    # O parâmetro figsize define o tamanho da figura em polegadas (largura, altura)
    # Uso uma figura grande para que os detalhes fiquem bem visíveis
    fig, ax = plt.subplots(figsize=(15, 5))
    
    # Plotando os dados - eu uso o plot direto do matplotlib
    # df.index contém as datas e df['value'] contém o número de visualizações
    # Defino a cor como vermelho para destacar a linha e linewidth=1 para uma linha fina
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    
    # Adicionando título e rótulos aos eixos como pedido no projeto
    # O título descreve o que o gráfico está mostrando
    # Os rótulos dos eixos indicam o que cada eixo representa
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')  # Eixo X mostra as datas
    ax.set_ylabel('Page Views')  # Eixo Y mostra o número de visualizações
    
    
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    
    # Vou fazer uma cópia para não modificar o dataframe original
    # Isso é uma boa prática para evitar efeitos colaterais indesejados
    df_bar = df.copy()
    
    # Adicionando colunas de ano e mês para agrupar os dados
    # Uso o atributo .year do índice de datas para extrair o ano
    df_bar['year'] = df_bar.index.year
    # Uso o atributo .month do índice de datas para extrair o mês como número (1-12)
    df_bar['month'] = df_bar.index.month
    
    # Agrupando por ano e mês e calculando a média
    # O método groupby permite agrupar os dados por múltiplas colunas
    # Depois seleciono a coluna 'value' e calculo a média para cada grupo
    # O método unstack transforma o resultado em uma tabela onde as linhas são anos e as colunas são meses
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
   
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plotando o gráfico de barras
    # O método plot com kind='bar' cria um gráfico de barras
    # Cada grupo de barras representa um ano, e cada barra dentro do grupo representa um mês
    df_bar.plot(kind='bar', ax=ax)
    
    # Configurando os rótulos e a legenda
    # Defino os rótulos dos eixos conforme solicitado no projeto
    ax.set_xlabel('Years')  # Eixo X mostra os anos
    ax.set_ylabel('Average Page Views')  # Eixo Y mostra a média de visualizações
    
    # Configurando os nomes dos meses na legenda
    # Crio uma lista com os nomes dos meses em inglês para usar na legenda
    # A ordem é importante para corresponder às colunas do DataFrame
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    ax.legend(title='Months', labels=months)  # Adiciono a legenda com título 'Months'
    
    
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    
    # Faço uma cópia do DataFrame original para não modificá-lo
    df_box = df.copy()
    # O método reset_index transforma o índice em uma coluna chamada 'date'
    # Isso é necessário porque precisamos acessar a coluna de datas diretamente
    df_box.reset_index(inplace=True)
    # Crio uma coluna 'year' extraindo o ano de cada data
    df_box['year'] = [d.year for d in df_box.date]
    # Crio uma coluna 'month' extraindo o mês de cada data no formato abreviado (Jan, Feb, etc.)
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # Criando uma ordem para os meses para que apareçam em ordem cronológica
    # Isso é importante porque, por padrão, os gráficos ordenariam os meses alfabeticamente
    # Quero que os meses apareçam na ordem correta: Jan, Feb, Mar, etc.
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    
    # Vou criar dois gráficos de caixa lado a lado
    # O parâmetro (1, 2) indica 1 linha e 2 colunas de subplots
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    
    
    # O boxplot mostra a distribuição dos dados para cada ano
    # Cada caixa mostra: mediana, quartis, valores mínimos/máximos e outliers
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')  # Título do gráfico
    axes[0].set_xlabel('Year')  # Rótulo do eixo X
    axes[0].set_ylabel('Page Views')  # Rótulo do eixo Y
    
    
    # O parâmetro order=month_order garante que os meses apareçam na ordem cronológica
    # e não em ordem alfabética
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=month_order)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')  # Título do gráfico
    axes[1].set_xlabel('Month')  # Rótulo do eixo X
    axes[1].set_ylabel('Page Views')  # Rótulo do eixo Y
    
    
    fig.savefig('box_plot.png')
    return fig
