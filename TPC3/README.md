- TPC 3

Na aula do dia 2 de Outubro, foi atribuído um trabalho para casa: Criar um aplicação. Aqui está a minha resolução do mesmo.

Autora: Cláudia Isabel Ribeiro Teixeira (A110414)

![image_alt](https://github.com/ClaudiaTeixeiraa/ATP2025/blob/77557153f49b6a14713aa4e3b2b5c516b8586747/foto%20formal.jpg)

Segue o código criado para resolver o TPC:
```python

print("Seja bem-vind@ à nossa aplicação! Contamos com um menu que suprirá as suas necessidades.")

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

lista = []

while True:
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
      def cresce(lista):
        n = len(lista)
        for i in range(n-1):
          for j in range(0,n-i-1):
            if lista[j] > lista [j + 1]:
              lista[j],lista[j+1] = lista [j + 1],lista[j]
        return lista
      lista = cresce(lista)

      print(f"A tua lista por ordem crescente é {lista}")

     else:
      print("Ups parece que ainda não tens lista. Para que possas escolher a opção 7 deves antes passar pela 1 ou 2.")


  elif escolha == 8:
     if lista:
      def decresce(lista):
        n = len(lista)
        for i in range(n-1):
          for j in range(0,n-i-1):
            if lista[j] < lista [j + 1]:
              lista[j],lista[j+1] = lista [j + 1],lista[j]
        return lista
      lista = decresce(lista)
      print(f"A tua lista por ordem decrescente é {lista}")

     else:
      print("Ups parece que ainda não tens lista. Para que possas escolher a opção 8 deves antes passar pela 1 ou 2.")


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
    print("Tenha um bom dia. Adeusss")
    break

    ```
