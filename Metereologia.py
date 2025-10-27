print("""Seja bem-vinda/o à nossa aplicação de Metereologia. No nosso menu terá acesso às ações que pode realizar.""" )


tabMeteo1 = [((2025,1,20), 2, 16, 0), 
             ((2025,1,21), 1, 13, 0.2), 
             ((2025,1,22), 7, 17, 0.01), 
             ((2025,1,23), 5, 14, 0), 
             ((2025,1,24), 3, 12, 0), 
             ((2025,1,25), 4, 15, 0.1), 
             ((2025,1,26), 6, 18, 0), 
             ((2025,1,27), 7, 19, 0), 
             ((2025,1,28), 8, 20, 0.05), 
             ((2025,1,29), 9, 21, 0), 
             ((2025,1,30), 7, 18, 0), 
             ((2025,1,31), 5, 16, 0.3), 
             ((2025,2,1), 4, 14, 0), 
             ((2025,2,2), 3, 13, 0), 
             ((2025,2,3), 2, 12, 0.4), 
             ((2025,2,4), 1, 11, 0.6), 
             ((2025,2,5), 0, 10, 0.8), 
             ((2025,2,6), 2, 13, 0.1), 
             ((2025,2,7), 4, 15, 0), 
             ((2025,2,8), 5, 17, 0), 
             ((2025,2,9), 6, 18, 0.05), 
             ((2025,2,10), 7, 19, 0)]



def listar(tabMeteo):
    res = []
    for i in tabMeteo:
        res.append(i)
    return res



def medias(tabMeteo):
    res = []
    for i in tabMeteo:
        med = (i[1] + i[2])/2
        res.append((f"""Dia:{i[0]} // Temp. média:{med}   """)) 
    return res



def guardaTabMeteo(t, fnome):
    with open(fnome,"w",encoding='utf-8' ) as f: 
        for dia in t:
            f.write(f"{dia[0][0]}; {dia[0][1]}; {dia[0][2]}; {dia[1]}; {dia[2]}; {dia[3]}\n")
       
    return



def carregaTabMeteo(fnome):
    with open(fnome,"r") as f:
        res = []
        for linha in f:
            campos = linha.split(";")
            res.append(((int(campos[0]), int(campos[1]), int(campos[2])), float(campos[3]), float(campos[4]), float(campos[5])))
        f.close()
        return res



def minMin(tabMeteo):
    res = []
    min = tabMeteo[0][1]
    for i in tabMeteo[1:]:
        if i[0][1] < min:
            min = i[0][1]
    return f"""     Temperatura mínima: {min}ªC"""




def amplTerm(tabMeteo):
    res = []
    for i in tabMeteo:
        dif = i[2] - i[1]
        res.append((f""" Dia: {i[0]}, Amplitude térmica: {dif} """))
    return res 



def maxChuva(tabMeteo):
    res = []
    max = tabMeteo[0][3]
    for dia,_,_,precip in tabMeteo[1:]:
        if precip > max:
            max = precip
    res.append((f"""Dia: {dia}, Precipitação: {max}"""))
    return res 



def diasChuvosos(tabMeteo, p):
    res = []
    for i in tabMeteo:
        if i[3] > p:
            res.append((f"""Dia: {i[0]}, Precipitação: {i[3]})"""))
    if p > 1 or p < 0:
        print("     O valor que inseriu não se encontra entre 0 e 1.")
    return res

    
def diasconsec(tabMeteo, p):
    maxConseq = 0 
    res = 0      
    for _, _, _, prec in tabMeteo:
        if prec < p:
            res = res + 1
            if res > maxConseq:
                maxConseq = res
        else:
            res = 0 
    print(f"""     Numero máximo de dias consecutivos com precipitação inferior a {p} é {maxConseq}.""")
    if p > 1 or p < 0:
        print("     O valor que inseriu não se encontra entre 0 e 1.")

    return 


import matplotlib.pyplot as plt

def extraiMin(t):
    res = []
    for _,tmin,_,_ in t:
        res.append(tmin)
    return res

def extraiMax(t):
    res = []
    for _,_,tmax,_ in t:
        res.append(tmax)
    return res

def extraiPrecip(t):
    res = []
    for _,_,_,Precip in t:
        res.append(Precip)
    return res


def grafTabMeteo(t):
    #T min
    x1 = list(range(1,len(t)+1))
    y1 = extraiMin(t)
    plt.plot(x1, y1, color='Pink', label = "Temperatura mínima")

    #T máx
    x2 = list(range(1,len(t)+1))
    y2 = extraiMax(t)
    plt.plot(x2, y2, color='deeppink', linestyle='dashed', label = "Temperatura máxima")

    #Precip
    x3 = list(range(1,len(t)+1))
    y3 = extraiPrecip(t)
    plt.plot(x3, y3, color='Red', linestyle='dashdot', label = "Precipitação")

    plt.title("Metereologia")
    plt.legend()
    plt.show()

    return



def menu():
    print(""" 
     Só poderá escolher as opções com os dados que já estão inseridos na nossa plataforma.    
     No menu de operações abaixo selecione a opção que quer selecionar:
    - 1: Listar os dados da plataforma;
    - 2: Calcular a temperatura média de cada dia;
    - 3: Guardar uma tabela meteorológica num ficheiro de texto;
    - 4: Carregar uma tabela meteorológica de um ficheiro de texto;
    - 5: Indicar a temperatura mínima mais baixa registada na tabela;
    - 6: Devolver a amplitude térmica de cada dia [(data, amplitude)];
    - 7: Indicar o dia em que a precipitação registada teve o seu valor máximo e indica esse valor;
    - 8: Indicar os dias em que a precipitação foi superior a um limite definido por si;
    - 9: Receber um tabela meteorológica e um limite p e retorna o maior número consecutivo de dias com precipitação abaixo desse limite;
    - 10: Desenhar os gráficos da temperatura mínima, máxima e de pluviosidade;
    - 0: Sair da aplicação""")
    escolha = int(input("""     Insira o número correspondente à sua opção: """))
    return escolha

c = True
while c == True:
    escolha = menu()

    if escolha == 1:
        print(listar(tabMeteo1))

    elif escolha == 2:
        print(medias(tabMeteo1))
    
    elif escolha == 3: 
        fnome = input("     Que nome quer dar ao seu ficheiro? ")
        guardaTabMeteo(tabMeteo1, fnome)
            
    elif escolha == 4:
        fnome = input("     Qual é o ficheiro que quer abrir? ")
        print("""     O que vai obter é uma lista de tuplos. Dentro de cada tuplo temos a seguinte estrutrura:
    ((Ano,Mês,Dia), Temperatura mínima, Temperatura máxima, Precipitação)""")
        print(f"""     {carregaTabMeteo(fnome)}""")

    elif escolha == 5:
        print(minMin(tabMeteo1))
    
    elif escolha == 6:
        print(amplTerm(tabMeteo1))
    
    elif escolha == 7:
        print("     O dia em que mais choveu foi o seguinte: ")
        print(maxChuva(tabMeteo1))

    elif escolha == 8:
        p = float(input("""     Qual limite de precipitação quer (valores entre 0 e 1)? """))
        print("     Na lista abaixo consegue ver em que dias a precipitação foi superior ao limite que arbitrou.")
        print(diasChuvosos(tabMeteo1, p))
    
    elif escolha == 9:
        p = float(input("""     Qual limite de precipitação quer (valores entre 0 e 1)? """))
        print(diasconsec(tabMeteo1, p))

    elif escolha == 10:
        print(grafTabMeteo(tabMeteo1))


    elif escolha == 0:
        c = False
        print("     Tenha um bom dia!")
    
    else:
        print("     A opção selecionada não corresponde a nenhuma das opções do menu. Tente novamente.")