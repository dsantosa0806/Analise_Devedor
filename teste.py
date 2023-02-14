from datetime import datetime, date

import pandas as pd
table = pd.read_excel('tables/devedor.xlsx')
# print(table.columns)
# Atribuindo dados para variáveis
table = pd.read_excel('tables/devedor.xlsx')

# Atribuindo dados para variáveis
for i, devedor in enumerate(table['Devedor']):
    qtde_aits_prevista  = int(table.loc[i,'Qtde'])

    # print(devedor,qtde_aits_prevista)


numero = '2.637,52'
numero = float(numero.replace('.','').replace(',','.'))


ano_atual = int(date.today().strftime("%Y"))
ano_devedor = 1993

print(ano_atual - ano_devedor)