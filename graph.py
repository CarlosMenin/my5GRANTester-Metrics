import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dados = pd.read_csv("my5grantester_metrics_500.csv")
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
        
    
    cor = plt.scatter(timestamp,connections,label= "Tester {}".format(grupo.iloc[0,0])).get_facecolor()[0]
    valor_medio = np.mean(connections)
    
    # Traçar linha reta com valor médio
    plt.axhline(y=valor_medio,color=cor)
plt.title('500ms')
plt.xlabel('Tempo do experimento (s)')
plt.ylabel('Tempo até conexão (ms)')
plt.legend()        
plt.show()