**TPC 3**
-
- Na aula do dia **9 de Outubro**, foi atribuído um trabalho para casa: **Aplicação para gerir um cinema**. Aqui está a minha resolução do mesmo.

Autora: Cláudia Isabel Ribeiro Teixeira **(A110414)**
- 
![image](https://github.com/ClaudiaTeixeiraa/ATP2025/blob/50853c9a0b9cb98c9196bc095d8ef1134162d2fd/foto%20formal.jpg)
-
**Notas de resolução**
-
- Como sugerido no enunciado, decidi criar 2 outras funções para a minha app.
    - **1ª opção**: Escolha 6 no menu
        - Ao selecionar esta opção, a pessoa tem a oportunidade de anular a compra de um bilhete que fez anteriormente.
    - **2ª opção**: Escolha 7 no menu
        - Ao selecionar esta opção, a pessoa tem acesso à ocupação da sala que selecionar, em percentagem.
- Às minhas salas iniciais, decidi adicionar mais 2 salas para além das que estão no enunciado:
    - sala3 = (140, [], "Jaws")
    - sala4 = (175, [], "LaLaLand")
- Nos meus "print" deixei muitos espaços para que a dar run ao programa ele fique bem organizado. Questão somente estética.

Resolução
-
- Aqui segue o código que criei para a aplicação:
```python
sala1 = (150, [], "Twilight")
sala2 = (200, [], "Hannibal")
sala3 = (140, [], "Jaws")
sala4 = (175, [], "LaLaLand")
cinema = [sala1,sala2,sala3,sala4]


def listar(cinema):
  print("""
  Neste momento temos os seguintes filmes em exibição: """)
  for sala in cinema:
    print("   -", sala[2])
  return


def disponivel(cinema,filme,lugar):
  for sala in cinema:
    if filme.lower() == sala[2].lower():
        if lugar in sala[1] or lugar > sala[0]:
          print("""      O lugar não está disponível""")
          return False 
        else:
          print("""      O lugar está disponível""")
          return True 

  print("""      Parece que o filme que inseriu não se encontra no nosso sistema. Tente novamente.""")
  return False 


def vendebilhete(cinema,filme,lugar):
  for sala in cinema:
    if filme.lower() == sala[2].lower() and lugar <= sala[0]:
      if lugar in sala[1]:
        print("      Infelizmente esse lugar já não está disponível.")
      else:
        sala[1].append(lugar)
        print("      O seu lugar foi reservado com sucesso. Obrigada pela preferência.")
      return


def listardisponibilidades(cinema):
  for sala in cinema:
    disponiveis = sala[0]-len(sala[1])
    print(f"""   
                
          - Para {sala[2]} temos {str(disponiveis)} lugares disponíveis.""")
  return


def inserirSala(cinema,sala):
  for sa in cinema:
      if filme.lower() == sa[2].lower():
        print("""      O filme que inseriu já se encontra numa das nossas salas.""")
        return
  cinema.append(sala)
  print(f"""      Sala com o filme '{sala[2]}' adicionada com sucesso!""")
  return "      Agora a lista de filmes disponíveis é:" + str(cinema)


def anularBilhete(cinema,sala,filme,lugar):
  for sala in cinema:
    if filme.lower() == sala[2].lower():
      if lugar in sala[1]:
        sala[1].remove(lugar)
        print("      O seu bilhete foi anulado. O seu reembolso acontecerá dentro de momentos.")
        return 
      print("      Parece que esse lugar não está marcado como ocupado. Verifique o seu bilhete novamente.")
      return


def ocupação(cinema,sala,filme):
  for sala in cinema:
    if filme.lower() == sala[2].lower(): 
      disponiveis = sala[0]-len(sala[1])
      percentagem = ((int(disponiveis) // int(sala[0]))*100)
      print(f"""      Para o filme que escolheu, a sala está {percentagem}% ocupada.""")
      return 

  print(f"""      Parece que o filme que escolheu não está no catálogo.""")
  return


print("Seja bem-vinda/o à nossa aplicação de gestão de cinemas!")

def menu():
  print("""
  Escolha a opção que melhor se adequa à ação que quer realizar:
      1. Listar os filmes no catálogo
      2. Verificar disponibilidade de lugar
      3. Comprar bilhete
      4. Listar disponibilidades
      5. Inserir nova sala
      6. Anular compra de bilhete
      7. Ocupação de sala
      8. Sair""")
  escolha = input("      Insira aqui a sua opção: ")
  return escolha


c = True
while c == True:
  escolha = menu()

  if escolha == "1":
    listar(cinema)


  elif escolha == "2":
    filme = str(input("""      
      Insira o nome do filme que quer ver:"""))
    lugar = int(input("""      Insira o lugar:"""))
    print(disponivel(cinema,filme,lugar))


  elif escolha == "3":
    print("""      As nossas salas estão organizadas por números. Cada sala tem um número limitado de lugares.""")
    filme = input("      Insira o nome do filme que quer ver: ")
    lugar = int(input("      Insira o lugar que quer: "))
    print(vendebilhete(cinema,filme,lugar))


  elif escolha == "4":
    print(listardisponibilidades(cinema))
  

  elif escolha == "5":
    filme = str(input("""      Qual filme quer inserir? """))
    lugar = int(input("""      Quantos lugares quer que a sala tenha? """))
    sala = (lugar,[],filme)
    print(inserirSala(cinema,sala))

  
  elif escolha == "6":
    filme = str(input("      Insira o filme para o qual quer anular o seu bilhete: "))
    lugar = int(input("      Insira o lugar que quer anular na sala: "))
    print(anularBilhete(cinema,sala,filme,lugar))


  elif escolha == "7":
    filme = str(input("      Insira o filme: "))
    ocupação(cinema,sala,filme)
    

  elif escolha == "8":
    c = False
    print("""      
      Obrigada pela preferência! Tenha um bom dia.""")
```
