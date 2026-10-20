# Site da Alvorecer Ação Social e Educacional

Site institucional da Alvorecer Ação Social e Educacional (CNPJ 68.591.445/0001-27), Curitiba/PR.
Endereço definitivo: www.alvorecerpr.org.br. Endereço provisório: alvorecerpr.github.io.

## Regra do repositório

Este repositório é público. Só entra aqui o que vai ao site. Planilhas, dados de empregados,
rascunhos, pendências internas e fotos sem o rosto protegido de crianças e adolescentes não
entram, nem por um instante: o que é enviado fica no histórico mesmo depois de apagado.

## Como está organizado

- `fonte/paginas/` - o conteúdo de cada página (só o miolo, sem cabeçalho e rodapé).
- `fonte/parcerias.json` - os dados das parcerias com o poder público (página Transparência, art. 11 da Lei 13.019/2014).
- `fonte/gerar.py` - monta as páginas finais (`index.html` e as pastas de cada página) com o cabeçalho e o rodapé comuns.
- `assets/` - estilo, script, fontes (licença OFL) e imagens da marca (Manual da marca v1.0).

Depois de alterar qualquer arquivo de `fonte/`, rode `python3 fonte/gerar.py` na raiz e envie o resultado.

## Prévia

Enquanto `PREVIA = True` em `fonte/gerar.py`, o site mostra a faixa de prévia, marca em amarelo
o que ainda depende de dado ou de decisão e pede aos buscadores que não indexem as páginas.
Na virada para o domínio definitivo, trocar para `False`, gerar de novo e conferir que não sobrou
nenhum marcador.
