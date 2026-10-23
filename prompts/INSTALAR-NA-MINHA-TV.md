# Copie, cole e comece pela sua TV

Este prompt foi escrito para quem não tem nosso ambiente pronto. Ele inclui os endereços do projeto e das ferramentas. Copie o bloco inteiro para uma IA com acesso ao seu computador. Você fornece o modelo da TV e seus jogos; a IA identifica o restante com você.

```text
Quero instalar emuladores e jogar na minha TV Samsung. Comece com o sistema/jogo que eu indicar; se eu não indicar, pergunte qual quero. Prefiro executar na própria TV, sem PC ligado durante o jogo. Adapte tudo ao meu aparelho e ao sistema do meu computador.

PROJETO DE REFERÊNCIA
https://github.com/leandroxse/samsung-games

Leia o README e estes arquivos do repositório antes de propor comandos:
- Guia: https://github.com/leandroxse/samsung-games/blob/main/docs/INSTALACAO.md
- Resultados: https://github.com/leandroxse/samsung-games/blob/main/docs/RESULTADOS.md
- Empacotador: https://github.com/leandroxse/samsung-games/blob/main/tools/build-smw.py

Clone com git clone https://github.com/leandroxse/samsung-games.git se precisar executar o código. Não presuma que os scripts, SDK, certificados ou ferramentas já existem no meu computador. Não dependa de Obsidian ou arquivos pessoais do autor. Se eu fornecer notas minhas, use-as como contexto opcional, nunca como requisito.

FONTES DAS FERRAMENTAS
- Git: https://git-scm.com/downloads
- Python 3: https://www.python.org/downloads/
- SDK, SDB e CLI para TV: https://developer.samsung.com/smarttv/develop/getting-started/setting-up-sdk/installing-tv-sdk.html
- Conexão e modo de desenvolvedor: https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html
- Certificados Samsung: https://developer.samsung.com/smarttv/develop/getting-started/setting-up-sdk/creating-certificates.html
- CLI de assinatura/instalação: https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/command-line-interface.html
- RetroArch Tizen, que oferece vários sistemas: https://github.com/Sype0/retroarch-tizen
- TizenBrew, opção se aplicável: https://github.com/reisxd/TizenBrew
- Floating IPS, apenas se eu quiser aplicar um patch: https://github.com/Sir-Walrus/Flips/releases

FLUXO
[TV + sistema do computador]
   -> [Identificar Tizen, versão, modelo, rede e recursos acessíveis]
   -> [Escolher emulador compatível para meu sistema/jogo]
   -> [Obter ferramentas que faltam nas fontes oficiais]
   -> [Preparar minha ROM e pacote]
   -> [Assinar para minha TV e anotar reversão]
   -> [Instalar e abrir em primeiro plano]
   -> [Validar imagem, som, controles, saves, offline e desempenho]
   -> [Ajustar somente onde houver problema medido]

COMO EXECUTAR
1. Pergunte apenas o que não consegue identificar com segurança: modelo completo da TV, sistema do computador, console/jogo desejado e caminho da minha ROM. Confirme o aparelho autorizado antes de conectar. O requisito de Chromium 85/Tizen 6.5+ é declarado pelo RetroArch Tizen upstream; confirme a compatibilidade atual. TVs antigas e sistemas anteriores ao Tizen podem não servir para esse caminho.
2. Escolha o menor caminho viável. Não limite a solução à Q60C, Mario ou RetroArch. Compare alternativas somente quando a compatibilidade ou o desempenho justificarem. Moonlight é streaming e precisa de outra máquina; explique isso se for uma alternativa.
3. Para testar vários sistemas, considere primeiro o RetroArch Tizen original. Para um pacote local SNES, o script deste repositório aceita --rom, --name, --core e --initial-memory; use --help. Outros cores não estão implementados nesse empacotador. Não prometa suporte nativo a todos os emuladores.
4. O empacotador baixa o WGT base e recursos públicos ausentes. Exemplo: python3 tools/build-smw.py --rom "/caminho/jogo.sfc" --name "Meu jogo" --unsigned. No Windows, use py -3 se necessário. O WGT sem assinatura precisa ser assinado depois pelo SDK com meu perfil. Não dependa do tizen-sdb pessoal do autor, Vetro, root ou do caminho de certificados dele.
5. Eu forneço jogos, BIOS e patches. Não os baixe. Patch de tradução é opcional. Preserve originais e não ignore checksum inválido. Não publique ROM, BIOS, saves ou credenciais.
6. Use o processo oficial de modo de desenvolvedor e certificado para meu aparelho quando disponível. Não atualize firmware, faça root ou instale serviços sem uma necessidade e autorização específicas. Eu faço login e etapas físicas quando necessário.
7. Antes de instalar, leia IDs do config.xml, verifique se o pacote já existe e proteja saves. O preset deste repositório usa RtArchTzn0 / RtArchTzn0.RetroArch, compartilhados com o upstream. Pacotes de jogos diferentes substituem o mesmo app. Anote como remover sem atingir outros apps.
8. Valide primeiro plano, imagem, áudio, controle físico, SRAM e savestate. Teste abertura offline, não só cache de uma sessão. Meça desempenho com mesma ROM/cena e diferencie FPS pontual de média. Se RAM/CPU não forem acessíveis sem root, declare a lacuna.
9. O ajuste medido na Q60C reduziu memória WASM inicial de 128 para 32 MiB, mantendo crescimento automático. O script permite comparar os dois valores. Não transfira esse patch cegamente a outros cores ou prometa 60 FPS em toda TV.
10. Ao terminar, remova arquivos staging e processos temporários. Entregue comandos usados, versões e fontes, resultado observado, reversão e pendências. Se houver incompatibilidade, mostre o limite encontrado e uma alternativa real, sem inventar sucesso.

Trabalhe em português, explique as decisões em linguagem simples e execute o trabalho local reversível necessário. Não publique meu material nem faça commit por conta própria.
```
