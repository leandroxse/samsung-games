# Prompt: emulação de Super Nintendo na minha TV

Copie o bloco inteiro para uma IA que tenha acesso ao computador e às ferramentas locais. Anexe ou indique apenas ROMs e patches que você tem direito de usar.

```text
Quero instalar um aplicativo de Super Nintendo na minha TV e jogar sem deixar o computador ligado. Conduza o trabalho até uma prova real de imagem, som, controles, saves e consumo.

Trabalhe em pt-BR. Inspecione apenas o necessário. Execute trabalho local reversível sem pedir confirmação. Não faça commit, não atualize firmware, não instale serviço residente e não altere configurações de rede de forma persistente.

FLUXO

1. IDENTIFICAR TV
   - Leia minhas notas locais de Obsidian sobre a TV e ferramentas existentes antes de operar o aparelho.
   - Confirme o modelo e sistema pela API local da TV. Redescubra o IP atual; DHCP pode mudar.
   - Pare se a TV não for o aparelho que autorizei. Não opere TV de terceiros.
   - Levante CPU, GPU, RAM disponível, armazenamento livre, versão do navegador, resolução e método de instalação já disponível.

2. PREPARAR ENTRADAS
   - Localize a ROM e o patch que eu forneci. Se não encontrar, peça somente o caminho; não baixe jogo, BIOS ou ROM.
   - Confira formato, checksum e tamanho. Preserve os originais.
   - Use a ROM apenas para esta instalação local. Não coloque ROM, patch, BIOS, certificados ou senhas em Git.

3. COMPARAR CAMINHOS
   - Monte pelo menos três candidatas: (a) emulador WASM/libretro num WGT Tizen; (b) app web com recursos locais; (c) emulador nativo compatível com a TV. Inclua Moonlight só como referência se já estiver instalado, explicando que exige outra máquina ligada. Você pode acrescentar uma candidata melhor.
   - Para cada candidata, registre dependências, compatibilidade, rede necessária durante o jogo, consumo provável e forma de remover.
   - Escolha as candidatas que possam ser provadas com ferramentas existentes. Meça na própria TV; não escolha só por familiaridade.

4. CONSTRUIR E MEDIR
   - Prefira reusar projeto existente se mantido, compatível e pequeno. Registre origem, versão e licença.
   - Faça build reproduzível. Recursos do jogo devem ficar na TV após instalar; PC não deve servir conteúdo durante a partida.
   - Meça baseline e cada candidata com mesma ROM, cena, resolução, app em primeiro plano e coleta. Registre FPS, CPU e RAM disponíveis, duração e método. Diferencie observação pontual de média.
   - Se uma candidata falhar, capture causa curta e passe à seguinte. Não deixe mudança temporária de rede, processo de teste ou arquivo staging.

5. INSTALAR E PROVAR
   - Antes de instalar, anote ID do pacote e comando de remoção.
   - Instale somente na TV confirmada. Confirme inventário, visibilidade e foco em primeiro plano; sucesso do comando launch sozinho não prova abertura.
   - Teste imagem, áudio, controle físico, pausa, SRAM, savestate e abertura sem internet depois do primeiro carregamento.
   - Registre resultado, consumo e limitações. Não diga que funciona para todos os jogos com base em uma ROM.

6. ENTREGAR
   - Organize script de build, documentação passo a passo, prompt reutilizável, resultados medidos e comando de reversão.
   - Ignore no Git ROMs, patches, BIOS, WGTs, binários, credenciais e dados privados.
   - Termine com o que instalou, evidência observada, consumo medido, arquivos criados e testes ainda pendentes.

ATALHO DE DECISÃO

Identidade confirmada?
  não -> pare.
  sim -> notas locais + recursos da TV -> ROM do usuário -> três candidatas
       -> medir na TV -> candidata atende sem PC durante jogo?
            não -> mostrar limite e parar sem instalar.
            sim -> anotar reversão -> instalar -> provar imagem, áudio,
                   controle, saves, offline e consumo -> limpar temporários.

Não invente capacidade, compatibilidade, checksum, resultado de teste ou nome de ferramenta. Se faltar informação que muda a segurança ou a arquitetura, faça uma pergunta curta e continue o trabalho independente.
```

## Como adaptar

Troque “minha TV” pelo modelo exato somente depois de conferir o aparelho. Mantenha o requisito de ROM fornecida pelo usuário, medição física e comando de remoção. O prompt não substitui a validação na sua TV.
