Ao resolver o TPC 3: **Aplicação para manipulação de listas de inteiros**, nas opções 7 e 8 acabei por fazer algo alterado relativamente ao que a indicação pedia. O suposto era dizer somente se a lista estava em ordem crescente ou decrescente. No entanto, resolvi de outra forma, ao escolher a opção 7, o meu código devolve a lista já em ordem crescente e na opção 8, em decrescente. Para evitar atualizar a ultima edição do meu ficheiro README e comprovar que fiz o TPC a tempo, decidi criar este outro ficheiro para colocar o código como pedido no exercício. Como acredito que a minha primeira resolução é também válida e útil, decidi não alterar o ficheiro README inicial. 

Segue o código a seguir exatamente a indicação do enunciado: 
```python
print("Seja bem-vinda/o à minha aplicação! Aqui está o menu com as opções de ação que quer realizar.")

def menu():
  print("""
    Menu:
    (1) Criar Lista
    (2) Ler Lista
    (3) Soma
    (4) Média
    (5) Maior
    (6) Menor
    (7) Ordenada por ordem crescente
    (8) Ordenada por ordem decrescente
    (9) Procura um elemento
    (0) Sair""")
  escolha = int(input("Insira o número da ação que quer realizar: "))
  return escolha

c = True
lista = []
while c == True:
  escolha = menu()

  if escolha == 1:
    import random
    tamanho = random.randint(2, 50) #Escolhi que no máximo a lista terá 15 elementos e no mínimo 2
    lista = [random.randint(1, 100) for _ in range(tamanho)]
    print(f"Ok, aqui vai a sua lista criada aleatoriamente: {lista}")


  elif escolha == 2:
    lista = []
    N = int(input("Quantos números quer na sua lista? "))
    i = 0
    while i < N:
      num = int(input("Insira o número: "))
      i = i + 1
      lista.append(num)
    print(f"Ok, aqui vai a sua lista: {lista}")


  elif escolha == 3:
    soma = 0
    if lista:
      def soma(lista):
        soma = 0
        for elem in lista:
            soma = elem + soma
        return soma
      print(f"A soma dos elementos da tua lista é: {soma(lista)}")

    else:
      print("Ups parece que ainda não tens lista. Para que possas escolher a opção 3 deves antes passar pela 1 ou 2.")


  elif escolha == 4:
    if lista:
      def media(lista):
        soma = 0
        for elem in lista:
            soma = elem + soma
        med = soma / len(lista)
        return med
      print(f"A média dos elementos da tua lista é: {media(lista)}")

    else:
      print("Ups parece que ainda não tens lista. Para que possas escolher a opção 4 deves antes passar pela 1 ou 2.")


  elif escolha == 5:
     if lista:
      def maior(lista):
        l = lista[0]
        for i in lista[1:]:
            if i > l:
                l = i
        return l
      print(f"O maior dos elementos da tua lista é: {maior(lista)}")

     else:
      print("Ups parece que ainda não tens lista. Para que possas escolher a opção 5 deves antes passar pela 1 ou 2.")


  elif escolha == 6:
     if lista:
      def menor(lista):
        l = lista[0]
        for i in lista[1:]:
            if i < l:
                l = i
        return l
      print(f"O menor dos elementos da tua lista é: {menor(lista)}")

     else:
      print("Ups parece que ainda não tens lista. Para que possas escolher a opção 6 deves antes passar pela 1 ou 2.")


  elif escolha == 7:
     if lista:
        crescente = True 
        i = 0
        while i < (len(lista)-1):
          if lista [i] > lista [i+1]:
            crescente = False
          i = i + 1

        if crescente:
            print("A tua lista está em ordem crescente.")
        else:
            print("A tua lista não está em ordem crescente.")
        
     else:
      print("Ups parece que ainda não tens lista. Para que possas escolher a opção 7 deves antes passar pela 1 ou 2.")



  elif escolha == 8:
      if lista:
        decrescente = True 
        i = 0
        while i < (len(lista)-1):
          if lista [i] < lista [i+1]:
            decrescente = False
          i = i + 1

        if decrescente:
            print("A tua lista está em ordem decrescente.")
        else:
            print("A tua lista não está em ordem decrescente.")
        
      else:
        print("Ups parece que ainda não tens lista. Para que possas escolher a opção 7 deves antes passar pela 1 ou 2.")


  elif escolha == 9:
     if lista:
      elem = int(input("Qual é o caracter que queres procurar? "))
      if elem in lista:
        posição = lista.index(elem)
        print(f"O número que inseriste encontra-se na posição {posição} ")

      else:
        print("-1")

     else:
      print("Ups parece que ainda não tens lista. Para que possas escolher a opção 9 deves antes passar pela 1 ou 2.")


  elif escolha == 0:
    c = False
    print("Tenha um bom dia. Adeusss")

```
