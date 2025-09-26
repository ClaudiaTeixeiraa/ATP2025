- **TPC 2**
  
- Na aula do dia **22 de Setembro**, foi atribuído um trabalho para casa: O Jogo dos Fósforos. Aqui está a minha resolução do mesmo (incluindo os dois níveis do jogo). 
- **Autor:** Cláudia Isabel Ribeiro Teixeira (**A110414**)
-  ![image_alt](https://github.com/ClaudiaTeixeiraa/ATP2025/blob/ffd0a10a1c1303a2a439cda594d9faebdf964e2a/foto%20formal%20(2).jpg)

-  Resolução do "**Jogo dos fósforos**" incluindo o Nível 1 e o Nível 2:
-  Fiz ambos os níveis no mesmo ficheiro Python através de uma *if clause* que depende do jogador que a pessoa a jogar escolher.
-  Insiro aqui  o código sem ser por print, caso queira testar:
 ```python
print("Olá! Vamos jogar o jogo dos 21 fósforos. O jogo baseia-se na subtração de números (1, 2, 3 ou 4) ao número 21 alternadamente.")
print("Quem for a pessoa a substrair o último 1, perde.")

def jogo():
    jogador = input ("Preferes ser o primeiro a jogar (jogador 1) ou o segundo (jogador 2)? ")
    if jogador.lower() == "jogador 1":
        números = [1, 2, 3, 4]
        print("OK! Tu podes começar.")
        fósforos = 21
        while fósforos > 1: 
            while True: 
                try:
                    primeiro = int(input("Escolhe um número: "))
                    if primeiro in números:
                        break #Este break autoriza o jogo a prosseguir ao acabar com este while loop
                    else:
                        print("Esse número não está na lista. Escolhe um número entre 1 e 4.")
                except ValueError:
                        print("Ups. Parece que essa resposta é inválida.")
                        primeiro = int((input("Escolhe um número: ")))
                #Este try e except ValueError servem para invalidar dados que não sejam números como queremos

            fósforos = fósforos - primeiro
            print(f"Sobram agora {fósforos} fósforos.")

            if primeiro == 1:
                escolha = 4
            elif primeiro == 2:
                escolha = 3
            elif primeiro == 3:
                escolha = 2
            else:
                escolha = números[0]
            #Este números[0] indica a posição do número que temos na lista números. Neste caso, na posição 0 temos o número 1
            #Poderia só ter escrito "escolha = 1" como está acima. Só fiz de duas maneiras diferentes para me lembrar que posso fazê-lo
            print(f"Agora é a minha vez! Eu escolho o número {escolha}.")
            fósforos = fósforos - (escolha)
            print(f"Boa! Com as nossas escolhas agora temos {str(fósforos)}.")
        if fósforos <= 1:
            print("Parece que já temos um perdedor haha.")
            print("Como tens de retirar o último fósforo, perdeste. Talvez da próxima vez consigas entender o padrão.")
                

    elif jogador.lower() == "jogador 2":
        print("Tudo bem, então eu começo. Vamos lá!")
        números = [1, 2, 3, 4]
        fósforos = 21
        while fósforos > 1:
            import random
            aleatório = random.choice(números)
            fósforos = fósforos - aleatório
            print(f"Eu escolho o número {aleatório}. Sobram {fósforos} fósforos. Agora é a tua vez.")

            while True:
                try:
                    segundo = int(input("Insere um número: "))
                    if segundo in números:
                        break
                    else: 
                        print("Só podes escolher números entre 1 e 4. Tenta de novo.")
                except ValueError:
                        print("Ups. Parece que essa resposta é inválida.")
                        segundo = int(input("Escolhe um número: "))

            fósforos = fósforos - segundo
            print (f"Okk. Sobram {fósforos} fósforos.")

        if fósforos <= 1:
            print("Parece que já temos um perdedor haha.")
            print("O jogo acabou. Talvez possamos jogar de novo.")
        
    else:
        print("Infelizmente, essa resposta não é válida. Tenta novamente.")
        
    return 

while True:
    jogo()
    resposta = input("Queres jogar de novo (sim / não)? ")
    if resposta.lower() != "sim":
        print("Foi divertido. Talvez joguemos mais para a próxima. Adeusss")
        break
```
- Ainda, os prints retirados do ficheiro que criei no VSCode:
-  ![image_alt](https://github.com/ClaudiaTeixeiraa/ATP2025/blob/bf3fa0cbc4780fadb854e1741ab79fef8a25917d/Resolu%C3%A7%C3%A3oDoJogoDosF%C3%B3sforospt1.png)
-  ![image_alt](https://github.com/ClaudiaTeixeiraa/ATP2025/blob/4c0bdfc99817ce51843255148a64dad4660cddab/Resolu%C3%A7%C3%A3oDoJogoDosF%C3%B3sforospt2.png)
-  ![image_alt](https://github.com/ClaudiaTeixeiraa/ATP2025/blob/521702f4cd69315197156593f12109bf537209e0/Resolu%C3%A7%C3%A3oDoJogoDosF%C3%B3sforospt3.png)



