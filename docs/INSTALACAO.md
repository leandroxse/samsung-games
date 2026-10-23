# Montagem e instalação

Este roteiro reproduz o protótipo registrado em [`README.md`](../README.md). Ele foi validado na TV Samsung QN50Q60CAGXZD autorizada. O fluxo de instalação de outra TV depende do modelo, da versão do Tizen e das ferramentas disponíveis naquela rede.

## Antes de começar

Tenha no computador:

- Python 3;
- Floating IPS v198 (`flips`) no `PATH`;
- o WGT RetroArch Tizen v0.3.2 salvo como `artifacts/RetroArch-v0.3.2.wgt`;
- ROM original e patch BPS obtidos por você;
- certificado de autor e distribuidor Tizen que aceite instalar apps na TV;
- acesso ao instalador local já usado para a TV.

Não coloque ROM, patch, WGT assinado, binário ou certificado no Git. Confira o alvo antes de qualquer operação privilegiada. A QN50Q60CAGXZD é o único aparelho autorizado neste registro.

## Preparar e empacotar

1. Aplique patch à ROM que você possui:

   ```bash
   tools/prepare-rom.sh \
     "/caminho/para/Super Mario World (USA).sfc" \
     "/caminho/para/SMW-PTBR-2.0.bps"
   ```

   O resultado deve existir em `roms/SMW-PTBR-2.0.sfc`. Floating IPS valida a ROM de entrada. Não ignore erro de checksum.

2. Confirme que o WGT base existe. O empacotador baixa os recursos públicos ausentes para `.work/offline-assets/`.

3. Configure `TIZEN_SDB` com o caminho de `tizen-sdb` e `TIZEN_CERT_DIR` com a pasta do seu perfil privado. Essa pasta contém `author.p12`, `distributor.p12` e `password.txt`. A senha não é registrada no Git nem impressa.

4. Gere o pacote:

   ```bash
   TIZEN_SDB="$HOME/TizenTube/tools/tizen-sdb" \
   TIZEN_CERT_DIR="/caminho/para/seu/perfil-de-assinatura" \
   python3 tools/build-smw.py
   ```

   Saída: `artifacts/SuperNintendo-SMW-PTBR.wgt`. Pacote Tizen: `RtArchTzn0`. Aplicativo: `RtArchTzn0.RetroArch`.

## Instalar na TV testada

Redescubra o IP por DHCP e confira a identidade antes de instalar:

```bash
curl -fsS "http://<IP_TV>:8001/api/v2/" \
  | jq '.device|{modelName,developerMode,developerIP}'
```

Confirme `modelName` como `QN50Q60CAGXZD`, modo de desenvolvedor ativo e endereço atual. Não reutilize IP antigo nem opere outro aparelho.

Na Q60C deste registro, o instalador do Vetro local recebe o WGT no caminho temporário da TV e instala via SDB local. Exemplo da etapa de instalação, depois que o arquivo já estiver em staging:

```bash
curl -fsS -X POST "http://<IP_TV>:8099/install" \
  -H 'Content-Type: application/json' \
  --data '{"path":"/home/owner/share/tmp/sdk_tools/samsung-games-SMW-final.wgt"}'
```

O corpo retorna resultado do instalador; confirme também no inventário SDB e abra o app. A abertura real deve mostrar a interface em primeiro plano. `tizen.application.launch()` sozinho não comprova foco.

O transporte do arquivo para staging depende da ferramenta já configurada nessa TV. Na rede testada, a conexão SDB direta do computador falhava porque o IP autorizado do PC não correspondia ao endereço exigido pela TV. O processo concluído usou o SDB local pela API Vetro existente e removeu os arquivos temporários depois. Não altere IP, rota ou firewall sem medir e limpar a alteração ao final.

## Validar e remover

Verifique imagem, som, entrada do controle, pause/retomada, savestate e SRAM. Faça uma abertura offline para confirmar que ROM, core e recursos estão empacotados. Registre carga e duração do teste; uma leitura pontual de FPS não prova estabilidade.

Comando de remoção deste pacote, via shell root já configurado na TV:

```bash
pkgcmd -u -n RtArchTzn0 --global
```

A remoção apaga os dados privados do app. Exporte os arquivos de save antes de remover ou atualizar por um método que apague dados. Confirme no inventário que `RtArchTzn0` saiu. Não remova outros pacotes.

## Arquivos de dados

O jogo guarda os saves no armazenamento persistente do navegador, em diretórios separados para SRAM e savestates. No teste realizado:

```text
/home/web_user/retroarch/userdata/saves/Snes9x 2010/SMW-PTBR-2.0.srm
/home/web_user/retroarch/userdata/states/Snes9x 2010/SMW-PTBR-2.0.state
```

Salvar, fechar e reabrir foram verificados. Reinício físico da TV e exportação foram deixados em aberto.
