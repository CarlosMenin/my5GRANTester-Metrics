import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

base_filename = 'my5grantester_metrics_{}.csv'
colors = ['red','blue','green','orange','purple','gray']
column_names = ['SM5G_PDU_SESSION_INACTIVE','MM5G_NULL','MM5G_DEREGISTERED','MM5G_REGISTERED_INITIATED','MM5G_REGISTERED','SM5G_PDU_SESSION_ACTIVE_PENDING']

for delay_ms in range(100,501,100):
    dados = pd.read_csv(base_filename.format(delay_ms))
    dados = dados.sort_values(by=dados.columns[0])

    for i in range(0, len(dados), 100):
        first_line = True
        ue_number = np.array([])
        arrays = [[] for _ in range(len(column_names))]

        for indice, linha in dados.iterrows():
            ue_number = np.append(ue_number,linha['gnbid'])
            for j in range(len(column_names)):
                arrays[j].append(linha[column_names[j]])
        arrays = [np.array(arr) for arr in arrays]
            
    # Plotar as linhas
    for j in range(0,len(column_names)):
        plt.plot(ue_number,arrays[j],color= colors[j],label= column_names[j])
        #valor_medio = np.mean(connections)
        
    # Traçar linha reta com valor médio
    for j in range(0,len(column_names)):
        mean = np.mean(arrays[j])
        plt.axhline(y=mean,color= colors[j])
    
    # Plot da linha pontilhada com o desvio padrão
    for j in range(0,len(column_names)):
        std = np.std(arrays[j])
        plt.axhline(y=std,color= colors[j],linestyle='--')

    # Configurar título e legendas
    plt.title('{}ms'.format(delay_ms))
    plt.xlabel('UE Number')
    plt.ylabel('Tempo de experimento (ms)')
    plt.legend()     
    plt.savefig('graph_times_{}ms.png'.format(delay_ms))
    plt.clf()