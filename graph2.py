import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pasta = os.getcwd()  # Obtém a pasta de trabalho atual

column_names = ['MM5G_REGISTERED_INITIATED',
                'MM5G_REGISTERED', 'SM5G_PDU_SESSION_ACTIVE_PENDING']
colors = ['green', 'orange', 'red']

for arquivo in os.listdir(pasta):
    if arquivo.endswith(".csv"):
        nome_arquivo = os.path.splitext(arquivo)[0]
        teste = nome_arquivo.split("_")[2]

        base_filename = os.path.join(pasta, arquivo)

        dados = pd.read_csv(base_filename)
        dados = dados.sort_values(by=dados.columns[0])

        fig, ax = plt.subplots()  # Cria uma nova figura e eixo para cada iteração do loop

        stacked_data = np.zeros(len(dados))

        for column_index, column_name in enumerate(column_names):
            column_data = np.array(dados[column_name])
            diff_column_data = column_data - stacked_data

            ax.fill_between(dados['gnbid'], stacked_data, stacked_data + diff_column_data,
                            label='{}'.format(column_name), color=colors[column_index], alpha=1.0)

            stacked_data += diff_column_data

        ax.set_title('{}'.format(teste))
        ax.set_xlabel('UE Number')
        ax.set_ylabel('Tempo de experimento (ms)')
        ax.legend(loc='upper left', bbox_to_anchor=(0, 1.0), fontsize='6')

        fig.savefig('graph_times_{}.png'.format(
            teste,), dpi=300)
        plt.close(fig)
