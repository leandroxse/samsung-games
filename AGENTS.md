# Samsung Games

Fale em pt-BR. Este projeto explora emulação local em Samsung Smart TVs com Tizen. Leia `README.md` e a documentação relevante antes de alterar o fluxo.

## Alvo e segurança

- A prova publicada foi medida em Samsung QN50Q60CAGXZD com Tizen 9.0. Não presuma compatibilidade com outros modelos.
- Antes de operar uma TV, confirme o modelo, o endereço atual e a autorização explícita. Não opere aparelho de terceiros.
- Não atualize firmware, altere debloat, instale serviço residente ou crie hook de boot.
- Toda instalação precisa registrar ID do pacote e comando reversível de remoção.
- Faça alterações de rede somente se necessárias, temporárias e com limpeza após o uso.

## ROMs e arquivos privados

- O usuário fornece ROMs, patches e BIOS. Nunca baixe jogos ou BIOS.
- Não versione ROM, patch, BIOS, WGT assinado, binário, certificado, senha, saves ou capturas privadas. Consulte `.gitignore`.
- Não imprima nem registre senha de assinatura. Use caminho de certificado configurado por ambiente.

## Desenvolvimento

- Reuse os scripts e ferramentas existentes. Prefira mudanças pequenas e reversíveis.
- Meça consumo na própria TV, com carga equivalente, e descreva o cenário e limites da medição.
- Sucesso de chamada de abertura não prova primeiro plano; confirme visibilidade e foco na TV.
- `AGENTS.md` e `CLAUDE.md` devem permanecer idênticos.
- Commits usam `tipo(escopo): assunto`. Não publique binários junto com código.
