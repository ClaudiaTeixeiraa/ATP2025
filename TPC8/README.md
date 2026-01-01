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

Após a análise das instruções iniciais, iniciou-se um processo de reflexão e definição do projeto. Desde a fase inicial, destacou-se a intenção de criar uma clínica composta por diferentes unidades médicas, correspondentes a diferentes especialidades.  

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
--
Inicialmente para as chegadas, foi criada uma função para gerar chegadas de acordo com taxas geradas:
```
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

```
A partir desta função, foi possível gerar todas as chegadas de pacientes antecipadamente, antes do início da simulação. Com base nas taxas definidas, foi implementada uma distribuição de Poisson não homogénea, em que a taxa de chegada de pacientes varia ao longo do dia. Registam-se maiores intensidades nos períodos de pico: no início do dia (das 9:00 às 11:00, correspondendo às primeiras duas horas de funcionamento da clínica, com taxa de chegada definida como 18/60) e no final da tarde (das 18:00 às 21:00, correspondendo às últimas três horas antes do fecho, com taxa de chegada definida como 16/60).

Os tempos entre chegadas são gerados segundo uma distribuição exponencial, cuja média é inversamente proporcional à taxa de chegada, garantindo, desta forma, a caracterização de um processo de Poisson não homogéneo ao longo do dia definido por intervalo = np.random.exponential(1 / taxa).

Optou-se por não utilizar a função de pré-geração dos tempos de chegada, pois concluiu-se que a geração das chegadas em tempo real durante a simulação assegura um comportamento mais consistente do sistema, impedindo esperas artificiais e permitindo uma integração mais natural com a evolução temporal da simulação e a interface. Assim sendo, as chegadas são geradas ao longo da própria simulação e a função anteriormente mencionada foi descartada.

LUCAS EXPLICA AS CHEGADAS PORQUE AGORA COM AS CONFIG_ATUAL NÃO SEI ESPECIFICAMENTE ONDE ESTÃO DEFINIDAS AS TAXAS; FALAR DA FUNÇÃO CHEGADA_VALIDA EM CHEGADAS.PY

2.2. Triagem
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
- "consulta": temConsulta()
  
- Sendo temConsulta():
```
def temConsulta():
    consulta = False
    n = random.randint(1,100) 
    if n <= 80:
        consulta = True
    return consulta
```
A função temConsulta serve para diferenciar os pacientes que têm consulta marcada dos que não têm consulta porque na fila para a triagem serão organizados também por este estatuto. 

- "especialidade": doenca()
  
- Sendo doenca(): 
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
Esta função é fundamental porque define as proporções de cada especialidade, ou seja, o número de doentes com certa especialidade vai estar distribuído diferentemente. Por exemplo, um paciente tem uma maior probabilidade de apresentar um problema ou consulta de Medicina Geral (30%) do que de Endocrinologia (3%). Esta função também é um grande auxílio para mais tarde gerar a base de dados com os médicos da clínica. Assunto abordado mais à frente. A função gera um número aleatório entre 1 e 100 e cada especialidade tem um intervalo de números que pode ser maior ou menor consoante a “popularidade” da mesma. 

-"prioridade": prioridadeIndividual(pessoa)

-Sendo prioridadeIndividual(pessoa): 

```
def prioridadeIndividual(pessoa):
    prior = False
    if pessoa["incapacidade"] == True or pessoa["bebe_ao_colo"] == True or pessoa["gravidez"] == True or pessoa["idade"] <= 2 or pessoa["idade"] >= 75:
        prior = True
    return prior
```

A função de prioridade individual somente lê a base de dados e se a pessoa tiver alguma incapacidade (“incapacidade” : True), um bebé ao colo (“bebé ao colo” : True), estiver grávida (“gravidez” : True) ou ter mais de 75 anos de idade, é considerada uma pessoa com estatuto prioritário ("prioridade": True) 

Após a atribuição destes parâmetros, os doentes são organizados na fila para a triagem com base nos mesmos pelo que, os doentes com estatuto prioritário ficam em primeiro na lista, de seguida ficam os não prioritários com consulta e, por fim, os não prioritários sem consulta. Esta organização é possível através da função chegadaAntesTriagem(doente,fila_triagem) presente no ficheiro Triagem.py:
```
def chegadaAntesTriagem(doente, fila_triagem):
    #Fila antes de ser atendido na receção, ou seja, à chegada à clínica
    # doente prioritário fica atrás do último prioritário da fila 
    prioritarios=fila_triagem[0]
    resto= fila_triagem[1] #o resto são os pacientes que não são prioritários
    if doente["prioridade"] == True:
        prioritarios.append(doente)
    elif doente["consulta"] == True :
        j = 0
        while j < len(resto) and resto[j]["consulta"]:
            j += 1
        resto.insert(j, doente)
    else:
        resto.append(doente) #quem não tem consulta, vai para o fim da lista de espera inteira
   
    return fila_triagem
```
Nesta função, os doentes prioritários são colocados atrás do último doente prioritário já existente na fila, garantindo que pessoas com maior necessidade de atenção são atendidas primeiro. Entre os restantes, os doentes com consulta estão posicionados à frente dos que não têm consulta, mantendo a ordem relativa dos pacientes com consulta. Os doentes sem consulta são adicionados ao final da fila.

A triagem em si é feita nos balcões de atendimento que estão definidos por:
balcoes = [{balcão}]

balcão = {“id”: int , “prioritario”: bool, “disponivel” : bool, “doente” : str, “entrada” : float, “saida” : float, “ndoentes_atendidos” : int, “tempo_ocupado” : float}

```
balcoes = [
    {"id":1, "prioritario":True,  "disponivel":True, "doente":None, "entrada":None, "saida":None, "ndoentes_atendidos" : 0, "tempo_ocupado": 0.0},
    {"id":2, "prioritario":False, "disponivel":True, "doente":None, "entrada":None, "saida":None, "ndoentes_atendidos" : 0, "tempo_ocupado": 0.0},
    {"id":3, "prioritario":False, "disponivel":True, "doente":None, "entrada":None, "saida":None, "ndoentes_atendidos" : 0, "tempo_ocupado": 0.0}
]
```
Através da função criaBalcoes cada balcão regista se está disponível, o doente atendido, o tempo de entrada e saída, o número de doentes atendidos e o tempo total de ocupação.
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
Agora que os balcões estão criados podem ser ocupados. Mas ainda não há nada que defina o tempo de triagem, por isso mesmo é que a função tempoTriagem foi criada:
```
def tempoTriagem(t_atual):
    t_Triagem = max(0.5,np.random.normal(loc=3.0, scale=1.0))  # distribuição normal para tempo na triagem que em média demora 3 minutos e desvio padrão de 1 minuto
    entrada_triagem = t_atual
    saida_triagem = t_atual + t_Triagem
    t_atual += t_Triagem
    return entrada_triagem, saida_triagem, t_Triagem
```
Esta função usufrui da distribuição normal para gerar tempos de triagem que tendem para 3 minutos e podem sofrer um desvio-padrão de 1 minuto, garantindo variabilidade realista nos tempos de atendimento. Aqui também são registados os tempos que permitem atualizar o dicionário do doente e o balcão. garantindo variabilidade realista nos tempos de atendimento.

Durante a simulação, a função ocupar_balcaoTriagem verifica quais balcões estão disponíveis e atribui doentes da fila, atualizando os tempos de entrada e saída de cada paciente, bem como o estado do balcão. Para além disso, cria o evento de SAI_TRIAGEM que vai ser fundamental para a simulação em si:
```
def ocupar_balcaoTriagem(lista,balcoes,t_atual):
    fila_prioritario = lista[0]
    fila_resto=lista[1]
    eventos_gerados=[]
    for balcao in balcoes:
        #se o balcão for prioritário e estiver livre
        if balcao["prioritario"] and balcao["disponivel"] and fila_prioritario:
            doente = fila_prioritario.pop(0)  #remove o primeiro paciente da fila
            entrada = max(t_atual, doente["tchegada"])   #o max define o tempo de início da triagem como o maior entre t_atual e tchegada: se o balcão ficar livre antes da chegada do doente, usa tchegada; se estiver livre depois da chegada, usa t_atual

            _, saida, t_Triagem = tempoTriagem(entrada) #atualiza os tempos

            balcao.update({
                "doente": doente,
                "disponivel": False,
                "entrada": entrada,
                "saida": saida,
                "ndoentes_atendidos" : balcao["ndoentes_atendidos"] + 1,
                "tempo_ocupado": balcao["tempo_ocupado"] + t_Triagem
            })

            #também conseguimos atualizar os dados do paciente
            doente.update({ 
                "tentrada_triagem" : entrada,
                "tsaida_triagem": round(saida,2),
                "estado_final": "TRIAGEM"
            })

            #e ainda, geramos um evento de saída de triagem
            evento = {
                "tempo" : doente["tsaida_triagem"],
                "tipo" : "SAI_TRIAGEM",
                "doente" : doente,
                "balcao" : balcao["id"]
            }
            eventos_gerados.append(evento)

        #se o balcão não for prioritário e estiver livre 
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
Após o atendimento ao balcão, os doentes são removidos do balcão e o seu estado é atualizado para “FILA_CONSULTORIO”, indicando que aguardam agora para consulta. Para que isto aconteça é necessário haver uma função que atualize o estado do balcão para livre novamente. A função que permite isto é desocupar_balcaoTriagem:
```
def desocupar_balcaoTriagem(balcoes, t_atual):
    eventos_gerados = [] 
    evento = None
    for balcao in balcoes:
        if not balcao["disponivel"] and t_atual >= balcao["saida"]:

            doente = balcao["doente"]
        
            balcao.update({
                    "doente": None,
                    "disponivel": True,
                    "entrada": None,
                    "saida": None
                })
            
            doente["estado_final"] = "FILA_CONSULTORIO" #registo

            eventos_gerados.append(evento)
    return balcoes, eventos_gerados
```
Neste contexto, os eventos do tipo SAI_TRIAGEM são gerados no momento em que um doente inicia a triagem, pois é nesse instante que se conhece o tempo de conclusão do serviço.

A função desocupar_balcaoTriagem não gera novos eventos, limitando-se a atualizar o estado do sistema (libertação do balcão e transição do doente para a fila de consulta). Esta abordagem evita a criação de eventos redundantes e mantém a simulação consistente e eficiente.

Assim, a lista de eventos contém apenas eventos futuros relevantes, enquanto as alterações internas de estado são tratadas diretamente no momento da ocorrência do evento.

Ainda no ficheiro "Triagem.py" está a função tempo_medio_FilaTriagem que serve para obter dados acerca do tempo médio de espera na fila de triagem. Esta estatística vai ser usada mais à frente na interface de simulação:
```
def tempo_medio_FilaTriagem(doentes_atendidos):
    diferenca = []
    for doente in doentes_atendidos:
        if doente["tentrada_triagem"] != None:
            diferenca.append((doente["tentrada_triagem"] - doente["tchegada"]))

    media = round(sum(diferenca)/len(diferenca),2)

    return media
```

2.3. Consultório
--

