# Dicionário de dados — SINISA Esgoto 2024 (base municipal)

Arquivo: `data/processed/municipios_esgoto_2024.parquet` (e `.csv.gz`). 1 linha = 1 município da base técnica (3.903 linhas; 2.749 com dados de esgoto, ver `tem_dado_esgoto`). Gerado automaticamente por `src/etl.py`.

Valores originais `Não calculado (...)` viram vazios (NaN); os motivos estão em `data/processed/etl_log.json`.

| Variável | Significado | Tipo | Unidade / formato | Origem |
| --- | --- | --- | --- | --- |
| `cod_ibge` | Código IBGE do município (7 dígitos) | string | chave primária | SINISA (cadastro) |
| `tem_dado_esgoto` | Município possui dados de esgoto na base de indicadores do SINISA 2024 | bool | derivada; False = município listado na base técnica sem informação do prestador | derivada |
| `macrorregiao` | Macrorregião do município | string | Norte, Nordeste, Centro-Oeste, Sudeste, Sul | SINISA (cadastro) |
| `municipio` | Nome do município | string | texto | SINISA (cadastro) |
| `uf` | Unidade da Federação | string | sigla de 2 letras | SINISA (cadastro) |
| `capital` | Município é capital de UF | bool | True/False | SINISA (cadastro) |
| `rm_ride` | Região Metropolitana ou RIDE do município | string | nome ou 'Fora de RM/RIDE' | SINISA (cadastro) |
| `natureza_juridica` | Natureza jurídica do(s) prestador(es) (CAD0002) | string | 'A | B' quando há vários prestadores | SINISA (cadastro) |
| `abrangencia` | Abrangência do prestador (CAD0003) | string | Local, Regional ou Múltipla | SINISA (cadastro) |
| `prestador` | Nome do prestador (CAD0005) | string | texto | SINISA (cadastro) |
| `sigla_prestador` | Sigla do prestador (CAD0006) | string | texto | SINISA (cadastro) |
| `pop_total` | População Total Residente | float64 | Habitantes | Gestão técnica DFE0001 |
| `pop_urbana` | População Urbana Residente | float64 | Habitantes | Gestão técnica DFE0002 |
| `pop_rural` | População Rural Residente | float64 | Habitantes | Gestão técnica DFE0003 |
| `atividades_abrangidas` | Atividades abrangidas para Esgotamento Sanitário | object | nan | Gestão técnica CAD2103 |
| `pop_urb_atendida_rede` | População urbana atendida com rede de esgotamento sanitário | float64 | Habitantes | Gestão técnica GTE0001 |
| `pop_rur_atendida_rede` | População rural atendida com rede de esgotamento sanitário | float64 | Habitantes | Gestão técnica GTE0002 |
| `extensao_rede_km` | Extensão da rede pública de esgotamento sanitário | float64 | km | Gestão técnica GTE1001 |
| `esgoto_coletado_mil_m3` | Volume total de esgoto coletado | float64 | 1.000 m³/ano | Gestão técnica GTE1002 |
| `esgoto_tratado_mil_m3` | Volume total de esgoto tratado | float64 | 1.000 m³/ano | Gestão técnica GTE1014 |
| `atend_rede_pop_total` | Atendimento da população total com rede coletora de esgoto | float64 | % | Indicador IES0001: [(GTE0001 + GTE0002) / DFE0001] x 100 |
| `atend_rede_pop_urbana` | Atendimento da população urbana com rede coletora de esgoto | float64 | % | Indicador IES0002: (GTE0001 / DFE0002) x 100 |
| `atend_rede_pop_rural` | Atendimento da população rural com rede coletora de esgoto | float64 | % | Indicador IES0003: (GTE0002 / DFE0003) x 100 |
| `ies0004` | Atendimento dos domicílios totais com rede coletora de esgoto | float64 | % | Indicador IES0004: [(GTE0008 + GTE0018 + GTE0012 + GTE0020) / OGM4006] x 100 |
| `ies0005` | Atendimento dos domicílios urbanos com rede coletora de esgoto | float64 | % | Indicador IES0005: [(GTE0008 + GTE0012) / OGM4004] x 100 |
| `ies0006` | Atendimento dos domicílios rurais com rede coletora de esgoto | float64 | % | Indicador IES0006: [(GTE0018 + GTE0020) / OGM4005] x 100 |
| `atend_coleta_trat_dom_total` | Atendimento dos domicílios totais com coleta e tratamento de esgoto | float64 | % | Indicador IES0007: [(GTE0009 + GTE0019 + GTE0013 + GTE0021) / OGM4006] x 100 |
| `ies0008` | Atendimento dos domicílios urbanos com coleta e tratamento de esgoto | float64 | % | Indicador IES0008: [(GTE0009 + GTE0013) / OGM4004] x 100 |
| `ies0009` | Atendimento dos domicílios rurais com coleta e tratamento de esgoto | float64 | % | Indicador IES0009: [(GTE0019 + GTE0021) / OGM4005] x 100 |
| `ies1001` | Extensão de rede de esgoto por ligação | float64 | m/ligação | Indicador IES1001: {[(GTE1001 + GTE1001_A) / 2] / [(GTE0003 + GTE0003_A + GTA0004 + GTA0004_A) / 2]} x 1.000 |
| `ies1002` | Densidade de economias de esgoto por ligação | float64 | econ./ligação | Indicador IES1002: [(GTE0006 + GTE0006_A +GTE0016 + GTE0016_A) / 2] / [(GTE0003 + GTE0003_A) / 2] |
| `ies1003` | Incidência das economias residenciais ativas com coleta de esgoto | float64 | % | Indicador IES1003: {[(GTE0008 + GTE0008_A + GTA0018 + GTA0018_A) / 2] / [(GTE0006 + GTE0006_A + GTA0016 + GTA0016_A) / 2]} x 100 |
| `ies1004` | Incidência das economias residenciais ativas com tratamento de esgoto | float64 | % | Indicador IES1004: {[(GTE0009 + GTE0009_A + GTE0019 + GTE0019_A) / 2] / [(GTE0007 + GTE0007_A + GTE0017 + GTE0017_A) / 2]} x 100 |
| `ies2002` | Esgoto coletado referido à água consumida | float64 | % | Indicador IES2002: (GTE1002 / GTA1211) x 100 |
| `ies2003` | Esgoto tratado referido à água consumida | float64 | % | Indicador IES2003: [(GTE1014 + GTE1013) / GTA1211] x 100 |
| `trat_sobre_coletado` | Esgoto tratado referido ao esgoto coletado | float64 | % | Indicador IES2004: [(GTE1014 + GTE1015 + GTE1013) / (GTE1002 + GTE1009)] x 100 |
| `energia_kwh_m3` | Consumo médio de energia elétrica no serviço de esgotamento sanitário | float64 | KWh/m³ | Indicador IES2005: GTE1016 / GTE1002 |
| `extravasamentos_por_km` | Extravasamentos de esgoto reparados por extensão de rede | float64 | extravasamentos/km | Indicador IES3001: GTE3002 / GTE1001 |
| `tempo_reparo_horas` | Tempo médio para reparo de extravasamentos de esgoto | float64 | horas/reparo | Indicador IES3002: GTE3004 / GTE3002 |
| `ies3003` | Extravasamentos de esgoto reparados por reclamação | float64 | extravasamentos/reclamação | Indicador IES3003: GTE3002 / GTE3001 |
| `ife0001` | Produtividade do pessoal total no serviço de esgotamento sanitário | float64 | ligações/empregado | Indicador IFE0001: [(GTE0003 + GTE0003_A) / 2] / [(GFI2147 +GFI2147_A) / 2] |
| `ife0002` | Participação do pessoal próprio no serviço de esgotamento sanitário | float64 | % | Indicador IFE0002: ([(GFI2145 + GFI2145_A)/2] / [(GFI2147 + GFI2147_A)/2]) * 100 |
| `receita_direta_rs_m3` | Receita operacional direta média de usuários de esgoto | float64 | R$/m³ | Indicador IFE1001: GFI1101 / [(GTE1006 - GTE1009) x 1.000] |
| `ife1002` | Receita operacional direta total média de esgoto | float64 | R$/m³ | Indicador IFE1002: GFI1105 / (GTE1006 x 1000) |
| `ife1003` | Participação da receita operacional indireta na receita operacional total de esgoto | float64 | % | Indicador IFE1003: (GFI1104 / GFI1105) x 100 |
| `evasao_receita_pct` | Evasão de receitas do serviço de esgoto | float64 | % | Indicador IFE1004: [(GFI1105 - GFI1106) / GFI1105] x 100 |
| `ife1005` | Dias de faturamento comprometidos com contas a receber de esgoto | float64 | dias | Indicador IFE1005: (GFI1107 / GFI1105) x 360 |
| `desempenho_financeiro_pct` | Desempenho financeiro do serviço de esgotamento sanitário | float64 | % | Indicador IFE2001: (GFI1105 / GFI2120) x 100 |
| `despesa_total_rs_m3` | Despesa total média de esgoto incluindo tributos | float64 | R$/m³ | Indicador IFE2002: GFI2120 / (GTE1006 x 1000) |
| `ife2003` | Despesa total média de esgoto não incluindo tributos | float64 | R$/m³ | Indicador IFE2003: (GFI2120 - GFI2106 - GFI2117) / (GTE1006 x 1000) |
| `ife2004` | Despesa de exploração média de esgoto | float64 | R$/m³ | Indicador IFE2004: GFI2108 / (GTE1006 x 1000) |
| `ife2005` | Despesa de exploração média de esgoto por economia ativa | float64 | R$/economia/ano | Indicador IFE2005: GFI2108 / [(GTE0006 + GTE0016 + GTE0006_A + GTE0016_A)/2] |
| `ife2006` | Despesa média com pessoal próprio do serviço de esgotamento sanitário | float64 | R$/empregado/ano | Indicador IFE2006: GFI2101 / [(GFI2145 + GFI2145_A) / 2] |
| `ife2007` | Despesa média de energia elétrica do serviço de esgotamento sanitário | float64 | R$/KWh | Indicador IFE2007: GFI2104 / (GTE1016 x 1000) |
| `ife2008` | Incidência da despesa de pessoal próprio nas despesas de exploração de esgoto | float64 | % | Indicador IFE2008: (GFI2101 / GFI2108) x 100 |
| `ife2009` | Incidência da despesa de pessoal total nas despesas de exploração de esgoto | float64 | % | Indicador IFE2009: [(GFI2101 + GFI2102) / GFI2108] x 100 |
| `ife2010` | Incidência da despesa de energia elétrica nas despesas de exploração de esgoto | float64 | % | Indicador IFE2010: (GFI2104 / GFI2108) x 100 |
| `ife2011` | Margem da despesa de exploração de esgoto | float64 | % | Indicador IFE2011: (GFI2108 / GFI1103) x 100 |
| `ife2012` | Margem da despesa com pessoal próprio do serviço de esgotamento sanitário | float64 | % | Indicador IFE2012: (GFI2101 / GFI1103) x 100 |
| `ife2013` | Margem da despesa com pessoal total do serviço de esgotamento sanitário | float64 | % | Indicador IFE2013: [(GFI2101 + GFI2102) / GFI1103] x 100 |
| `ife2014` | Margem da despesa com serviço da dívida de esgoto | float64 | % | Indicador IFE2014: (GFI2112 /GFI1103) x 100 |
| `suficiencia_caixa_pct` | Suficiência de caixa do serviço de esgotamento sanitário | float64 | % | Indicador IFE2016: [GFI1106 / (GFI2108 + GFI2109 + GFI2111 + GFI2117)] x 100 |
| `multiplos_prestadores` | Município com mais de um prestador (valor de CAD0002 contém '|') | bool | derivada | derivada |
| `natureza_grupo` | Natureza jurídica agrupada em 5 classes | string | derivada | derivada |
| `pop_atendida_rede` | População atendida com rede coletora = pop_urb_atendida_rede + pop_rur_atendida_rede (convenção do SINISA); vazio se não há dado | float64 | habitantes; derivada | derivada |
| `pop_sem_rede` | População sem rede coletora = pop_total − pop_atendida_rede (mínimo 0) | float64 | habitantes; derivada | derivada |
| `cobertura_efetiva_trat` | Estimativa da % da população com esgoto coletado e tratado = atend_rede_pop_total × min(trat_sobre_coletado, 100) / 100 | float64 | percentual; derivada (aproximação) | derivada |
| `flag_trat_acima_100` | trat_sobre_coletado acima de 100% (ex.: esgoto importado/exportado) | bool | derivada | derivada |
| `faixa_pop` | Faixa de população residente | category | até 20 mil; 20–100 mil; 100–500 mil; acima de 500 mil | SINISA (cadastro) |
| `meta90_coleta` | Atendimento com rede ≥ 90% (referência da Lei 14.026/2020) | boolean | derivada; vazio se indicador não calculado | derivada |
| `meta90_efetiva` | cobertura_efetiva_trat ≥ 90% | boolean | derivada; vazio se não calculável | derivada |

Fonte: Ministério das Cidades / SINISA, módulo Esgotamento Sanitário, ano de referência 2024 (publicação 18/12/2025). Licença do texto e dos dados derivados: CC-BY 4.0.
