# 🐝 Bee Guardian

Bee Guardian é um jogo **roguelike top-down** desenvolvido em **Python com PgZero**, onde o jogador controla uma abelha cuja missão é **proteger uma flor** de insetos invasores.

O projeto foi criado como um exemplo de jogo educacional bem estruturado, com foco em **movimento em grade suave**, **animação real de sprites**, **lógica clara de gameplay** e **código limpo**.

---

## 🎮 Gameplay

- O jogador controla uma **abelha protetora**
- Insetos invasores surgem continuamente e tentam alcançar a flor
- A abelha **elimina os insetos** antes que eles cheguem ao alvo
- O jogo utiliza um **sistema de pontuação**:
  - 🐞 Inseto eliminado: **+5 pontos**
  - 🌸 Inseto alcança a flor: **−30 pontos**
- O jogo termina quando a pontuação chega a **0 ou menos**

---

## 🕹️ Controles

- **Setas do teclado**: mover a abelha
- **Mouse**:
  - Start Game
  - Sound ON / OFF
  - Exit

---

## 🎵 Áudio

- Música de fundo contínua
- Efeitos sonoros para:
  - Cliques no menu
  - Eliminação de insetos
  - Penalidade quando um inseto alcança a flor
- Todo o áudio pode ser ativado ou desativado pelo menu principal

---

## 🧠 Características técnicas

- Gênero: **Roguelike (top-down, grid-based)**
- Movimento entre células com **transição suave animada**
- Animação real de sprites:
  - Abelha (idle e movimento)
  - Insetos (idle e movimento)
  - Flor (animação contínua)
- Inimigos se movimentam **dentro de um território**
- Menu principal com botões clicáveis
- Sistema de dificuldade progressiva

---

## 📚 Tecnologias utilizadas

- **Python 3**
- **PgZero**
- Bibliotecas padrão:
  - `random`
  - `math`
- `Rect` do Pygame (permitido pelo enunciado)

Nenhuma outra biblioteca externa é utilizada.

---

## ▶️ Como executar

1. Instale o PgZero:
   ```bash
   pip install pgzero

2. Execute o jogo na pasta do projeto:
   ```bash
    pgzrun main.py

