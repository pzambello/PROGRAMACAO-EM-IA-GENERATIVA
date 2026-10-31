import customtkinter as ctk
from tkinter import messagebox

# Configuração inicial do tema do CustomTkinter
ctk.set_appearance_mode("System")  # Segue o tema do sistema ("System", "Dark" ou "Light")
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

def calcular_media():
    try:
        # Pega os valores e converte para float (substituindo vírgula por ponto)
        n1 = float(nota1.get().replace(',', '.'))
        n2 = float(nota2.get().replace(',', '.'))
        n3 = float(nota3.get().replace(',', '.'))
        nome_ = nome.get().strip()
        
        if not nome_:
            nome_ = "Aluno(a)"

        media = (n1 + n2 + n3) / 3 
        resultado.configure(text=f"Média Final: {media:.2f}")

        # Define as cores baseadas no resultado
        if media >= 7:
            situacao.configure(text=f'{nome_}, VOCÊ PASSOU DIRETO! 👍', text_color='#2ecc71') # Verde
        elif 5 <= media < 7:
            situacao.configure(text=f'{nome_}, VOCÊ ESTÁ EM RECUPERAÇÃO ⚠️', text_color='#f39c12') # Amarelo/Laranja
        else:
            situacao.configure(text=f'{nome_}, VOCÊ NÃO PASSOU... ❌', text_color='#e74c3c') # Vermelho
            
    except ValueError:
        messagebox.showerror("Erro de Entrada", "Por favor, preencha todos os campos com números válidos nas notas!")

# Janela Principal
janela = ctk.CTk()
janela.geometry('420x580')
janela.title('Sistema Escola XYZ')
janela.resizable(False, False)

# Título Principal
titulo = ctk.CTkLabel(janela, text='SISTEMA ESCOLA XYZ', font=ctk.CTkFont(family="Arial", size=20, weight="bold"))
titulo.pack(pady=(25, 15))

# Frame do Formulário para centralizar os campos
frame_form = ctk.CTkFrame(janela, fg_color="transparent")
frame_form.pack(pady=5, padx=30, fill="x")

# Nome
lbl_nome = ctk.CTkLabel(frame_form, text='Nome do Aluno:', font=ctk.CTkFont(family="Arial", size=12, weight="bold"), anchor="w")
lbl_nome.pack(fill="x", pady=(0, 2))
nome = ctk.CTkEntry(frame_form, placeholder_text="Digite o nome...", height=38, corner_radius=8)
nome.pack(fill="x", pady=(0, 12))

# Nota 1
lbl_n1 = ctk.CTkLabel(frame_form, text='Nota 1:', font=ctk.CTkFont(family="Arial", size=12, weight="bold"), anchor="w")
lbl_n1.pack(fill="x", pady=(0, 2))
nota1 = ctk.CTkEntry(frame_form, placeholder_text="Ex: 7.5", height=38, corner_radius=8)
nota1.pack(fill="x", pady=(0, 12))

# Nota 2
lbl_n2 = ctk.CTkLabel(frame_form, text='Nota 2:', font=ctk.CTkFont(family="Arial", size=12, weight="bold"), anchor="w")
lbl_n2.pack(fill="x", pady=(0, 2))
nota2 = ctk.CTkEntry(frame_form, placeholder_text="Ex: 8.0", height=38, corner_radius=8)
nota2.pack(fill="x", pady=(0, 12))

# Nota 3
lbl_n3 = ctk.CTkLabel(frame_form, text='Nota 3:', font=ctk.CTkFont(family="Arial", size=12, weight="bold"), anchor="w")
lbl_n3.pack(fill="x", pady=(0, 2))
nota3 = ctk.CTkEntry(frame_form, placeholder_text="Ex: 6.5", height=38, corner_radius=8)
nota3.pack(fill="x", pady=(0, 15))

# Botão Calcular
botao = ctk.CTkButton(janela, text='Calcular Média', font=ctk.CTkFont(family="Arial", size=14, weight="bold"), 
                      height=42, corner_radius=8, command=calcular_media)
botao.pack(pady=10, padx=30, fill="x")

# Resultado da Média
resultado = ctk.CTkLabel(janela, text='', font=ctk.CTkFont(family="Arial", size=14, weight="bold"))
resultado.pack(pady=(10, 2))

# Situação do Aluno
situacao = ctk.CTkLabel(janela, text='', font=ctk.CTkFont(family="Arial", size=13, weight="bold"))
situacao.pack(pady=2)

janela.mainloop()