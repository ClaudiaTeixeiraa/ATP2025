#TPC 8
# Simulação de uma Clínica

## Índice
- Introdução ao trabalho (ideias, expectativas)
- Desenvolvimento/Execução de código
- Criação da interface
- Criação de gráficos a partir da simulação na interface
- Conclusões finais

---

## 1. Introdução ao trabalho

Aquando da disponibilização do guião do projeto, foi possível reconhecer de imediato a sua dimensão e complexidade face ao nível de conhecimentos de programação até então adquiridos. Ainda assim, a ambição de desenvolver um projeto bem estruturado e o desafio associado ao desconhecido motivaram o início do trabalho.  

Após a análise das instruções iniciais, iniciou-se um processo de reflexão e definição conceptual do projeto. Desde a fase inicial, destacou-se a intenção de criar uma clínica composta por diferentes unidades médicas, correspondentes a diferentes especialidades.  

Adicionalmente, procurou-se aproximar o modelo da realidade, introduzindo estatutos de prioridade que permitissem um atendimento mais eficaz a pessoas com algum tipo de incapacidade. Com o mesmo objetivo de realismo, foi também definido um processo de triagem prévio à consulta, representando o funcionamento típico da receção de uma clínica.  

Ainda numa fase preliminar, estabeleceu-se que a clínica funcionaria durante 12 horas diárias, no período compreendido entre as 9:00 e as 21:00.  

Com estes pressupostos definidos, iniciou-se a fase de criação de código.

---

## 2. Desenvolvimento/Execução de código

Considerando a disponibilização de uma base de dados contendo informação relativa aos pacientes, optou-se pela sua utilização. No entanto, originalmente cada doente era caracterizado por parâmetros que não se encaixam propriamente no contexto do projeto, alguns sendo desnecessários. Assim sendo, removemos as que achamos irrelevantes e adicionamos outros que seriam úteis mais à frente:

```json
{
    "id": "p0",
    "BI": "91702023-5",
    "nome": "Neyanne Sampaio",
    "idade": 47,
    "sexo": "feminino",
    "incapacidade": false,
    "bebe_ao_colo": false,
    "gravidez": false
}
```

A cada paciente foram removidas algumas chaves que não seriam úteis no contexto da simulação e adicionamos: incapacidade, bebe_ao_colo, gravidez cujo valor é um boolean. Estas características seriam fundamentais para mais tarde definir prioridades. Para além da remoção, foram adicionadas estas chaves mas com algumas condições para fazer com que a base de dados se aproximasse da realidade:

Pessoas com menos de 15 anos e mais de 50 anos não poderiam estar grávidas;

Pessoas com menos de 15 anos não poderiam estar com bebé ao colo;

Da base de dados toda, somente cerca de 20% das pessoas é que apresentam pelo menos um critério de prioridade;

Após o estabelecimento das condições sobre os dados a tratar, iniciou-se a arquitetura para o funcionamento da clínica.

2.1. Chegadas

Inicialmente para as chegadas, foi criada uma função para gerar chegadas de acordo com taxas geradas:

tfinal = 12*60

def gera_tempos_chegada(tfinal):
    #taxas = [(início do bloco, fim do bloco, doentes que chegam/hora)]
    taxas = [
        (0, 2 * 60, 18 / 60),
        (2 * 60, 4 * 60, 11 / 60),
        (4 * 60, 7 * 60, 7 / 60),
        (7 * 60, 9 * 60, 9 / 60),
        (9 * 60, 12 * 60, 16 / 60)
    ]

    tchegadas = []
    tempo_atual = 0.0

    for hinicio, hfim, taxa in taxas:
        tempo_atual = max(tempo_atual, hinicio)
        while tempo_atual < hfim and tempo_atual < tfinal:
            intervalo = np.random.exponential(1 / taxa)
            tempo_atual += intervalo

            if tempo_atual < hfim and tempo_atual < tfinal:
                tchegadas.append(round(tempo_atual,2))

    return tchegadas


A partir desta função, foi possível gerar todas as chegadas de pacientes antecipadamente, antes do início da simulação. Com base nas taxas definidas, foi implementada uma distribuição de Poisson não homogénea, em que a taxa de chegada de pacientes varia ao longo do dia. Registam-se maiores intensidades nos períodos de pico: no início do dia (das 9:00 às 11:00, correspondendo às primeiras duas horas de funcionamento da clínica, com taxa de chegada definida como 18/60) e no final da tarde (das 18:00 às 21:00, correspondendo às últimas três horas antes do fecho, com taxa de chegada definida como 16/60).

Os tempos entre chegadas são gerados segundo uma distribuição exponencial, cuja média é inversamente proporcional à taxa de chegada, garantindo, desta forma, a caracterização de um processo de Poisson não homogéneo ao longo do dia definido por intervalo = np.random.exponential(1 / taxa).

Optou-se por não utilizar a função de pré-geração dos tempos de chegada, pois concluiu-se que a geração das chegadas em tempo real durante a simulação assegura um comportamento mais consistente do sistema, impedindo esperas artificiais e permitindo uma integração mais natural com a evolução temporal da simulação e a interface. Assim sendo, as chegadas são geradas ao longo da própria simulação e a função anteriormente mencionada foi descartada.

LUCAS EXPLICA AS CHEGADAS PORQUE AGORA COM AS CONFIG_ATUAL NÃO SEI ESPECIFICAMENTE ONDE ESTÃO DEFINIDAS AS TAXAS; FALAR DA FUNÇÃO CHEGADA_VALIDA EM CHEGADAS.PY

###2.2. Triagem
--

Agora que os pacientes já chegam à clínica e recebem um tempo de chegada, precisam de ser atendidos na triagem. Este passo é importante porque é quando os parâmetros de prioridade inicialmente atribuídos são usados para organizar os doentes na fila. Num novo ficheiro Triagem.py foi criada uma função:
```
def Doentes(ficheiro):
    doentes = []
    f = open(ficheiro, "r", encoding = "utf-8")
    lista = json.load(f)
    for pessoa in lista:
        doente = {
        "nome": pessoa["nome"],
        "idade": pessoa["idade"],
        "sexo": pessoa["sexo"],
        "id": pessoa["id"],
        "BI": pessoa["BI"],
        "consulta": temConsulta(),
        "especialidade": doenca(),
        "prioridade": prioridadeIndividual(pessoa),
        "tchegada": None,
        "tentrada_triagem":None,
        "tsaida_triagem": None,
        "tentrada_consultorio" : None,
        "tsaida_consultorio":None,
        "aguarda_consultorio" :False,
        "estado_final" : None
        }
        doentes.append(doente)
    f.close()
    return doentes
```

Através desta função, o doente, já carregado da base de dados, ganha agora ainda mais atributos. De todos estes, são relevantes mencionar agora consulta, especialidade e prioridade:
```
def temConsulta():
    consulta = False
    n = random.randint(1,100) 
    if n <= 80:
        consulta = True
    return consulta
```
```
def doenca():
    n = random.randint(1,101)
    if n <= 7:
        doenca = "Dermatologia"
    elif n > 7 and n<= 13:
        doenca = "Gastroenterologia"
    elif n> 13 and n <= 18:
        doenca = "Pneumonologia"
    elif n> 18 and n <= 26:
        doenca = "Cardiologia"
    elif n>26 and n <= 29:
        doenca = "Endocrinologia"
    elif n>29 and n <= 38:
        doenca = "Ortopedia"
    elif n>38 and n <= 44:
        doenca = "Neurologia"
    elif n>44 and n <= 54:
        doenca = "Ginecologia e Obstetrícia"
    elif n>54 and n <= 58:
        doenca = "Psiquiatria"
    elif n>58 and n <= 70:
        doenca = "Pediatria"
    else:
        doenca = "Medicina Geral"
    return doenca
```
```
def prioridadeIndividual(pessoa):
    prior = False
    if pessoa["incapacidade"] == True or pessoa["bebe_ao_colo"] == True or pessoa["gravidez"] == True or pessoa["idade"] <= 2 or pessoa["idade"] >= 75:
        prior = True
    return prior
```

Após a atribuição destes parâmetros, os doentes são organizados na fila para a triagem com base nos mesmos pelo que, os doentes com estatuto prioritário ficam em primeiro na lista, de seguida ficam os não prioritários com consulta e, por fim, os não prioritários sem consulta. Esta organização é possível através da função chegadaAntesTriagem(doente,fila_triagem) presente no ficheiro Triagem.py:
```
def chegadaAntesTriagem(doente, fila_triagem):  
    prioritarios=fila_triagem[0]
    resto= fila_triagem[1]
    if doente["prioridade"] == True:
        prioritarios.append(doente)
    elif doente["consulta"] == True :
        j = 0
        while j < len(resto) and resto[j]["consulta"]:
            j += 1
        resto.insert(j, doente)
    else:
        resto.append(doente)
   
    return fila_triagem
```

A triagem em si é feita nos balcões de atendimento que estão definidos por:
```
balcoes = [
    {"id":1, "prioritario":True,  "disponivel":True, "doente":None, "entrada":None, "saida":None, "ndoentes_atendidos" : 0, "tempo_ocupado": 0.0},
    {"id":2, "prioritario":False, "disponivel":True, "doente":None, "entrada":None, "saida":None, "ndoentes_atendidos" : 0, "tempo_ocupado": 0.0},
    {"id":3, "prioritario":False, "disponivel":True, "doente":None, "entrada":None, "saida":None, "ndoentes_atendidos" : 0, "tempo_ocupado": 0.0}
]
```

Função para criar os balcões:
```
def criaBalcoes(config_atual):
    nbalcoes = config_atual["nbalcoes"]
    nbalcoes_prior = config_atual["nbalcoes_prior"]
    balcoes = []

    for i in range(1, nbalcoes + 1):
        balcoes.append({
            "id": i,
            "prioritario": False,
            "disponivel": True,
            "doente": None,
            "entrada": None,
            "saida": None,
            "ndoentes_atendidos": 0,
            "tempo_ocupado": 0.0
        })
   
    for i in range(0,nbalcoes_prior):
        balcoes[i]["prioritario"] = True

    return balcoes
```

Durante a simulação, a função ocupar_balcaoTriagem verifica quais balcões estão disponíveis e atribui doentes da fila, atualizando os tempos de entrada e saída de cada paciente, bem como o estado do balcão:
```
def ocupar_balcaoTriagem(lista,balcoes,t_atual):
    fila_prioritario = lista[0]
    fila_resto=lista[1]
    eventos_gerados=[]
    for balcao in balcoes:
        if balcao["prioritario"] and balcao["disponivel"] and fila_prioritario:  
            doente = fila_prioritario.pop(0)  
            entrada = max(t_atual, doente["tchegada"])  
            _, saida, t_Triagem = tempoTriagem(entrada)

            balcao.update({
                "doente": doente,
                "disponivel": False,
                "entrada": entrada,
                "saida": saida,
                "ndoentes_atendidos" : balcao["ndoentes_atendidos"] + 1,
                "tempo_ocupado": balcao["tempo_ocupado"] + t_Triagem
            })

            doente.update({
                "tentrada_triagem" : entrada,
                "tsaida_triagem": round(saida,2),
                "estado_final": "TRIAGEM"
            })

            evento = {
                "tempo" : doente["tsaida_triagem"],
                "tipo" : "SAI_TRIAGEM",
                "doente" : doente,
                "balcao" : balcao["id"]
            }
            eventos_gerados.append(evento)

        elif not balcao["prioritario"] and balcao["disponivel"] and fila_resto:
            doente = fila_resto.pop(0)
            entrada = max(t_atual, doente["tchegada"])
            _, saida, t_Triagem = tempoTriagem(entrada)

            balcao.update({
                "doente": doente,
                "disponivel": False,
                "entrada": entrada,
                "saida": saida,
                "ndoentes_atendidos" : balcao["ndoentes_atendidos"] + 1,
                "tempo_ocupado": balcao["tempo_ocupado"] + t_Triagem
            })

            doente.update({
                "tentrada_triagem" : entrada,
                "tsaida_triagem": round(saida,2),
                "estado_final" : "TRIAGEM"
            })

            evento = {
                "tempo" : doente["tsaida_triagem"],
                "tipo" :"SAI_TRIAGEM",
                "doente" : doente,
                "balcao" : balcao["id"]
            }
            eventos_gerados.append(evento)

    return lista, balcoes, eventos_gerados
```
