import customtkinter as ctk
from tkinter import messagebox


# Força o modo escuro para garantir o fundo preto
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def calcular_media():
    try:
        # Validação e conversão das notas
        nota_1 = float(nota1.get())
        nota_2 = float(nota2.get())
        nota_3 = float(nota3.get())
        nome_ = nome.get().strip()
        
        if not nome_:
            messagebox.showwarning("Aviso", "Por favor, digite o nome do aluno(a).")
            return


        media = (nota_1 + nota_2 + nota_3) / 3
        resultado.configure(text=f"Média Final: {media:.2f}")


        # Lógica de aprovação com cores dinâmicas
        if media >= 7.0:
            situacao.configure(text=f'O aluno(a) {nome_} PASSOU DIRETO!', text_color='#2ecc71')
        elif 5.0 <= media < 7.0:
            situacao.configure(text=f'O aluno(a) {nome_} ESTÁ EM RECUPERAÇÃO.', text_color='#f39c12')
        else:
            situacao.configure(text=f'O aluno(a) {nome_} NÃO PASSOU...', text_color='#e74c3c')
            
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira apenas números válidos nas notas.")


# Janela Principal com fundo preto absoluto
janela = ctk.CTk()
janela.title("Sistema Escola XYZ")
janela.geometry('430x700')
janela.resizable(False, False)
janela.configure(fg_color='#000000')


# Cores do tema personalizado
COR_AZUL = '#00d2ff'
COR_AZUL_HOVER = '#009abf'
COR_CONTAINER = '#111111'


# --- Título ---
titulo = ctk.CTkLabel(
    janela, 
    text='SISTEMA ESCOLA XYZ', 
    font=ctk.CTkFont(family='Arial', size=18, weight='bold'),
    text_color=COR_AZUL
)
titulo.pack(pady=20)


# --- Frame do Formulário ---
frame_form = ctk.CTkFrame(janela, corner_radius=12, fg_color=COR_CONTAINER)
frame_form.pack(padx=20, pady=5, fill='x', ipady=10)


def criar_campo(master, texto):
    lbl = ctk.CTkLabel(master, text=texto, font=ctk.CTkFont(family='Arial', size=12, weight='bold'), text_color='#ffffff')
    lbl.pack(anchor='w', padx=20, pady=(10, 2))
    
    entry = ctk.CTkEntry(
        master, 
        font=ctk.CTkFont(family='Arial', size=12), 
        width=350, 
        height=38, 
        corner_radius=8,
        fg_color='#1a1a1a',
        text_color='#ffffff',
        border_color=COR_AZUL
    )
    entry.pack(padx=20, pady=(0, 5))
    return entry


nome = criar_campo(frame_form, 'Nome do Aluno(a):')
nota1 = criar_campo(frame_form, 'Nota 1:')
nota2 = criar_campo(frame_form, 'Nota 2:')
nota3 = criar_campo(frame_form, 'Nota 3:')


# --- Botão Calcular ---
botao = ctk.CTkButton(
    janela, 
    text='CALCULAR MÉDIA', 
    font=ctk.CTkFont(family='Arial', size=13, weight='bold'),
    height=42,
    corner_radius=8,
    fg_color=COR_AZUL,
    hover_color=COR_AZUL_HOVER,
    text_color='#000000',
    command=calcular_media
)
botao.pack(padx=20, pady=20, fill='x')


# --- Área de Resultados ---
frame_resultado = ctk.CTkFrame(janela, corner_radius=12, fg_color="transparent")
frame_resultado.pack(padx=20, pady=5, fill='x')


resultado = ctk.CTkLabel(frame_resultado, text='', font=ctk.CTkFont(family='Arial', size=14, weight='bold'), text_color='#ffffff')
resultado.pack(pady=2)


situacao = ctk.CTkLabel(frame_resultado, text='', font=ctk.CTkFont(family='Arial', size=13, weight='bold'))
situacao.pack(pady=5)


janela.mainloop()