import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

test = 'dec_2000_390_20'
base_filename = 'my5grantester_metrics_{}.csv'.format(test)
colors = ['red', 'blue', 'green', 'orange', 'purple', 'gray']
column_names = ['SM5G_PDU_SESSION_INACTIVE', 'MM5G_NULL', 'MM5G_DEREGISTERED', 'MM5G_REGISTERED_INITIATED', 'MM5G_REGISTERED', 'SM5G_PDU_SESSION_ACTIVE_PENDING']

for delay_ms in range(100, 101, 100):
    dados = pd.read_csv(base_filename.format(delay_ms))
    dados = dados.sort_values(by=dados.columns[0])

    for column_index, column_name in enumerate(column_names):
        ue_number = np.array([])
        column_data = np.array([])

        for indice, linha in dados.iterrows():
            ue_number = np.append(ue_number, linha['gnbid'])
            column_data = np.append(column_data, linha[column_name])

        # Plotar o gráfico da coluna atual
        plt.plot(ue_number, column_data, color=colors[column_index], label=column_name)

        # Calcular a média da coluna atual
        mean_value = np.nanmean(column_data)
        # Traçar linha reta com valor médio
        plt.axhline(y=mean_value, color=colors[column_index], linestyle='-', label="Média")
        plt.text(max(ue_number) + 55, mean_value, f'{mean_value:.2f}', ha='left', va='center')

        # Calcular o desvio padrão da coluna atual
        std_value = np.nanstd(column_data)
        # Traçar linha pontilhada com desvio padrão
        plt.axhline(y=mean_value + std_value, color=colors[column_index], linestyle='--', label="Desvio Padrão")
        plt.axhline(y=mean_value - std_value, color=colors[column_index], linestyle='--')
        plt.text(max(ue_number) + 55, mean_value + std_value, f'{mean_value+std_value:.2f}', ha='left', va='center')
        plt.text(max(ue_number) + 55, mean_value - std_value, f'{mean_value-std_value:.2f}', ha='left', va='center')

        # Configurar título e legendas do gráfico atual
        plt.title('{} - {}'.format(test, column_name))
        plt.xlabel('UE Number')
        plt.ylabel('Tempo de experimento (ms)')
        plt.legend()
        
        # Salvar o gráfico atual
        plt.savefig('graph_times_{}_{}.png'.format(test, column_name))
        plt.clf()