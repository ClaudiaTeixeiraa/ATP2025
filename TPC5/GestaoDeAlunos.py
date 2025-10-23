print("""Seja bem-vinda/o à nossa aplicação de gestão de alunos.No nosso menu terá acesso às ações que pode realizar.""" )

turma = []


def criarTurma():
    print(f"""     Ao selecionar esta opção, criou automaticamente a sua turma.""")
    turma.clear()
    return
    

def adicionar(turma):
    numero = int(input("""     Quantos alunos quer adicionar? """))

    for i in range(numero):
        nome = input("""     Insira o nome da/o aluna/o: """)
        id = int(input("""     Insira o ID da/o aluna/o (Ex:12345): """))

        idsEscolhidos = [aluno[1] for aluno in turma]
        while id not in range(10000,100000) or id in idsEscolhidos:
            print("O ID não é válido. Verifique se ele segue o formato pedido (Ex:12345) e se não está a inserir um ID que já se encontra na nossa plataforma.")
            id = int(input("""     Insira o ID da/o aluna/o (Ex:12345): """))    
        
        idsEscolhidos.append(id)
        notaTPC = float(input("""     Insira a nota de TPC: """))
        while notaTPC < 0 or notaTPC > 20:
            print("A nota de de TPC não é válida (0-20)(Ex: 11.1)")
            notaTPC = float(input("""     Insira a nota de TPC: """))
        
        notaProj = float(input("""     Insira a nota de projeto: """))
        while notaProj < 0 or notaProj > 20:
            print("A nota de projeto não é válida (0-20)(Ex: 11.1)")
            notaProj = float(input("""     Insira a nota de projeto: """))
        
        notaTeste = float(input("""     Insira a nota ao teste: """))
        while notaTeste < 0 or notaTeste > 20:
            print("A nota de teste não é válida (0-20)(Ex: 11.1)")
            notaTeste = float(input("""     Insira a nota ao teste: """))
        
        print("""     Obrigada! Iremos agora processar os dados inseridos.""")
        aluno = [nome, id, [notaTPC, notaProj, notaTeste]]
        turma.append(aluno)
                    
    return 


def listar(turma):
    print("""     Neste momento a nossa turma encontra-se da seguinte maneira: """)
    print("""     NOME     /    ID    /  NOTAS""")
    for aluno in turma:
        print(f"   -{aluno}")
    return


def consultar(turma):
    idEsc = int(input("""     Qual é o ID do aluno que quer procurar? """))
    encontrado = False
    for aluno in turma:
        if idEsc == aluno[1]:
            print(f"""     O aluno que escolheu tem os seguintes dados na nossa plataforma:
        Nome: {aluno[0]}
        Id: {aluno[1]}
        Nota de TPC's: {aluno[2][0]}
        Nota de Projeto: {aluno[2][1]}
        Nota de Teste: {aluno[2][2]}""")
            encontrado = True    

    if not encontrado:
        print("""     O ID que inseriu não se encontra na nossa plataforma de gestão. Verfifique se escreveu o ID correto (Ex: 12345)""")
    return


def menu():
    print("""     
     No menu de operações abaixo selecione a opção que quer selecionar:
    - 1: Criar uma turma;
    - 2: Inserir um aluno na turma;
    - 3: Listar a turma;
    - 4: Consultar um aluno por id;
    - 5: Guardar a turma em ficheiro;
    - 6: Carregar uma turma dum ficheiro;
    - 0: Sair da aplicação""")
    escolha = int(input("""     Insira o número correspondente à sua opção: """))
    return escolha

c = True
while c == True:
    escolha = menu()

    if escolha == 1:
        criarTurma()

    elif escolha == 2:
        adicionar(turma)
        print(f"""     A turma é composta por {len(turma)} aluno(s). 
        Turma: {turma}
""")
        
    elif escolha == 3:
        listar(turma)
    

    elif escolha == 4:
        consultar(turma)

    elif escolha == 5:
        with open("./BasedeTurmas/Turma.txt","w") as f:
            cabecalho = (f"""     NOME     //     ID     //  NOTA TPC  //  NOTA PROJETO  //  NOTA TESTE  \n""")
            f.write(cabecalho)
            for aluno in turma:
                linha = (f""" {aluno[0]}  //  {aluno[1]}  //  {aluno[2][0]}  //  {aluno[2][1]}  //  {aluno[2][2]}   
""")
                f.write(linha)
            print("""     O teu ficheiro de turma foi criado com sucesso.""")
            

    elif escolha == 6:
        with open("./BasedeTurmas/Turma.txt","r") as f:
            for linha in f:
                print(f"""    {linha}""")



    elif escolha == 0:
        c = False
        print("""      Tenha um bom dia!""")
    
    else:
        print("A opção que escolheu não corresponde a nenhuma das nossas opções. Tente novemente.")
