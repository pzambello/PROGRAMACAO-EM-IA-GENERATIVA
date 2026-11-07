# biblioteca para aleatoriedade
import random

# numero = random.randint(1,10)
# print(numero)
print('JOGO DA ALEATORIEDADE...')
print('GANHE ATÉ 5 K')
print('Escolha um número de 1 a 20  ')
numero_maquina = random.randint(1,20)

chances = 3
for x in range(3):
    print('Voce tem ', chances, ' chances ')
    numero_usuario = int(input('Escolha o seu número >> '))
    chances = chances - 1
    if numero_maquina == numero_usuario:
        print('Voce tem ' )
        print('VOCÊ GANHOU 5K !!')
    else:
        print('VOCÊ ERROU FEIO !!!')
        if chances == 0: 
            print('Maquina escolheu ' , numero_maquina)