import customtkinter as ctk
from tkinter import messagebox

# Configuração do CustomTkinter para o tema escuro
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

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

# Janela Principal (Fundo Preto / Muito escuro)
janela = ctk.CTk()
janela.geometry('440x600')
janela.title('Sistema Escola XYZ')
janela.resizable(False, False)
janela.configure(fg_color='#0b0f19')  # Fundo preto/azulado bem escuro

# Título Principal com efeito de destaque
titulo = ctk.CTkLabel(
    janela, 
    text='SISTEMA ESCOLA XYZ', 
    font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
    text_color='#ffffff'
)
titulo.pack(pady=(25, 15))

# Painel Central (Card com efeito 3D simulado por bordas e fundo contrastante)
card = ctk.CTkFrame(
    janela, 
    fg_color='#121824',          # Fundo do card ligeiramente mais claro que a janela
    corner_radius=20,            # Bordas BEM arredondadas
    border_width=2,              # Largura da borda
    border_color='#00d2ff'       # Borda azul brilhante (efeito 3D/neon)
)
card.pack(pady=5, padx=25, fill="both", expand=True)

# Frame interno para organizar os campos dentro do card
frame_form = ctk.CTkFrame(card, fg_color="transparent")
frame_form.pack(pady=20, padx=20, fill="both", expand=True)

# Estilo padrão para os inputs (Bordas azuis arredondadas e letras brancas)
def criar_entrada(master, placeholder):
    return ctk.CTkEntry(
        master, 
        placeholder_text=placeholder, 
        placeholder_text_color='#888888',
        height=40, 
        corner_radius=12,         # Bem arredondado
        border_width=1.5,
        border_color='#0077ff',   # Borda azul
        fg_color='#1a2233',       # Fundo interno do input escuro
        text_color='#ffffff'      # Letras brancas
    )

def criar_label(master, texto):
    return ctk.CTkLabel(
        master, 
        text=texto, 
        font=ctk.CTkFont(family="Arial", size=12, weight="bold"), 
        text_color='#ffffff',     # Letras brancas
        anchor="w"
    )

# Nome
criar_label(frame_form, 'Nome do Aluno:').pack(fill="x", pady=(0, 2))
nome = criar_entrada(frame_form, "Digite o nome...")
nome.pack(fill="x", pady=(0, 10))

# Nota 1
criar_label(frame_form, 'Nota 1:').pack(fill="x", pady=(0, 2))
nota1 = criar_entrada(frame_form, "Ex: 7.5")
nota1.pack(fill="x", pady=(0, 10))

# Nota 2
criar_label(frame_form, 'Nota 2:').pack(fill="x", pady=(0, 2))
nota2 = criar_entrada(frame_form, "Ex: 8.0")
nota2.pack(fill="x", pady=(0, 10))

# Nota 3
criar_label(frame_form, 'Nota 3:').pack(fill="x", pady=(0, 2))
nota3 = criar_entrada(frame_form, "Ex: 6.5")
nota3.pack(fill="x", pady=(0, 15))

# Botão Calcular com Efeito 3D (Cores vibrantes, cantos super arredondados e relevo)
botao = ctk.CTkButton(
    card, 
    text='CALCULAR MÉDIA', 
    font=ctk.CTkFont(family="Arial", size=14, weight="bold"), 
    height=45, 
    corner_radius=16,             # Cantos bem arredondados
    fg_color='#0077ff',           # Azul principal
    hover_color='#005bb5',        # Azul mais escuro ao passar o mouse
    text_color='#ffffff',         # Letras brancas
    command=calcular_media
)
botao.pack(pady=(0, 15), padx=20, fill="x")

# Resultados (Letras brancas)
resultado = ctk.CTkLabel(
    card, 
    text='', 
    font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
    text_color='#ffffff'
)
resultado.pack(pady=(0, 5))

situacao = ctk.CTkLabel(
    card, 
    text='', 
    font=ctk.CTkFont(family="Arial", size=13, weight="bold")
)
situacao.pack(pady=(0, 10))

janela.mainloop()