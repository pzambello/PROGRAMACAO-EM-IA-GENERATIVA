


import sqlite3
import pandas as pd
import streamlit as st


dados =  pd.read_excel('dados_2.xlsx')
df  =  pd.DataFrame(dados, index = None)




arquivo_DB = sqlite3.connect('nome_banco.db')
cursor =  arquivo_DB.cursor()


cursor.execute('''


        CREATE TABLE IF NOT EXISTS dados(
         
             vendas REAL,
             vendedor TEXT             
        
        
        )
''')




# x = float(df['vendas'][0])
# y = df['vendedor'][0]


# print(dados['vendas'])
# print(dados['vendedor'])


nome1 =  st.text_input('Nome 1: ')
venda1 = st.number_input('Venda 1')


nome2 =  st.text_input('Nome 2: ')
venda2 = st.number_input('Venda 2')



nome3 =  st.text_input('Nome 3: ')
venda3 = st.number_input('Venda 3')



if st.button('INSERIR NO BANCO DE DADOS'):


    cursor.execute('INSERT INTO dados VALUES(?,?)',(venda1,nome1 ))
    cursor.execute('INSERT INTO dados VALUES(?,?)',(venda2,nome2 ))
    cursor.execute('INSERT INTO dados VALUES(?,?)',(venda3,nome3 ))


    arquivo_DB.commit()



