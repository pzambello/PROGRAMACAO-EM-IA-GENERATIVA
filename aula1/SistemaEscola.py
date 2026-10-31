import tkinter as tk
def calcular_media():
    nota11 = float(nota1.get())
    nota22 = float(nota2.get())
    nota33 = float(nota3.get())
    media = (nota11 + nota22 + nota33)/3 
    resultado.config(text = media)

    nome_ = nome.get()

    if media >= 7:
        situacao.config(text = f'{nome_} VOCÊ PASSOU DIRETO 👍')
    elif media >=5 and media < 7:
        situacao.config(text = f'{nome_} VOCÊ ESTÁ EM RECUPERAÇÃO')
    else:
        situacao.config(text = f'{nome_} VOCÊ NÃO PASSOU ...')    

janela = tk.Tk()
janela.geometry('500x500')
titulo = tk.Label(janela, text='SISTEMA ESCOLA XYZ')
titulo.pack()

nome_titulo = tk.Label(janela, text = 'Nome: ')
nome_titulo.pack()
nome = tk.Entry(janela)
nome.pack()

nome_nota1 = tk.Label(janela, text = 'Nota 1: ')
nome_nota1.pack()

nota1 = tk.Entry(janela, text = 'Nota 1')
nota1.pack(pady = 5)

nome_nota2 = tk.Label(janela, text = 'Nota 2: ')
nome_nota2.pack()
nota2 = tk.Entry(janela, text = 'Nota 2')
nota2.pack(pady = 5)

nome_nota3 = tk.Label(janela, text = 'Nota 3: ')
nome_nota3.pack()
nota3 = tk.Entry(janela, text = 'Nota 3')
nota3.pack(pady = 5)


botao = tk.Button(janela, text = 'calcular', command = calcular_media)
botao.pack()

resultado  =  tk.Label(janela, text = ' ')
resultado.pack()

tk.Label(janela, text = 'Situação ').pack()
situacao = tk.Label(janela, text = ' ')

situacao.pack()


janela.mainloop()
