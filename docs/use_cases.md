# 🎮 Casos de Uso: World's Easiest Game

## 📌 Visão Geral
Este documento detalha os casos de uso para o jogo **"World's Easiest Game"**, um jogo de plataforma cujo objetivo principal é navegar por fases, coletar moedas quando necessário, evitar inimigos e alcançar o final de cada nível. O jogo foca na medição de tempo e na conclusão das fases.

## 👤 Atores
- **Jogador**: O único ator que interage diretamente com o jogo, controlando o personagem e as opções de menu.

---

## Casos de Uso Principais

### 1. 🕹️ Iniciar Jogo
- **Descrição**: O jogador acessa a tela inicial do jogo e inicia uma nova partida ou continua uma partida existente (se um save for encontrado).
- **Fluxo Básico**:
  1. O jogo é iniciado e tenta carregar um save existente.
  2. Se o save for carregado com sucesso:
     - O sistema verifica se há dados de jogador.
     - Se não houver dados de jogador (primeira inicialização ou save inválido):
       - Um novo personagem (Player) e um novo cronômetro (Cronometro) são criados.
       - O jogo salva o estado inicial.
     - O jogo exibe o menu principal.
  3. Se ocorrer um erro ao carregar o save:
     - Uma mensagem de erro de depuração é exibida no console.
     - O jogo é encerrado.
- **Pós-condições**: O jogador está no menu principal, ou o jogo foi encerrado devido a um erro.

---

### 2. 🧭 Navegar pelo Menu Principal
- **Descrição**: O jogador interage com as opções apresentadas no menu principal do jogo para iniciar uma partida, ver os controles ou sair.
- **Fluxo Básico**:
  1. O jogo exibe a tela do menu principal com as opções: "PLAY", "CONTROLS" e "QUIT".
  2. O jogador move o cursor do mouse, e os botões reagem visualmente (mudança de cor).
  3. O jogador clica em uma das opções:
     - "PLAY": O jogo inicia o loop principal da jogabilidade.
     - "CONTROLS": O jogo exibe a tela de controles.
     - "QUIT": O jogo é encerrado.
- **Fluxo Alternativo**:
  - Sair da Aplicação:
    1. O jogador clica no botão de fechar a janela do jogo.
    2. O jogo é encerrado.
- **Pós-condições**: O jogo iniciou, a tela de controles foi exibida, ou o jogo foi encerrado.

---

### 3. 🎮 Visualizar Controles
- **Descrição**: O jogador acessa uma tela que mostra as instruções de controle do jogo.
- **Fluxo Básico**:
  1. O jogo exibe a tela de controles, mostrando as teclas de atalho e o texto "Setinhas :)".
  2. O jogador move o cursor do mouse, e o botão "BACK" reage visualmente.
  3. O jogador clica no botão "BACK".
  4. O jogo retorna ao menu principal.
- **Fluxo Alternativo**:
  - Sair da Aplicação:
    1. O jogador clica no botão de fechar a janela.
    2. O jogo é encerrado.
- **Pós-condições**: O jogador retornou ao menu principal ou o jogo foi encerrado.

---

## Casos de Uso de Jogabilidade

### 4. 🏃 Jogar Fase
- **Descrição**: O jogador interage com o ambiente da fase, move seu personagem, evita inimigos e coleta moedas enquanto o tempo é contabilizado.
- **Pré-condições**: O jogo foi iniciado após o jogador selecionar "PLAY" no menu principal.
- **Fluxo Básico**:
  1. O sistema carrega as fases e obtém as instâncias do jogador e do cronômetro.
  2. O cronômetro é retomado (se não houver trapaças).
  3. Mapa da fase atual é carregado.
  4. O jogo entra em seu loop principal:
     - A taxa de quadros (FPS) é controlada.
     - A tela é preenchida com a cor de fundo.
     - HUD com cronômetro, botões "Menu" e "Reset" é desenhada.
     - O estado do mapa (moedas, inimigos) é atualizado.
     - O estado do jogador (posição, colisões) é atualizado e renderizado.
       - Movimentação: O jogador controla o personagem usando as setas do teclado.
     - O sistema verifica se o jogador completou a fase.
       - Condição de Conclusão da Fase: O jogador deve coletar todas as moedas (se existirem na fase) e chegar ao final da fase.
       - Se a fase for completada:
         - O próximo nível é carregado.
         - O cronômetro é ajustado para a nova fase.
     - O jogo aguarda e processa eventos do usuário.
       - Colisão com Inimigo:
         - Se o jogador colidir com um inimigo:
           - O jogador é transportado de volta para o início da fase.
           - Uma morte é contabilizada no contador de mortes do jogador.
     - A tela é atualizada.
- **Pós-condições**: O jogador progrediu para a próxima fase, retornou ao menu principal, reiniciou o jogo, ou saiu da aplicação.

---

### 5. ↩️ Voltar ao Menu Principal
- **Descrição**: Durante a jogabilidade, o jogador pode optar por retornar ao menu principal.
- **Fluxos**:
  - Via botão "Menu":
    1. O jogador clica no botão "Menu" na HUD.
    2. O cronômetro é pausado.
    3. O estado atual do jogo é salvo.
    4. Retorna ao menu principal.
  - Via tecla ESC:
    1. O jogador pressiona a tecla ESC.
    2. O cronômetro é pausado.
    3. O estado atual do jogo é salvo.
    4. O jogo retorna ao menu principal.
- **Pós-condições**: O jogador está no menu principal, e o estado do jogo foi salvo.

---

### 6. 🔄 Reiniciar Jogo
- **Descrição**: O jogador pode reiniciar todo o jogo, voltando para a primeira fase e resetando o progresso.
- **Fluxo Básico**:
  1. O jogador clica no botão "Reset" na HUD.
  2. A posição e o estado do jogador são redefinidos para o início da Fase 1.
  3. O cronômetro é redefinido e pausado.
  4. O estado atual do jogo é salvo.
  5. O jogo retorna ao menu principal.
- **Pós-condições**: O jogo foi reiniciado para a Fase 1, e o jogador está no menu principal.

---

### 7. 🧥 Trocar Aparência do Personagem
- **Descrição**: O jogador pode mudar a "skin" ou aparência do seu personagem durante a jogabilidade.
- **Fluxo Básico**:
  1. Durante a jogabilidade, o jogador pressiona a tecla T.
  2. A skin do personagem é alternada.
- **Pós-condições**: A aparência do personagem foi alterada.

---

### 8. 🧪 Utilizar Ferramentas de Cheats (Para Desenvolvimento/Teste)
- **Descrição**: Funcionalidades de atalho para avançar ou retroceder fases, geralmente usadas para teste e não disponíveis para o jogador final.
- **Fluxos**:
  - Avançar Fase:
    1. Durante a jogabilidade, o jogador pressiona a tecla N.
    2. A fase do jogador é incrementada.
    3. O próximo nível é carregado.
    4. A flag de "trapaça" do jogador é ativada (has_cheated = 1).
    5. O cronômetro é pausado.
  - Voltar Fase:
    1. Durante a jogabilidade, o jogador pressiona a tecla M.
    2. A fase do jogador é decrementada, com um limite mínimo na Fase 1.
    3. A fase anterior (ou a Fase 1) é carregada.
    4. A flag de "trapaça" do jogador é ativada.
    5. O cronômetro é pausado.
- **Pós-condições**: O jogador foi movido para uma fase diferente, o cronômetro foi pausado e é exibido a mensagem "cheater" na tela.

---

### 9. ❌ Encerrar Jogo (Durante Jogabilidade)
- **Descrição**: O jogador fecha a aplicação do jogo durante a jogabilidade.
- **Fluxo Básico**:
  1. O jogador clica no botão de fechar a janela do jogo.
  2. O estado atual do jogo é salvo.
  3. O jogo é encerrado.
- **Pós-condições**: O jogo foi encerrado, e o progresso foi salvo.

---

### 10. 🏆 Visualizar Resultados Finais
- **Descrição**: O jogador vê o desempenho total após completar todas as fases do jogo.
- **Pré-condições**: O jogador completou a última fase do jogo.
- **Fluxo Básico**:
  1. A tela é preenchida com a cor de fundo (branco).
  2. Uma imagem de conclusão do jogo é exibida.
  3. O botão "MENU" é exibido, permitindo ao jogador retornar ao menu principal.
  4. O sistema verifica se o jogador utilizou cheats:
     - Se o jogador NÃO utilizou cheats:
       - O tempo gasto em cada fase é formatado (minutos:segundos:milissegundos) e exibido em uma tabela.
       - O tempo total acumulado de todas as fases é calculado e exibido.
       - O número total de mortes é exibido.
     - Se o jogador utilizou cheats:
       - A mensagem "Cheater" é exibida na tela.
       - Uma imagem específica (Mickey) é exibida.
  5. O jogador interage com os eventos:
     - Sair da Aplicação: Se o jogador clica no botão de fechar a janela, o jogo é encerrado.
     - Voltar ao Menu: Se o jogador clica no botão "MENU", o jogo retorna ao menu principal.
  6. A tela é atualizada.
- **Pós-condições**: O jogador retornou ao menu principal ou encerrou o jogo.