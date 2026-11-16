[README.md](https://github.com/user-attachments/files/34926794/README.md)
# Desigualdades no esgotamento sanitário brasileiro (SINISA 2024)

![Código MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-blue) ![Dados CC-BY 4.0](https://img.shields.io/badge/dados-CC--BY%204.0-lightgrey) ![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB) ![FAIR](https://img.shields.io/badge/FAIR-compliant-009E73)

**Artigo publicado:** https://SEU-USUARIO.github.io/sinisa-esgoto-2024/

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

## Estrutura

```
├── data/raw/                 # planilhas originais do SINISA (não alteradas; SHA-256 no log)
├── data/processed/           # Parquet + CSV.gz + etl_log.json
├── data/data_dictionary.md   # dicionário de dados (gerado pelo ETL)
├── notebooks/analise_exploratoria.ipynb
├── src/etl.py                # pipeline determinístico  |  src/run_notebook.py
├── tests/test_etl.py         # 4 testes, rodados no CI (.github/workflows/ci.yml)
├── uml/diagramas.md          # diagramas UML (Mermaid)
└── docs/                     # artigo (index.html) e figuras (assets/) — GitHub Pages
```

## Como reproduzir

```bash
git clone https://github.com/SEU-USUARIO/sinisa-esgoto-2024.git
cd sinisa-esgoto-2024
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.etl            # data/processed/, etl_log.json, data_dictionary.md
pytest -q                    # valida o pipeline
python -m src.run_notebook   # regenera as figuras em docs/assets/
```

## Fonte dos dados

Ministério das Cidades — SINISA, módulo Esgotamento Sanitário, ano de referência 2024 (publicação em 18/12/2025): https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa. Arquivos usados: *Indicadores – Base Municipal*, *Gestão Técnica de Esgoto – Base Municipal* e *Indicadores – UF/MR/BR* (validação).

## Licenças

Código: MIT (`LICENSE`). Dados derivados, figuras e texto: CC-BY 4.0 (`LICENSE-DATA.md`). Cite a fonte original (Ministério das Cidades/SINISA).
