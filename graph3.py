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

        for i in range(0, len(dados), 100):
            first_line = True
            timestamp = np.array([])
            connections = np.array([])
            grupo = dados.iloc[i:i+100].copy()

            for indice, linha in grupo.iterrows():
                if first_line:
                    timestamp_base = linha['timestamp']
                    first_line= False
                
                timestamp = np.append(timestamp,(linha['timestamp']-timestamp_base)/1000000000)
                connections = np.append(connections,linha['SM5G_PDU_SESSION_ACTIVE_PENDING'])
                
            
            cor = plt.scatter(timestamp, connections, label="Tester {}".format(grupo.iloc[0, 0]), s=2).get_facecolor()[0]


        plt.title('{}'.format(teste))
        plt.xlabel('Tempo do experimento (s)')
        plt.ylabel('Tempo até conexão (ms)')
        plt.legend()        
        plt.savefig('graph_all_connections_{}.png'.format(teste))
        plt.clf()