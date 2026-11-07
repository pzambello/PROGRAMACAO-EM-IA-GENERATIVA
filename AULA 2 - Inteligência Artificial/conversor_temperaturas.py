import tkinter as tk
from tkinter import ttk



def salvar_selecao1():
    # .get() busca o valor atual selecionado no Combo
    valor_selecionado1 = combo.get()
    
    # Guarda o valor na variável global ou faz o que precisar com ele
    print(f"Valor guardado com sucesso: {valor_selecionado1}")
    label_resultado1.config(text=f"Selecionado: {valor_selecionado1}")

def salvar_selecao2():
    # .get() busca o valor atual selecionado no Combo
    valor_selecionado2 = combo.get()
    
    # Guarda o valor na variável global ou faz o que precisar com ele
    print(f"Valor guardado com sucesso: {valor_selecionado2}")
    label_resultado2.config(text=f"Selecionado: {valor_selecionado2}")


def mostrar_selecao(event):
  print(f"Você selecionou Temperatura Original : {combo.get()}")

#print('CONVERSOR DE TEMPERATURA')
# Criando a janela principal
janela = tk.Tk()



janela.geometry("300x400")

tk.Label("SELECIONE TEMPERATURA ORIGINAL").pack()

optar_tipos_temp = ["Celsious", "Fahrenheit", "Kelvin"]

# Criando o Combobox
combo = ttk.Combobox(janela, values=optar_tipos_temp)
combo.set("SELECIONE TEMPERATURA ORIGINAL")  # Valor inicial exibido
combo.pack(padx=20, pady=40)

combo.bind("<<ComboboxSelected>>", mostrar_selecao)
# Botão para confirmar e guardar o valor
botao = tk.Button(janela, text="Guardar Valor", command=salvar_selecao1)
botao.pack(pady=5)


combo= ttk.Combobox(janela, values=optar_tipos_temp)
combo.set("SELECIONE TEMPERATURA FINAL")  # Valor inicial exibido
combo.pack(padx=20, pady=40)

combo.bind("<<ComboboxSelected>>", mostrar_selecao)


# Botão para confirmar e guardar o valor
botao2 = tk.Button(janela, text="Guardar Valor", command=salvar_selecao2)
botao2.pack(pady=5)

temp_origem = 0
temp_origem = tk.Entry(janela)
temp_origem.pack()

temp_convertido = 0

if valor_selecionado1 == 'Celsius':
    if valor_selecionado2 == 'Fahrenheit':
        temp_convertido = (temp_origem * (9/5)) + 32
    else:
         temp_convertido = temp_origem  + 273,15
if valor_selecionado1 == 'Fahrenheit':
    if valor_selecionado2 == 'Celsius':
        temp_convertido = (5/9) * (temp_origem - 32)
    else:
         temp_convertido = (5/9) * (temp_origem  - 32) + 273,15
if valor_selecionado1 == 'Kelvin':
    if valor_selecionado2 == 'Celsius':
        temp_convertido = temp_origem - 273,15
    else:
         temp_convertido = (9/5) * (temp_origem  - 273,15) + 32

  #  print('Temperatura em ' , valor_selecionado1 , ' de ', temp_origem , ' convertido em ', valor_selecionado2, ' é igual a ', temp_convertido)

label_resultado1 = tk.Label(janela, text="")
label_resultado1.pack(pady=20)

label_resultado2 = tk.Label(janela, text="")
label_resultado2.pack(pady=20)


janela.mainloop()


