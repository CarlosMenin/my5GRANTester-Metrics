import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

test = 'dec_2000_390_20'
base_filename = 'my5grantester_metrics_{}.csv'.format(test)
for delay_ms in range(100,101,100):
    dados = pd.read_csv(base_filename.format(delay_ms))
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


    plt.title('{}ms'.format(test))
    plt.xlabel('Tempo do experimento (s)')
    plt.ylabel('Tempo até conexão (ms)')
    plt.legend()        
    plt.savefig('graph_all_connections_{}.png'.format(test))
    plt.clf()