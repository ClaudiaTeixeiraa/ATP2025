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
