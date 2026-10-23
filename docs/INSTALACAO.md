# Da sua TV ao primeiro jogo

O ponto de partida é a sua Samsung e o seu computador. Você não precisa reproduzir a rede, as notas ou os certificados de quem criou o projeto. A Q60C é nosso caso medido, não uma restrição de modelo para quem quer experimentar.

## 1. Descubra o que você tem

Anote modelo completo, versão do Tizen, IP atual e sistema do computador. Confira essas informações nas configurações da TV. Se a API de identificação estiver disponível, `http://IP_DA_TV:8001/api/v2/` também ajuda; sua ausência não prova incompatibilidade.

O [RetroArch Tizen upstream](https://github.com/Sype0/retroarch-tizen#compatibility) declara Chromium 85 ou mais recente, associado a Tizen 6.5+. Use isso como requisito declarado, não como teste físico de todos os modelos. TVs anteriores ao Tizen não executam este WGT. Se a versão for antiga, avalie outro runtime antes de instalar qualquer coisa. Não atualize firmware apenas para seguir este guia.

## 2. Obtenha as ferramentas na fonte

| Ferramenta | Onde obter | Quando precisa |
|---|---|---|
| Git | [git-scm.com](https://git-scm.com/downloads) | Clonar este repositório |
| Python 3 | [python.org](https://www.python.org/downloads/) | Executar o empacotador, sem bibliotecas extras |
| Tizen Studio, TV Extension e Certificate Extension | [Samsung: instalar TV SDK](https://developer.samsung.com/smarttv/develop/getting-started/setting-up-sdk/installing-tv-sdk.html) | Caminho oficial de assinatura e instalação; inclui SDB e CLI |
| Certificado Samsung | [Samsung: criar certificados](https://developer.samsung.com/smarttv/develop/getting-started/setting-up-sdk/creating-certificates.html) | Autorizar o pacote para o seu aparelho |
| RetroArch Tizen | [código](https://github.com/Sype0/retroarch-tizen), [releases](https://github.com/Sype0/retroarch-tizen/releases) | App original com vários sistemas; base do nosso pacote SNES |
| TizenBrew | [repositório e instalação](https://github.com/reisxd/TizenBrew) | Alternativa quando esse ambiente já está instalado ou for escolhido |
| Floating IPS | [releases oficiais](https://github.com/Sir-Walrus/Flips/releases) | Somente se você quiser aplicar um patch IPS/BPS |

Escolha os instaladores adequados a Windows, Linux ou macOS e confira os requisitos atuais da fonte. Não copie executáveis desconhecidos nem reutilize certificado de outra pessoa. Contas, certificados e a autorização do dispositivo são seus.

## 3. Escolha o caminho mais curto

**Quer experimentar vários sistemas?** Comece pelas instruções do [RetroArch Tizen original](https://github.com/Sype0/retroarch-tizen#installation). Se já usa TizenBrew, o módulo indicado pelo autor é `gh/Sype0/retroarch-tizen`; o WGT original também está nas releases. Esse app baixa cores pela internet. Não confunda esse comportamento com o pacote offline deste repositório.

**Quer um pacote local com uma ROM SNES?** Use o empacotador abaixo. Ele inclui core, ROM e recursos no WGT e permite comparar Snes9x atual, 2010 e 2005. O pacote tem uma entrada de jogo, não uma biblioteca de várias ROMs. Cada ROM recebe um nome interno derivado do conteúdo para separar seus saves dos de outro jogo; isso não migra automaticamente saves da prova antiga.

**Quer outro emulador?** Procure uma versão ou port compatível com o sistema da sua TV. Um APK de Android não instala no Tizen. Registre origem, licença e método de instalação; faça um teste pequeno antes de portar ou recompilar. Não é necessário refazer uma comparação extensa quando já existe uma opção compatível e suficiente.

## 4. Gere o pacote local de SNES

```bash
git clone https://github.com/leandroxse/samsung-games.git
cd samsung-games
python3 tools/build-smw.py --rom "/caminho/Meu jogo.sfc" --name "Meu jogo" --unsigned
```

No Windows, `py -3` pode substituir `python3`. Use o terminal na pasta clonada. O script obtém automaticamente a release base v0.3.2 e recursos públicos ausentes; cache e saída ficam fora do Git. A ROM precisa ser um arquivo extraído `.sfc` ou `.smc` compatível com o core. Nenhuma ROM é baixada.

Opções disponíveis:

```bash
python3 tools/build-smw.py --help
python3 tools/build-smw.py --rom "/caminho/Meu jogo.sfc" --core snes9x2010 --initial-memory 32 --unsigned --output artifacts/meu-jogo.wgt
```

`--core` aceita `snes9x`, `snes9x2010` e `snes9x2005`. `--initial-memory 128` mantém o mínimo upstream para comparação. O preset de canvas usa 1280×720 ampliado para viewport lógico de 1920×1080, como no teste; confira enquadramento em outra TV. Cores e recursos vêm do servidor upstream e podem mudar; guarde versões e hashes quando precisar repetir uma medição.

O nome `build-smw.py` foi mantido por compatibilidade, mas a ROM não precisa ser Mario nem ter tradução. `tools/prepare-rom.sh` é apenas o exemplo opcional de aplicar uma tradução BPS de SMW com Floating IPS no Linux/macOS; no Windows, use o Floating IPS adequado ao sistema.

## 5. Assine e conecte a sua TV

O pacote gerado com `--unsigned` **não está pronto para instalar**. Use o perfil Samsung criado para sua TV. Siga o [guia oficial de conexão](https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html): modo de desenvolvedor, IP do computador, reinício solicitado pela configuração e conexão no Device Manager. Não exige root nem Vetro.

Com Web CLI e o perfil configurados, confira a sintaxe na [documentação Samsung de linha de comando](https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/command-line-interface.html). Exemplo de assinatura do pacote já gerado:

```bash
python3 -m zipfile -e artifacts/meu-jogo.wgt .work/meu-jogo
tizen package -t wgt -s "SEU_PERFIL" -- .work/meu-jogo
```

A CLI precisa estar no PATH; use o executável instalado pelo SDK no seu sistema. No Device Manager, obtenha o nome do alvo e use “Permit to install applications” quando exigido pelo fluxo do certificado.

A assinatura automática antiga continua opcional: se você já tem um utilitário compatível com `tizen-sdb resign` e arquivos `author.p12`, `distributor.p12`, `password.txt`, configure `TIZEN_SDB` e `TIZEN_CERT_DIR` e omita `--unsigned`. Esse utilitário pessoal não é distribuído aqui e não é pré-requisito; o caminho público recomendado é o SDK acima.

## 6. Instale, jogue e confira

Antes de instalar, anote: pacote `RtArchTzn0`, aplicativo `RtArchTzn0.RetroArch`. Esse ID também é usado pelo upstream: exporte saves antes de substituir uma instalação existente. Pacotes gerados para outros jogos compartilham o mesmo ID e não se instalam lado a lado.

Pelo SDK, use o nome do WGT assinado informado pela etapa anterior e o alvo do Device Manager (`sdb devices` também lista os alvos):

```bash
tizen install -n NOME_GERADO.wgt -t NOME_DA_TV -- .work/meu-jogo
```

Confirme o resultado na TV. Abra o aplicativo e verifique imagem, áudio, enquadramento, botões e saves. Faça uma abertura com a conexão do app indisponível para verificar os arquivos locais. Esse caminho oficial está documentado pela Samsung; nesta prova específica, a instalação física usou uma integração Vetro/SDB que já existia. O fluxo do SDK não foi reexecutado aqui em outra TV.

A remoção pode ser feita pelo gerenciador de aplicativos da TV. Tirar um atalho da Home não é desinstalar: confira que o pacote saiu. **Desinstalar pode apagar saves**; exporte-os antes. A preservação na atualização depende da assinatura e do método usado.

## Se algo não funcionar

- **Não conecta:** confira IP atual, rede e IP do computador no modo de desenvolvedor. Não abra portas para a internet.
- **Instalação rejeitada:** confira perfil, DUID, autorização de instalação e assinatura; não compartilhe certificado ou senha.
- **Abre a interface, mas falha no jogo:** confira versão do navegador, WASM/WebGL, extensão e ROM compatível com o core.
- **Áudio falha ou jogo fica lento:** compare cores e memória inicial, com o mesmo trecho de jogo. Não aplique o ajuste de SNES cegamente a outros cores.
- **Não há métrica de RAM/CPU acessível:** registre essa limitação. Não faça root apenas para completar um relatório.

Os números medidos e as pendências do primeiro aparelho estão em [RESULTADOS.md](RESULTADOS.md).
