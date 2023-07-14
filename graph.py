import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pasta = os.getcwd()  # Obtém a pasta de trabalho atual
pasta_conexoes = os.path.join(pasta, 'Conexões')  # Caminho para a pasta 'conexões'

colors = ['red', 'blue', 'green', 'orange', 'purple',
          'yellow', 'cyan', 'magenta', 'gray', 'brown']
first_line = True

# Cria a pasta 'conexões' se ela não existir
if not os.path.exists(pasta_conexoes):
    os.makedirs(pasta_conexoes)

for arquivo in os.listdir(pasta):
    if arquivo.endswith(".csv"):
        nome_arquivo = os.path.splitext(arquivo)[0]
        test = nome_arquivo.split("_")[2]

        caminho_arquivo = os.path.join(pasta, arquivo)
        base_filename = caminho_arquivo  # Use o nome do arquivo atual como base

        dados = pd.read_csv(base_filename)
        dados = dados.sort_values(by=dados.columns[0])

        for i in range(0, len(dados), 100):

            timestamp = np.array([])
            connections = np.array([])
            grupo = dados.iloc[i:i + 100].copy()

            for indice, linha in grupo.iterrows():
                if first_line:
                    timestamp_base = linha['timestamp']
                    first_line = False

                timestamp = np.append(
                    timestamp, (linha['timestamp'] - timestamp_base) / 1000000000)
                connections = np.append(
                    connections, linha['SM5G_PDU_SESSION_ACTIVE_PENDING'])

            color_index = i // 100  # Índice da cor com base no grupo atual
            cor = colors[color_index % len(colors)]

            plt.scatter(timestamp, connections,
                        label="Tester {}".format(color_index), color=cor)

            # Calcular a média considerando NaN como zero
            mean_value = np.nanmean(connections)
            # Traçar linha reta com valor médio
            plt.axhline(y=mean_value, color=cor, linestyle='-', label="Média")
            plt.text(max(timestamp), mean_value,
                     f'{mean_value:.2f}', ha='left', va='center')

            # Calcular o desvio padrão
            std_value = np.nanstd(connections)
            # Traçar linha reta com desvio padrão
            plt.axhline(y=mean_value + std_value, color=cor,
                        linestyle='--', label="Desvio Padrão")
            plt.axhline(y=mean_value - std_value, color=cor, linestyle='--')
            plt.text(max(timestamp), mean_value + std_value,
                     f'{mean_value+std_value:.2f}', ha='left', va='center')
            plt.text(max(timestamp), mean_value - std_value,
                     f'{mean_value-std_value:.2f}', ha='left', va='center')

            plt.title('{}-{}'.format(test, color_index))
            plt.xlabel('Tempo do experimento (s)')
            plt.ylabel('Tempo até conexão (ms)')
            plt.legend(loc='upper right', bbox_to_anchor=(
                1.0, 1.0), fontsize='6')
            
            # Salvar o gráfico na pasta 'conexões'
            nome_grafico = 'graph_connections_{}-{}.png'.format(test, color_index)
            caminho_grafico = os.path.join(pasta_conexoes, nome_grafico)
            plt.savefig(caminho_grafico)
            plt.clf()

