# Desigualdades no esgotamento sanitário brasileiro (SINISA 2024)

![Código MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-blue) ![Dados CC-BY 4.0](https://img.shields.io/badge/dados-CC--BY%204.0-lightgrey) ![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB) ![FAIR](https://img.shields.io/badge/FAIR-compliant-009E73)

**Artigo publicado:** https://pedrohenriquesgoncalves-lang.github.io/esgotamento_sanitario_trabalho/

**Repositório:** https://github.com/pedrohenriquesgoncalves-lang/esgotamento_sanitario_trabalho

**Autoria:** Pedro Henrique dos Santos Gonçalves · [Integrante 2] · [Integrante 3]
**Instituição:** Unilasalle (Rio de Janeiro), Bacharelado em Sistemas de Informação, 6º período, 2º semestre de 2026
**Disciplina:** Linguagem de Programação (Análise e Visualização de Dados com Python)

## Resumo executivo

Análise da base municipal do módulo Esgoto do SINISA (ano de referência 2024; 3.903 municípios, 188,3 milhões de habitantes). Resultados principais: 62,3% da população tem rede coletora (reproduz o indicador oficial); o Sudeste atende 81,9% e o Norte 24,7%; só 16,9% dos municípios com dado atingem 90% de coleta; 1.154 municípios (14,6 milhões de habitantes) não têm dados; natureza jurídica e desempenho financeiro associam-se a cobertura e tratamento (associações descritivas, não causais).

**Palavras-chave:** esgotamento sanitário; SINISA; desigualdade regional; engenharia de dados; ciência aberta.

## Perguntas de pesquisa

1. **RQ1** — Quão desigual é o atendimento com coleta e tratamento entre macrorregiões, UFs e portes de município?
2. **RQ2** — A natureza jurídica do prestador está associada a diferenças de cobertura e de tratamento?
3. **RQ3** — O desempenho financeiro do serviço se relaciona com a cobertura e o tratamento?

## Resultados principais

| Indicador | Valor |
| --- | --- |
| Municípios na base (com dado de esgoto) | 3.903 (2.749) |
| População coberta pela base | 188,3 milhões (14,6 milhões em municípios sem dado) |
| População com rede coletora | 117,3 milhões (62,3%) |
| Estimativa de coleta com tratamento | 52,0% |
| Atendimento por macrorregião | Norte 24,7% · Nordeste 35,9% · Centro-Oeste 68,3% · Sul 57,7% · Sudeste 81,9% |
| Municípios com dado que atingem 90% de coleta | 462 (16,9%) |
| Natureza jurídica × cobertura / tratamento (Kruskal-Wallis, ε²) | 0,13 / 0,31 |
| Desempenho financeiro × tratamento (Spearman) | ρ = 0,32 |

O artigo traz 7 figuras (4 estáticas em Matplotlib e 3 interativas em Plotly) e 6 tabelas; todos os números estão em `docs/assets/resultados.json`.

## Estrutura

```
├── README.md · LICENSE (MIT) · LICENSE-DATA.md (CC-BY 4.0)
├── requirements.txt          # dependências com versões congeladas (pip freeze)
├── .gitignore · pytest.ini
├── data/raw/                 # planilhas originais do SINISA (não alteradas; SHA-256 no log)
├── data/processed/           # municipios_esgoto_2024 (.parquet e .csv.gz) + etl_log.json
├── data/data_dictionary.md   # dicionário de dados (gerado pelo ETL)
├── notebooks/analise_exploratoria.ipynb
├── src/etl.py                # pipeline determinístico  |  src/run_notebook.py
├── tests/test_etl.py         # 4 testes, rodados no CI (.github/workflows/ci.yml)
├── uml/diagramas.md          # diagramas UML (Mermaid)
└── docs/                     # artigo (index.html) e figuras (assets/) — GitHub Pages
```

## Como reproduzir

```bash
git clone https://github.com/pedrohenriquesgoncalves-lang/esgotamento_sanitario_trabalho.git
cd esgotamento_sanitario_trabalho
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.etl            # data/processed/, etl_log.json, data_dictionary.md
pytest -q                    # valida o pipeline
python -m src.run_notebook   # regenera as figuras em docs/assets/
```

## Qualidade e validação

- **Universo:** 3.903 municípios da base técnica; a coluna `tem_dado_esgoto` separa os 2.749 com indicadores dos 1.154 sem dado (que entram no denominador como não atendidos, como faz o SINISA).
- **Validação cruzada:** o atendimento recalculado a partir da base municipal reproduz o indicador oficial do Brasil (62,3%) e das 27 UFs, com erro médio absoluto de 0,002 ponto percentual.
- **Rastreabilidade:** valores "Não calculado" viram `NaN` e são contados por motivo em `data/processed/etl_log.json`; nenhum dado bruto é alterado e nenhuma linha é descartada.
- **Testes:** `pytest -q` roda 4 testes (universo, faixa 0–100%, validação contra o oficial, tipos) e o mesmo roda automaticamente no GitHub Actions a cada push.
- **Diagramas:** fluxo de dados, sequência do ETL e modelo de dados em `uml/diagramas.md`.

## Fonte dos dados

Ministério das Cidades — SINISA, módulo Esgotamento Sanitário, ano de referência 2024 (publicação em 18/12/2025): https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa. Arquivos usados: *Indicadores – Base Municipal*, *Gestão Técnica de Esgoto – Base Municipal* e *Indicadores – UF/MR/BR* (validação). Dicionário oficial das variáveis: [Glossário de informações – Esgoto 2024](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/area-do-prestador/arquivos/GlossrioInformaes_ESGOTO_2024.pdf); dicionário do projeto em `data/data_dictionary.md`.

## Licenças

Código: MIT (`LICENSE`). Dados derivados, figuras e texto: CC-BY 4.0 (`LICENSE-DATA.md`). Cite a fonte original (Ministério das Cidades/SINISA).
