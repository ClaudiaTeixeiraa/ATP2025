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

As estimativas dos tempos e tamanhos das filas de espera de estabelecimentos de saúde é um dos temas e preocupações principais quando o tema é eficácia de gestão de recursos. Um programa de simulação de chegadas de pacientes a uma clínica é um exemplo de uma forma de tentar perceber quais estratégias podem agilizar o atendimento de pacientes, garantindo a divisão de tarefas equitativas entre órgãos diferentes da clínica.


Ao elaborar uma simulação deste género, é esperado obter resultados relativos a:
1. Intervalos de tempo de:
1.1 filas de espera;
1.2 atendimento;
1.3 ocupação de recursos.
2. Tamanhos de filas de espera;
3. Taxas de:
3.1 número de pacientes atendidos;
3.2 número de pacientes por atender;
3.3 ocupação de recursos em função do número de pacientes chegados à clínica.
Com o tratamento destes dados, podemos inferir a eficácia e a exigência dos vários re-
cursos em função de vários parâmetros, como número de chegadas de pacientes, quantidade
de recursos em serviço e tempo.
O objetivo da elaboração deste projeto, no âmbito da unidade curricular de Algoritmos
e Técnicas de Programação, é implementar uma simulação de eventos discretos que
modela o funcionamento de uma clínica de saúde, permitindo avaliar o impacto de diferentes
parâmetros no desempenho do sistema.

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

2.3. Consultórios
--
Após os pacientes serem atendidos na receção, estes necessitam de ser encaminhados para as respetivas consultas médicas. Para tal, os pacientes são processados e inseridos nas filas de espera das consultas correspondentes à sua especialidade. Toda a lógica associada à gestão dos consultórios encontra-se implementada no ficheiro Consultórios.py, o qual importa as bibliotecas JSON e NumPy.

Antes de detalhar o funcionamento deste ficheiro, torna-se fundamental analisar a base de dados de médicos da clínica. Com o objetivo de conferir maior realismo à simulação, foi criado um ficheiro JSON que contém médicos das 11 especialidades definidas, distribuídos de acordo com a frequência e relevância de cada especialidade na clínica.

Na base de dados, cada médico é definido do seguinte modo:
```
{"nome":"Helena Santos",
"id":"m1",
"ocupado":false,
"doente":null,
"inicio_consulta":0.0,
"fim_consulta":0.0,
"especialidade":"Cardiologia",
"inicio_turno":0,
"fim_turno":430}
```
Através da análise desta estrutura, é possível observar que os médicos apresentam turnos distintos. Cada médico trabalha um total de 8 horas por dia, sendo que, nas especialidades com mais do que um médico, os turnos encontram-se intercalados de forma a garantir uma maior cobertura horária. Por outro lado, as especialidades que dispõem apenas de um médico funcionam exclusivamente durante um turno de 8 horas, que pode corresponder ao período inicial ou final do dia.

Face a esta organização, surgiu a necessidade de desenvolver uma função responsável por carregar os médicos a partir do ficheiro JSON e inicializar os seus dados para a simulação.

```
def carregaMedicos(ficheiro):
    medicos = []
    with open("./tentativa2/medicos.json", "r", encoding="utf-8") as p:
        lista_medicos = json.load(p)
        for pessoa in lista_medicos:
            medico = {
                "nome": pessoa["nome"],
                "id": pessoa["id"],
                "disponibilidade": True,
                "doente": None,
                "inicio_consulta":None,
                "fim_consulta":None,
                "inicio_turno":pessoa["inicio_turno"],
                "fim_turno":pessoa["fim_turno"],
                "especialidade": pessoa["especialidade"],
                "ndoentes_atendidos": 0,
                "id_doentes_atendidos" : [],
                "tempo_ocupado":0
                }
            medicos.append(medico)
    return medicos
```

Esta função abre o ficheiro medicos.json e, para cada médico presente na base de dados, cria um dicionário que contém tanto informações pessoais como variáveis de estado necessárias à simulação. São inicializados os atributos relacionados com a disponibilidade do médico, as consultas realizadas e as métricas de desempenho. Por fim, todos os médicos são adicionados a uma lista, que é devolvida pela função.

Uma vez que determinadas especialidades estão associadas a mais do que um médico, a clínica foi organizada em secções, sendo que cada secção corresponde a uma especialidade médica. Dentro de cada secção existem vários consultórios, e cada consultório está associado a um médico específico.

```
seccoes = [{"especialidade": "Dermatologia", "id": "s1", "consultorios":[]},

            {"especialidade": "Gastroenterologia", "id": "s2", "consultorios":[]},
                                                                            
            {"especialidade": "Pneumonologia", "id": "s3", "consultorios":[]},
            
            {"especialidade": "Cardiologia", "id": "s4", "consultorios":[]},
            
            {"especialidade": "Endocrinologia", "id": "s5","consultorios":[]},
                                                                        
            {"especialidade": "Ortopedia", "id": "s6","consultorios":[]},
            
            {"especialidade": "Neurologia", "id": "s7","consultorios":[]},

            {"especialidade": "Ginecologia e Obstetrícia", "id": "s8","consultorios":[]},

            {"especialidade": "Psiquiatria", "id": "s9","consultorios":[]},

            {"especialidade": "Pediatria", "id": "s10","consultorios":[]},

            {"especialidade": "Medicina Geral", "id": "s11","consultorios":[]}]
```

Inicialmente, a lista de consultórios de cada secção encontra-se vazia. Assim, foi necessário desenvolver uma função responsável pela criação dos consultórios e pela associação correta entre médicos e especialidades.

```
def cria_id(medico):
    c = medico["id"]
    num = c[1:]
    return num

def criaConsultorios(medicos,seccoes):
    for medico in medicos:
        n = 0
        while n < len(seccoes): 
            if medico["especialidade"] == seccoes[n]["especialidade"]:
                seccoes[n]["consultorios"].append({"id":"c" + cria_id(medico), "medico":medico})
                n +=1
            else: 
                n +=1
    return seccoes
```
A função criaConsultorios percorre a lista de médicos e, para cada um, identifica a secção correspondente à sua especialidade. Em seguida, é criado um consultório com um identificador próprio e este é associado ao médico em questão.

Para garantir coerência entre os identificadores dos médicos e dos consultórios, foi criada a função auxiliar cria id, que extrai a parte numérica do identificador do médico (por exemplo, "m3" → "3"), permitindo que o consultório associado utilize o mesmo número identificativo.

Com os consultórios criados e com os médicos carregados, restava associá-los à simulação. 

Primeiramente, a função encontraDoente tem o objetivo de remover um doente da fila de espera quando este já entrou no consultório, garantindo a coerência entre o estado do doente e as filas.
```
def encontraDoente(doente,fila):
    if doente != None:
        v = 0
        pronto = False
        while v < len(fila) and not pronto:
            if fila[v]["id"] == doente["id"] and doente["tentrada_consultorio"] != None:
                fila.pop(v)
                pronto = True
            else:
                v +=1
    return fila
```
A função recebe como argumentos um doente e uma fila de espera. Caso o doente exista, percorre a fila com o mesmo id e verifica se o doente com o mesmo id já entrou no consultório se este já possui tempo de entrada no consultório. Quando estas condições são satisfeitas, o doente é removido da fila utilizando o método pop e é retornada a fila agora sem esse doente. 

Por outro lado, a função atribuir doente a medico é responsável por atribuir um doente a um médico disponível, respeitando a especialidade médica e o horário de trabalho do médico. 
```
def atribuir_doente_a_medico(doente, seccoes, t_atual):
    medicos_seccao = None
    i = 0

    while i < len(seccoes) and medicos_seccao is None:
        sec = seccoes[i]
        if sec["especialidade"] == doente["especialidade"]:
            medicos_seccao = [c["medico"] for c in sec["consultorios"]]
        i += 1

    for m in medicos_seccao:
        m["disponibilidade"] = (m["inicio_turno"] <= t_atual < m["fim_turno"]and m["doente"] is None)
        
    disponiveis = [m for m in medicos_seccao if m["inicio_turno"] <= t_atual < m["fim_turno"] and m["doente"] is None]

    if not disponiveis:
        return None

    medico = min(disponiveis, key=lambda m: m["ndoentes_atendidos"])

    tempo = None
    i = 0

    while i < len(tempo_consulta_especialidade) and tempo is None:
        t = tempo_consulta_especialidade[i]
        if t["especialidade"] == medico["especialidade"]:
            tempo = max(5, np.random.normal(t["tempo_medio_consulta"], 5))
        i += 1
        
    medico["doente"] = doente
    medico["disponibilidade"] = False
    medico["inicio_consulta"] = round(t_atual, 2)
    medico["fim_consulta"] = round(t_atual + tempo, 2)
    doente["tentrada_consultorio"] = medico["inicio_consulta"]
    doente["tsaida_consultorio"] = medico["fim_consulta"]
    medico["ndoentes_atendidos"] += 1
    medico["id_doentes_atendidos"].append(doente["id"])
    medico["tempo_ocupado"] = round(medico["tempo_ocupado"] + tempo,2)
    doente["estado_final"] = "CONSULTA" #registo

    return medico #encontrou um médico
```

Em primeiro lugar, a função identifica a secção correspondente à especialidade do doente e obtém a lista de médicos dessa secção. De seguida, verifica quais os médicos que se encontram disponíveis no instante atual da simulação, ou seja, cujo turno está ativo e que não se encontram a atender outro doente.

Caso existam médicos disponíveis, é selecionado o médico que atendeu menos doentes até ao momento, promovendo assim uma distribuição mais equilibrada da carga de trabalho.

A duração da consulta é então calculada com base na especialidade médica, recorrendo a uma distribuição normal centrada no tempo médio definido para essa especialidade, sendo garantido um tempo mínimo de consulta.

```
tempo_consulta_especialidade = [
    {"especialidade": "Cardiologia", "tempo_medio_consulta": 30},
    {"especialidade": "Pediatria", "tempo_medio_consulta": 20},
    {"especialidade": "Dermatologia", "tempo_medio_consulta": 15},
    {"especialidade": "Gastroenterologia", "tempo_medio_consulta": 25},
    {"especialidade": "Pneumonologia", "tempo_medio_consulta": 25},
    {"especialidade": "Endocrinologia", "tempo_medio_consulta": 20},
    {"especialidade": "Ortopedia", "tempo_medio_consulta": 20},
    {"especialidade": "Neurologia", "tempo_medio_consulta": 30},
    {"especialidade": "Ginecologia e Obstetrícia", "tempo_medio_consulta": 25},
    {"especialidade": "Psiquiatria", "tempo_medio_consulta": 45},
    {"especialidade": "Medicina Geral", "tempo_medio_consulta": 15}
]
```
Por fim, são atualizados os estados do médico e do doente, incluindo os tempos de início e fim da consulta, as estatísticas do médico e o estado final do doente. A função devolve o médico atribuído ou None caso não exista disponibilidade.

À semelhança da ocupação dos médicos, torna-se necessário desócupa-los após o término da consulta e, para isso, foi desenvolvida a função desocuparMedico que garante que após a consulta o dicionário do médico é atualizado e ele consiga atender o próximo paciente. 

```
def desocuparMedico(medico,t_atual):
    if medico != None:
        if medico["fim_consulta"] != None:
            if t_atual >= medico["fim_consulta"] :

                doente = medico["doente"]
                doente["estado_final"] = "ATENDIDO" #registo

                medico.update({
                "disponibilidade": True,
                "doente": None,
                "inicio_consulta":None,
                "fim_consulta":None,
                })

    return medico
```
A função recebe um médico e o instante atual da simulação. Caso o médico se encontre em consulta e o tempo atual seja igual ou superior ao tempo de fim da consulta, considera-se que a consulta terminou.

Nessa situação, o estado final do doente é atualizado para "ATENDIDO", e os atributos do médico relacionados com a consulta são reinicializados, nomeadamente a disponibilidade, o doente associado e os tempos de consulta.

Apesar das funções anteriores gerirem corretamente a atribuição e libertação de médicos, estas não são responsáveis pela organização das filas de espera. Após a triagem os doentes deixam de ter prioridade com base nos critérios iniciais, sendo que quem tem consulta marcada tem prioridade sobre quem não tem consulta.POR AQUI LIGAÇÃO. 

Neste contexto, surge a função tentar atribuir fila que gere as filas de espera e tenta atribuir vários doentes, respeitando prioridades. Esta função seleciona o doente a ser atendido, dando prioridade aos doentes com consulta marcada, e apenas considera os doentes sem consulta quando a fila prioritária se encontra vazia. Sempre que um doente é atribuído a um médico, este é removido da fila correspondente e é criado um evento do tipo "SAI_CONSULTORIO", que representa o momento em que a consulta termina. Este processo é repetido enquanto existirem doentes em fila e médicos disponíveis.

```
def tentar_atribuir_fila(esp, filas_consultas, seccoes, eventos, t_atual):
    continuar = True

    while continuar == True: #enquanto houverem doentes na fila
        if filas_consultas[esp]["com_consulta"]:
            doente = filas_consultas[esp]["com_consulta"][0]
            origem = "com_consulta"

        elif filas_consultas[esp]["sem_consulta"]:
            doente = filas_consultas[esp]["sem_consulta"][0]
            origem = "sem_consulta"

        else: #as filas estão vazias
            continuar = False

        if continuar == True: #se não estiverem vazias
            medico = atribuir_doente_a_medico(doente, seccoes, t_atual)
            #procura o médico e tenta atribui-lo ao doente

            if medico: #se houver médico disponível
                filas_consultas[esp][origem].pop(0)
                #remove o primeiro paciente que estava na fila dessa especialidade

                eventos.append({
                    "tempo": medico["fim_consulta"],
                    "tipo": "SAI_CONSULTORIO",
                    "doente": doente,
                    "medico": medico
                })
                #atualiza o evento para SAI CONSULTÓRIO que é adicionado aos eventos da simulação

                eventos.sort(key=lambda e: e["tempo"])
                #ordena os eventos por ordem cronológica

            else: #caso não exista médico disponível
                continuar = False
                #a função termina
```

Deste modo, esta função desempenha um papel central na simulação, garantindo que os doentes são atendidos assim que existam médicos disponíveis, atualizando corretamente as filas, aplicando critérios de prioridade e coordenando a criação de eventos temporais. Assim, assegura-se um fluxo contínuo e realista de atendimento dentro da clínica.

A função atribuir doente a medico é responsável pela lógica individual de atribuição de um doente a um médico disponível, enquanto a função tentar atribuir fila atua ao nível da gestão global do sistema, selecionando doentes das filas de espera, aplicando critérios de prioridade e coordenando a criação de eventos na simulação.

Apesar de a função tentar_atribuir_fila remover explicitamente os doentes das filas no momento em que estes entram em consulta, a função encontraDoente mantém-se relevante como mecanismo auxiliar de consistência, permitindo garantir que um doente não permanece indevidamente em filas de espera após ter iniciado a consulta.

No restante conteúno no ficheiro relaciona-se com a obtenção de estatísticas para criação de gráficos. 
1. Função do tamanho das filas consultas: para cada especialidade guarda o tamanho das filas com e sem consulta e calcula o total.
   ```
   def tamanho_filas_cosultas(filas_consultas,tam_filas):

    for esp, fila in filas_consultas.items():

        if esp not in tam_filas:
            tam_filas[esp] = {
                "sem_consulta" : [],
                "com_consulta" : [],
                "tam_total" : []
            }
            tam_filas[esp]["sem_consulta"] = [len(fila["sem_consulta"])]
            tam_filas[esp]["com_consulta"] = [len(fila["com_consulta"])]
            tam_filas[esp]["tam_total"] = [len(fila["sem_consulta"]) + len(fila["com_consulta"])]
        
        else:
            tam_filas[esp]["sem_consulta"]= tam_filas[esp]["sem_consulta"] + [len(fila["sem_consulta"])]
            tam_filas[esp]["com_consulta"] = tam_filas[esp]["com_consulta"] + [len(fila["com_consulta"])]
            tam_filas[esp]["tam_total"] = tam_filas[esp]["tam_total"] + [len(fila["sem_consulta"]) + len(fila["com_consulta"])]

    return tam_filas
   ```
2. Função do tamanho total das filas consultas: soma o número total de doentes em todas as especialidades.
   ```
   def tamanho_total_filasconsultas(filas_consultas,tam_filas,tam_filas_total):
    soma = 0
    
    for esp,tams in tam_filas.items():
        soma += tam_filas[esp]["tam_total"][-1]

    tam_filas_total.append(soma)
        
    return tam_filas_total
   ```
3. Função da média do tamanho das filas consultas: calcula médias das filas com e sem consulta e uma média global por especialidade. Trata de casos em que não há dados.
   ```
   def media_tamanho_filas_consultas(tam_filas):

    med_filas = {}

    def calcula_media(fila):
        media = None
        if len(fila) != 0:
            media = sum(fila)/len(fila)
        return media

    for esp, fila in tam_filas.items():

        med_filas[esp] = {
            "media_sem_consulta": calcula_media(fila.get("sem_consulta", [])),
            "media_com_consulta": calcula_media(fila.get("com_consulta", [])),}
        if med_filas[esp]["media_com_consulta"] == None and med_filas[esp]["media_sem_consulta"] == None:
            med_filas[esp]["media_da_especialidade"] = None
        elif med_filas[esp]["media_com_consulta"] == None:
            med_filas[esp]["media_da_especialidade"] = med_filas[esp]["media_sem_consulta"]
        elif med_filas[esp]["media_sem_consulta"] == None:
            med_filas[esp]["media_da_especialidade"] = med_filas[esp]["media_com_consulta"]
        else:
            med_filas[esp]["media_da_especialidade"] = (med_filas[esp]["media_sem_consulta"] + med_filas[esp]["media_com_consulta"])/2

    return med_filas
   ```
4. Função da média global do tamanho das filas na clínica: junta as médias válidas de todas as especialidades e calcula a média final.
   ```
   def med_filas_consultas(med_filas):
    
    lista_soma = []

    for _,media in med_filas.items():

        if media["media_da_especialidade"] != None:
            lista_soma.append(media["media_da_especialidade"])
    
    media_final = None

    if lista_soma != []:
        media_final = sum(lista_soma)/len(lista_soma)
    
    return media_final
    ```
5. Função do tempo médio de espera entre a triagem e a entrada no consultório: para cada doente atentido calcula a diferença entre a entrada no consultório e a saída da triagem. Calcula a média dessas diferenças.
   ```
   def tempo_medio_FilasConsultas(doentes_atendidos):

    diferenca = []
    for doente in doentes_atendidos:
        if doente["tentrada_consultorio"] != None:
            diferenca.append((doente["tentrada_consultorio"] - doente["tsaida_triagem"]))

    media = round( sum(diferenca)/len(diferenca),2)

    return media
   ```
   



   
