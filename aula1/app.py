


acesso = input('Deseja acessar o sistema? s/n  -- ')
while acesso == 'S':

    print('SISTEMA ESCOLA XYZ')
    nome=input('nome aluno 😊 >> ')
    nota_1 = float(input('nota aluno 1 >> '))
    nota_2 = float(input('nota aluno 2 >> '))
    nota_3 = float(input('nota aluno 3 >> '))

    lista=[]
    lista.append(nota_1)
    lista.append(nota_2)
    lista.append(nota_3)


    media = sum(lista)/len(lista)

    print('O aluno ', nome, 'possui a média ', media)

    if media >= 6:
        print(f"o {nome}  Passou de ano 👍")
    elif media >= 5 and media <6:
        print(f"o {nome}  Está de recuperação 🤦‍♂️")
    else:
        print(f"o {nome}  Nao passou de ano 😢")
    acesso = input('Deseja continuar ? s/n >> ')
print('até logo')
input('clique enter para sair...')
    # FFF
    # FF
