


import tkinter as tk
from tkinter import ttk



def alterar():
    
    # escolheu o tipo de dado


    tipo_dado_ = tipo_dado.get()
    opcao  =  caixa.get()


    if tipo_dado_ == 'C' and opcao == 'C -> k': 


        x =  int(dado_usuario.get())
        f = (x + 273)
        mostrar.config(text = f)
    elif tipo_dado_ == 'C' and opcao == 'C -> F':
        x =  int(dado_usuario.get())
        f = (x * 1.8) + 32
        f  =  float(f)
        mostrar.config(text = f)


    elif tipo_dado_ == 'K' and opcao == 'C -> F':
        x =  int(dado_usuario.get())
        f = (x * 1.8) + 32
        f  =  float(f)
        mostrar.config(text = f)







janela =  tk.Tk()


janela.geometry('400x600')


text = tk.Label(janela, text = 'ALTERAÇÃO DE DADO')
text.pack()


lista_tipo = ['C', 'F', 'K']


tipo_dado =  ttk.Combobox(janela,values =  lista_tipo )
tipo_dado.pack(pady = 10)


dado_usuario =  tk.Entry(janela)
dado_usuario.pack()



lista  =  ['C -> k', 'C -> F', 'K -> C', 'K -> F', 'F ->C','F-> K' ]


caixa  = ttk.Combobox(janela,values =  lista )
caixa.pack(pady = 10)



bt_ =  tk.Button(janela, text = 'calcular',command =  alterar)
bt_.pack()



mostrar =  tk.Label(janela, text = ' ')
mostrar.pack()








janela.mainloop()