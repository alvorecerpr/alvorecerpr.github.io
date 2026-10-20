#!/usr/bin/env python3
"""Gera as páginas do site da Alvorecer a partir de fonte/paginas/*.html e fonte/parcerias.json.

Uso: python3 fonte/gerar.py   (na raiz do repositório)

PREVIA = True enquanto o site estiver só no endereço provisório (alvorecerpr.github.io):
mostra a faixa de prévia com os marcadores amarelos e pede aos buscadores que não indexem.
Na virada para www.alvorecerpr.org.br, trocar para False, gerar de novo e conferir que não sobrou
nenhum marcador amarelo (o script avisa).
"""
import html, json, os, re, sys

PREVIA = True
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.join(RAIZ, "fonte")
SITE_URL = "https://www.alvorecerpr.org.br"

MENU = [
    ("quem-somos", "Quem somos"),
    ("o-que-fazemos", "O que fazemos"),
    ("transparencia", "Transparência"),
    ("como-ajudar", "Como ajudar"),
    ("contato", "Contato"),
    ("centro-espirita", "Centro Espírita"),
]

PAGINAS = {
    "inicio": ("Alvorecer Ação Social", "Desde 1992 no Bairro Alto, em Curitiba: convivência para crianças e adolescentes, aprendizagem profissional para jovens e trabalho com as famílias.", ""),
    "quem-somos": ("Quem somos", "História, departamentos, gestão 2026/2028 e documentos oficiais da Alvorecer Ação Social e Educacional.", ""),
    "o-que-fazemos": ("O que fazemos", "Serviço de Convivência e Fortalecimento de Vínculos, Programa de Aprendizagem e Grupo de Artesanato.", ""),
    "centro-espirita": ("Centro Espírita Irmã Scheilla", "Programação semanal e atividades gratuitas do Centro Espírita Irmã Scheilla, na Rua Guglielmo Marconi, 576, Bairro Alto.", "ceis"),
    "transparencia": ("Transparência", "Parcerias com o poder público (art. 11 da Lei 13.019/2014) e demonstrações contábeis da Alvorecer.", ""),
    "como-ajudar": ("Como ajudar", "Doe pelo Pix, conheça o bazar e seja voluntário da Alvorecer.", ""),
    "contato": ("Contato", "Endereço, telefone, e-mails por assunto e formulário de contato da Alvorecer.", ""),
    "privacidade": ("Política de privacidade", "Como a Alvorecer trata os dados enviados pelo site.", ""),
}


def cabecalho(atual):
    itens = []
    for slug, nome in MENU:
        cls = ' class="ceis-link"' if slug == "centro-espirita" else ""
        cur = ' aria-current="page"' if slug == atual else ""
        itens.append(f'        <li><a{cls} href="/{slug}/"{cur}>{nome}</a></li>')
    itens.append('        <li><a class="btn btn-sun" href="/como-ajudar/#doar">Doe agora</a></li>')
    return f'''<header class="site">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Alvorecer Ação Social - início"><img src="/assets/img/alvorecer-sol-marca.svg" alt="" width="82" height="42"><span class="bt"><b>Alvorecer</b><small>AÇÃO SOCIAL</small></span></a>
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="mainNav">Menu</button>
    <nav class="main" id="mainNav" aria-label="Principal">
      <ul>
{chr(10).join(itens)}
      </ul>
    </nav>
  </div>
</header>'''


RODAPE = '''<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <img class="flogo" src="/assets/img/alvorecer-logo-negativo.svg" alt="Alvorecer Ação Social" width="170" height="110">
        <h4>Alvorecer Ação Social e Educacional</h4>
        <p>CNPJ <span class="mono">68.591.445/0001-27</span></p>
        <p>Rua Pedro Eloy de Souza, 1141, Bairro Alto, Curitiba/PR, CEP 82820-130</p>
        <p><a class="mono" href="tel:+554133677132">(41) 3367-7132</a></p>
      </div>
      <div>
        <h4>Navegar</h4>
        <ul><li><a href="/quem-somos/">Quem somos</a></li><li><a href="/o-que-fazemos/">O que fazemos</a></li><li><a href="/transparencia/">Transparência</a></li><li><a href="/como-ajudar/">Como ajudar</a></li><li><a href="/contato/">Contato</a></li><li><a href="/centro-espirita/">Centro Espírita</a></li></ul>
      </div>
      <div>
        <h4>Ajude agora</h4>
        <ul><li><a href="/como-ajudar/#doar">Doe pelo Pix</a></li><li><a href="/como-ajudar/#bazar">Bazar</a></li><li><a href="/como-ajudar/#voluntario">Seja voluntário</a></li><li><a href="/o-que-fazemos/#empresas">Contrate um aprendiz</a></li></ul>
      </div>
    </div>
    <div class="fine">
      <span>Parcerias com o poder público divulgadas conforme o art. 11 da Lei 13.019/2014.</span>
      <a href="/privacidade/">Política de privacidade</a>
    </div>
  </div>
</footer>'''

FAIXA_PREVIA = '''<div class="proto" role="note">
  <div class="wrap">
    <span><b>Prévia do novo site, em revisão.</b> Trechos em amarelo ainda dependem de dado ou de decisão.</span>
    <label for="togglePend"><input type="checkbox" id="togglePend" checked> Mostrar pendências</label>
  </div>
</div>'''


def documento(slug, titulo, descricao, corpo, main_cls):
    titulo_full = titulo if slug == "inicio" else f"{titulo} | Alvorecer Ação Social"
    caminho = "/" if slug == "inicio" else f"/{slug}/"
    robots = '<meta name="robots" content="noindex, nofollow">\n' if PREVIA else ""
    canon = "" if PREVIA else f'<link rel="canonical" href="{SITE_URL}{caminho}">\n'
    main_attr = f' class="{main_cls}"' if main_cls else ""
    return f'''<!doctype html>
<html lang="pt-BR" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo_full)}</title>
<meta name="description" content="{html.escape(descricao)}">
{robots}{canon}<meta name="theme-color" content="#9E1B32">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(titulo_full)}">
<meta property="og:description" content="{html.escape(descricao)}">
<meta property="og:locale" content="pt_BR">
<link rel="icon" href="/assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/site.js" defer></script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
{FAIXA_PREVIA if PREVIA else ""}
{cabecalho(slug)}

<main id="conteudo"{main_attr}>
{corpo}
</main>

{RODAPE}
</body>
</html>
'''


def termos_html():
    d = json.load(open(os.path.join(FONTE, "parcerias.json"), encoding="utf-8"))
    pc = d["prestacao_contas"]

    def cell(n, label, conteudo, wide=False, inicio=False):
        cls = "cell" + (" wide" if wide else "") + (" row-start" if inicio else "")
        marca = f"<i>{n}</i>" if n else ""
        return f'<div class="{cls}"><small>{marca}{label}</small><div>{conteudo}</div></div>'

    blocos, saltos = [], []
    for t in d["parcerias"]:
        if t.get("equipe"):
            linhas = "".join(f"<tr><td>{a}</td><td>{b}</td><td class=\"n\">{c}</td></tr>" for a, b, c in t["equipe"])
            eq = ('<div class="tbl-wrap"><table><thead><tr><th>Função</th><th>Jornada</th><th class="n">Remuneração mensal prevista</th></tr></thead>'
                  f'<tbody>{linhas}</tbody></table></div><p class="muted" style="margin-top:8px">Total previsto com a equipe: <b>{t["equipeTotal"]}</b></p>')
            if t.get("equipeNota"):
                eq += f'<p class="muted" style="font-size:.88rem;margin-top:4px">{t["equipeNota"]}</p>'
        else:
            eq = "<p>Não há equipe paga com recursos desta parceria.</p>"
        status = t.get("statusText") or f'{t["status"]} até {t["vigencia"].split(" a ")[1]}'
        partes = [
            cell("I", "Assinatura", t["assinatura"], inicio=True),
            cell("I", "Vigência", t["vigencia"]),
            cell("IV", "Origem do recurso", t["origem"]),
            cell("I", "Órgão responsável", t["orgao"], True),
            cell("III", "Objeto", t["objeto"], True),
            cell("IV", "Valor total", f'<span class="big tnum">{t["valor"]}</span>', inicio=True),
            cell("IV", "Valor liberado", f'<span class="big tnum">{t["liberado"]}</span><span class="muted" style="display:block;font-size:.9rem">{t["libnota"]}</span>'),
            cell("V", "Prestação de contas", pc),
        ]
        if t.get("nota"):
            partes.append(cell("", "Observação", t["nota"], True))
        partes.append(cell("VI", "Equipe paga com recursos da parceria", eq, True))
        partes.append(cell("II", "Organização", 'Alvorecer Ação Social e Educacional · CNPJ <span class="mono">68.591.445/0001-27</span>', True))
        blocos.append(f'<article class="termo" id="{t["id"]}"><header><div><div class="id">{t["num"]}</div><h3>{t["nome"]}</h3></div>'
                      f'<span class="status {t.get("statusCls", "vig")}">{status}</span></header><div class="grid">{"".join(partes)}</div></article>')
        curto = t["num"].replace("Termo de Colaboração", "TC").replace("Termo de Fomento", "TF")
        saltos.append(f'<li><a href="#{t["id"]}">{curto}</a></li>')
    return "\n".join(blocos), "".join(saltos)


def gravar(caminho_rel, conteudo):
    destino = os.path.join(RAIZ, caminho_rel)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(conteudo)


def main():
    pend_total = 0
    for slug, (titulo, desc, cls) in PAGINAS.items():
        corpo = open(os.path.join(FONTE, "paginas", f"{slug}.html"), encoding="utf-8").read().rstrip()
        if slug == "transparencia":
            termos, saltos = termos_html()
            corpo = corpo.replace("%%TERMOS%%", termos).replace("%%SALTOS%%", saltos)
        if "%%" in corpo:
            sys.exit(f"Marcador não substituído em {slug}")
        pend_total += len(re.findall(r'class="[^"]*\bpend(-box)?\b', corpo)) + corpo.count("class='pend'")
        doc = documento(slug, titulo, desc, corpo, cls)
        gravar("index.html" if slug == "inicio" else f"{slug}/index.html", doc)

    nf = '''<div class="wrap nf stack">
  <span class="eyebrow">Página não encontrada</span>
  <h1>Este endereço não existe ou mudou de lugar</h1>
  <p class="lead">Volte para o <a href="/">início</a> ou use o menu acima.</p>
</div>'''
    gravar("404.html", documento("404", "Página não encontrada", "Página não encontrada.", nf, ""))
    gravar("robots.txt", "User-agent: *\nDisallow: /\n" if PREVIA else f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    if not PREVIA:
        urls = "".join(f"  <url><loc>{SITE_URL}{'/' if s == 'inicio' else '/' + s + '/'}</loc></url>\n" for s in PAGINAS)
        gravar("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print(f"Páginas geradas: {len(PAGINAS)} + 404. Marcadores de pendência: {pend_total}.")
    if not PREVIA and pend_total:
        print("ATENÇÃO: versão final com marcadores de pendência. Resolva antes de publicar.")


if __name__ == "__main__":
    main()
