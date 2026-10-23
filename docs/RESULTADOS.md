# Resultados medidos

Medições desta prova na QN50Q60CAGXZD. Valores descrevem as coletas listadas; não prometem desempenho em outros jogos, TVs ou sessões.

## TV e orçamento

| Recurso | Leitura confirmada |
|---|---|
| Modelo | Samsung QN50Q60CAGXZD |
| Plataforma | `23_NKL_UHD_T09`, Tizen 9.0.0 |
| Firmware | `T-NKLCUABC-0090-2220.4` |
| CPU | 4 núcleos Cortex-A72 expostos; ambiente reporta `armv7l` |
| GPU | Mali-G31, um núcleo reportado pelo driver |
| RAM total | 1.423 MiB |
| RAM disponível | cerca de 260–400 MiB com Home ativa, conforme a carga |
| Armazenamento livre | cerca de 895 MiB a 1 GiB, conforme a leitura |
| Chromium | 120.0.6099.5 |

RAM e armazenamento mudam com a atividade da TV. O sistema raiz é somente leitura; dados ficam em `/home/owner/share/` ou `/opt/`. Não instale serviço residente, hook de boot, firmware ou alteração de debloat.

## Candidatas

| Abordagem | Resultado nesta rodada |
|---|---|
| WGT RetroArch com core WASM local | Escolhida para a prova porque reutiliza integração Tizen disponível e permite empacotar ROM, core e recursos. |
| App web hospedado fora da TV | Não implementada. Um servidor durante o jogo não atende ao uso sem PC. |
| Port nativo ARM | Não implementado. ABI, vídeo, áudio e controles ainda precisariam de prova. |
| Moonlight | Não serve à execução local; streaming exige outra máquina rodando o jogo. |

A comparação entre arquiteturas não está concluída. As três medições de core abaixo comparam opções dentro do WGT, não arquiteturas de execução.

## Ajuste de memória e desempenho

Os cores upstream testados iniciavam com 128 MiB de memória linear WASM. Com Snes9x 2010, o contador mostrou 39,24 FPS em 720p. Snes9x atual marcou 41,16 FPS em 1080p e 41,95 FPS em 720p. Snes9x 2005 marcou 40,74 FPS em 720p. Essas leituras são pontuais de captura.

Um perfil de CPU mostrou coleta de lixo como a maior amostra individual. O empacotador reduz o mínimo inicial da memória WASM para 32 MiB e mantém o crescimento automático. O patch valida o cabeçalho, flags, tamanho do campo e mínimo esperado; falha se o layout do core mudar. O código do emulador não é alterado.

Com Snes9x 2010 ajustado, uma captura marcou **60,05 FPS**. O heap chegou a **38,4375 MiB**, então 32 MiB é mínimo inicial, não limite. Em 12 amostras finitas, RAM disponível média foi **262,92 MiB**, mínima **257,02 MiB**; CPU global média foi **46,40%**. Na coleta do core upstream, CPU global média foi **82,65%** e RAM disponível média **247,99 MiB**.

As coletas ocorreram com a mesma ROM em primeiro plano e inspector ativo. A atividade do sistema e o trecho variam; não compare os valores como benchmark isolado nem generalize para uma sessão longa. A imagem e o áudio foram confirmados pelo usuário.

## Validações realizadas

- ROM patchada de arquivo fornecido pelo usuário; Floating IPS aceitou a ROM de origem.
- JavaScript, XML e WASM passaram validação local; o WASM final passou em `WebAssembly.validate`.
- App final 0.3.4 instalado e confirmado em primeiro plano na TV autorizada.
- ROM, core e recursos carregaram após recarga com a rede do app bloqueada via CDP.
- SRAM e savestate foram gravados e restaurados após reabertura.
- Monitor Moonlight e arquivos temporários de staging foram removidos após o teste.

## Pendências

- Validar controle físico e mapeamento de botões.
- Fazer sessão longa e reinício físico da TV.
- Testar jogos com outros chips e cargas gráficas.
- Medir outras arquiteturas se houver motivo para concluir comparação.

Verificação anterior de curto prazo não substitui esses testes. Relatórios brutos e capturas usados na rodada ficam em `artifacts/` local e são ignorados pelo Git.
