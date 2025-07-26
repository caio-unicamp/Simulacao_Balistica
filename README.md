# Simulação Balística de um Projétil 9mm FMJ considerando a Resistência do Ar

Este projeto simula o movimento balístico de uma bala 9mm FMJ (Full Metal Jacket) levando em conta a resistência do ar. Ele fornece graficamente as coordenadas do projétil em função do tempo, além de calcular a velocidade no ponto mais alto da trajetória e no momento do impacto com o solo.


## 🎯 Objetivo

Modelar de forma realista a trajetória de um projétil disparado por uma pistola, utilizando dados reais e técnicas numéricas para resolver o sistema de equações diferenciais que descreve seu movimento.


## ⚙️ Descrição Física do Problema

### 🔸 Movimento Balístico

Quando um projétil é disparado, ele segue uma trajetória determinada por:

- A força da **gravidade**, que age constantemente para baixo.
- A **resistência do ar**, que se opõe ao movimento e depende da velocidade, da forma do projétil e da densidade do ar.

### 🔸 Resistência do Ar

A força de arrasto que o ar exerce sobre o projétil é dada pela fórmula:

$\vec{F}_d = -\frac{1}{2} C_d \rho A v \vec{v}$

Onde:

- $\ C_d \$: Coeficiente de arrasto (depende da forma do projétil; para uma 9mm FMJ usa-se 0.295)
- $\ \rho \$: Densidade do ar (1.225 kg/m³ ao nível do mar)
- $\ A \$: Área frontal do projétil (baseado no diâmetro)
- $\ v \$: Velocidade escalar do projétil
- $\ \vec{v} \$: Vetor velocidade

Essa força depende do quadrado da velocidade e **atua sempre na direção oposta ao movimento**.

## 📌 Condições de Contorno

- **Gravidade constante**: $\ g = 9.81 \, \text{m/s}^2 \$
- **Resistência do ar considerada**, com parâmetros reais
- **Velocidade inicial**: 358 m/s (Valor estimado para munição 9mm FMJ)
- **Ângulo de disparo**: 45°
- **Massa do projétil**: 8 g
- **Área frontal do projétil**: Calculada como área de um círculo, usando o diâmetro real de 9.02 mm


## 🧮 Equações do Movimento

As equações diferenciais que governam o movimento são obtidas a partir da 2ª Lei de Newton:


$$m \cdot \vec{a} = \vec{F}_g + \vec{F}_d$$


Separando em componentes (horizontal e vertical):

- $$\ \frac{dx}{dt} = v_x \$$
- $$\ \frac{dy}{dt} = v_y \$$
- $$\ \frac{dv_x}{dt} = -\frac{1}{2m} C_d \rho A v v_x \$$
- $$\ \frac{dv_y}{dt} = -g -\frac{1}{2m} C_d \rho A v v_y \$$

Onde: 

$$\ v = \sqrt{v_x^2 + v_y^2} \$$


## 🧩 Método de Resolução (EDO)

Foi utilizado o método `solve_ivp` da biblioteca SciPy para resolver numericamente as equações diferenciais:

- Ele utiliza internamente métodos como **Runge-Kutta de ordem 5 (RK45)**.
- É ideal para sistemas de EDOs com eventos (como o impacto com o solo).
- Foram adotadas tolerâncias numéricas bem pequenas (`rtol=1e-8`, `atol=1e-8`) para garantir precisão.

### 🛑 Evento Especial: Impacto com o Solo

Foi definido um **evento** que detecta quando a altura do projétil volta a ser zero (y = 0), encerrando a simulação neste ponto.


## 📊 Saídas da Simulação

1. **Gráfico da posição horizontal x(t) e vertical y(t)** ao longo do tempo
2. **Velocidade no ponto mais alto da trajetória**
3. **Velocidade no momento do impacto com o solo**
4. **Tempo total de voo**


## 📦 Requisitos

- Python 3.8 ou superior
- Bibliotecas:
  - `numpy`
  - `matplotlib`
  - `scipy`

Instale com:

```bash
pip install numpy matplotlib scipy
```


## 🚀 Como Executar

1. Salve o script com o código da simulação (por exemplo, `simulacao_balistica.py`)
2. Execute com:

```bash
python3 simulacao_balistica.py
```

## 🧠 Conclusão

O projeto demonstra como traduzir um fenômeno físico real em um modelo computacional detalhado, com o uso de métodos numéricos para simulação e análise. Ele é especialmente útil para:

- Estudantes de Física ou Engenharia
- Desenvolvedores interessados em simulação de sistemas físicos

## 📚 Referências

- [Documentação](scipy.integrate.solve_ivp)
- [Tabela balística](beckerblindagens.com.br)
- [Explicação resistência do ar](https://en.wikipedia.org/wiki/Drag_(physics))