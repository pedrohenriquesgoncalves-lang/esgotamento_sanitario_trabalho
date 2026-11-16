"""ETL determinístico do SINISA - Esgotamento Sanitário 2024 (base municipal).

Lê os .xlsx brutos (sem alterá-los), padroniza nomes e tipos, trata valores
"Não calculado", cria métricas derivadas e grava Parquet + CSV.gz, um log de
tratamento (JSON) e o dicionário de dados (Markdown).

Uso (na raiz do repositório):  python -m src.etl
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
F_IND = RAW / "SINISA_ESGOTO_Indicadores_Base_Municipal_2024.xlsx"
F_TEC = RAW / "SINISA_ESGOTO_Informações_Gestão_Técnica_de_Esgoto_Base_Municipal_2024.xlsx"

log = logging.getLogger("etl")

# Colunas da base técnica que serão incorporadas (chave: cod_ibge)
TEC_COLS = ["DFE0001", "DFE0002", "DFE0003", "CAD2103", "GTE0001", "GTE0002",
            "GTE1001", "GTE1002", "GTE1014"]

# Nomes legíveis para as variáveis usadas na análise (demais seguem o código em minúsculas)
ALIASES = {
    "DFE0001": "pop_total", "DFE0002": "pop_urbana", "DFE0003": "pop_rural",
    "CAD2103": "atividades_abrangidas", "GTE0001": "pop_urb_atendida_rede",
    "GTE0002": "pop_rur_atendida_rede", "GTE1001": "extensao_rede_km",
    "GTE1002": "esgoto_coletado_mil_m3", "GTE1014": "esgoto_tratado_mil_m3",
    "IES0001": "atend_rede_pop_total", "IES0002": "atend_rede_pop_urbana",
    "IES0003": "atend_rede_pop_rural", "IES0007": "atend_coleta_trat_dom_total",
    "IES2004": "trat_sobre_coletado", "IES2005": "energia_kwh_m3",
    "IES3001": "extravasamentos_por_km", "IES3002": "tempo_reparo_horas",
    "IFE1001": "receita_direta_rs_m3", "IFE1004": "evasao_receita_pct",
    "IFE2001": "desempenho_financeiro_pct", "IFE2002": "despesa_total_rs_m3",
    "IFE2016": "suficiencia_caixa_pct",
}
TEC_CAD = ["Macrorregião", "Município", "UF", "Capital", "RM / RIDE", "CAD0002", "CAD0003", "CAD0005", "CAD0006"]
PCT_0_100 = [f"IES000{i}" for i in range(1, 10)]  # atendimento: deve estar em [0, 100]
REASONS = {"divisão por zero": "divisao_por_zero",
           "campos obrigatórios vazios": "campos_obrigatorios_vazios",
           "condições não atendidas": "condicoes_nao_atendidas"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_sinisa(path: Path, sheet: int = 0) -> tuple[pd.DataFrame, dict, dict]:
    """Lê uma aba SINISA (cabeçalho em várias linhas). Retorna dados, rótulos e unidades por código."""
    raw = pd.read_excel(path, sheet_name=sheet, header=None, dtype=object)
    code_row = raw.index[raw[0].astype(str).str.strip() == "cod_IBGE"][0]
    codes = raw.iloc[code_row].astype(str).str.strip().tolist()
    labels = dict(zip(codes, raw.iloc[code_row - 2].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()))
    units = dict(zip(codes, raw.iloc[code_row - 1].astype(str).str.strip()))
    df = raw.iloc[code_row + 1:].copy()
    df.columns = codes
    df = df[pd.to_numeric(df["cod_IBGE"], errors="coerce").notna()].reset_index(drop=True)
    return df, labels, units


def to_numeric_logged(df: pd.DataFrame, cols: list[str], stats: dict) -> pd.DataFrame:
    """Converte para número; textos 'Não calculado (...)' viram NaN e são contados por motivo."""
    for c in cols:
        s = df[c]
        num = pd.to_numeric(s, errors="coerce")
        bad = s[num.isna() & s.notna()].astype(str)
        for text, key in REASONS.items():
            n = int(bad.str.contains(text, regex=False).sum())
            if n:
                stats.setdefault("nao_calculado", {}).setdefault(c, {})[key] = n
        df[c] = num.astype("float64")
    return df


def natureza_grupo(x: str) -> str:
    if x == "Sem dado informado":
        return "Sem dado de esgoto"
    if x in {"Sociedade de economia mista", "Empresa privada", "Autarquia"}:
        return x
    return "Município (adm. direta)" if x == "Município" else "Outras ou múltiplas"


def build() -> tuple[pd.DataFrame, dict, dict, dict]:
    """Universo = 3.903 municípios da base técnica; 2.749 têm indicadores (tem_dado_esgoto=True)."""
    stats: dict = {"arquivos_brutos_sha256": {p.name: sha256(p) for p in (F_IND, F_TEC)}}
    ind, lab_i, uni_i = read_sinisa(F_IND)
    tec, lab_t, uni_t = read_sinisa(F_TEC)
    stats["linhas_lidas"] = {"indicadores": len(ind), "gestao_tecnica": len(tec)}
    assert ind["cod_IBGE"].is_unique and tec["cod_IBGE"].is_unique, "cod_IBGE duplicado"

    # tipos e textos
    ind_cols = [c for c in ind.columns if re.match(r"^(IES|IFE)\d{4}$", c)]
    ind = to_numeric_logged(ind, ind_cols, stats)
    tec = to_numeric_logged(tec, [c for c in TEC_COLS if c != "CAD2103"], stats)
    for t in (ind, tec):
        t["cod_IBGE"] = t["cod_IBGE"].astype(int).astype(str).str.zfill(7)

    # sanidade: o cadastro das duas bases deve coincidir nos municípios comuns
    chk = ind[["cod_IBGE", "CAD0002"]].merge(tec[["cod_IBGE", "CAD0002"]], on="cod_IBGE", suffixes=("_i", "_t"))
    norm = lambda x: x.astype(str).str.split(r"\s*\|\s*").map(lambda v: " | ".join(sorted(v)))  # ignora a ordem dos prestadores
    stats["divergencia_natureza_entre_bases"] = int((norm(chk["CAD0002_i"]) != norm(chk["CAD0002_t"])).sum())

    df = tec[["cod_IBGE"] + TEC_CAD + TEC_COLS].merge(ind[["cod_IBGE"] + ind_cols], on="cod_IBGE",
                                                      how="left", validate="1:1")
    df.insert(1, "tem_dado_esgoto", df["cod_IBGE"].isin(ind["cod_IBGE"]))
    assert df["tem_dado_esgoto"].sum() == len(ind) and df["DFE0001"].notna().all(), "falha no join municipal"
    sem = df[~df["tem_dado_esgoto"]]
    stats["universo"] = {"municipios": len(df), "com_dado": int(df["tem_dado_esgoto"].sum()),
                         "sem_dado": len(sem), "pop_sem_dado": int(sem["DFE0001"].sum()),
                         "pop_universo": int(df["DFE0001"].sum())}

    # cadastro
    df = df.rename(columns={"cod_IBGE": "cod_ibge", "Macrorregião": "macrorregiao", "Município": "municipio",
                            "UF": "uf", "Capital": "capital", "RM / RIDE": "rm_ride",
                            "CAD0002": "natureza_juridica", "CAD0003": "abrangencia",
                            "CAD0005": "prestador", "CAD0006": "sigla_prestador"})
    df["capital"] = df["capital"].eq("Sim")
    df["rm_ride"] = df["rm_ride"].fillna("Fora de RM/RIDE")
    df["natureza_juridica"] = df["natureza_juridica"].fillna("Sem dado informado")
    df["abrangencia"] = df["abrangencia"].fillna("Sem dado informado")
    df["multiplos_prestadores"] = df["natureza_juridica"].str.contains("|", regex=False)
    df["natureza_grupo"] = df["natureza_juridica"].map(natureza_grupo)
    df["abrangencia"] = np.where(df["abrangencia"].str.contains("|", regex=False), "Múltipla", df["abrangencia"])
    for c in ("macrorregiao", "municipio", "uf", "prestador", "sigla_prestador", "natureza_juridica"):
        df[c] = df[c].astype("string").str.strip()

    # faixa válida de percentuais de atendimento (sem apagar: só sinaliza e registra)
    fora = {c: int(((df[c] < 0) | (df[c] > 100)).sum()) for c in PCT_0_100}
    stats["atendimento_fora_0_100"] = fora
    for c in PCT_0_100:
        df.loc[(df[c] < 0) | (df[c] > 100), c] = np.nan

    # métricas derivadas (convenção SINISA: população atendida = urbana + rural com rede)
    df["pop_atendida_rede"] = (df["GTE0001"].fillna(0) + df["GTE0002"].fillna(0)).where(df["tem_dado_esgoto"])
    df["pop_sem_rede"] = (df["DFE0001"] - df["pop_atendida_rede"]).clip(lower=0)
    df["cobertura_efetiva_trat"] = df["IES0001"] * df["IES2004"].clip(upper=100) / 100
    df["flag_trat_acima_100"] = df["IES2004"] > 100
    df["faixa_pop"] = pd.cut(df["DFE0001"], [0, 20_000, 100_000, 500_000, np.inf],
                             labels=["até 20 mil", "20–100 mil", "100–500 mil", "acima de 500 mil"])
    df["meta90_coleta"] = (df["IES0001"] >= 90).where(df["IES0001"].notna()).astype("boolean")
    df["meta90_efetiva"] = (df["cobertura_efetiva_trat"] >= 90).where(df["cobertura_efetiva_trat"].notna()).astype("boolean")

    df = df.rename(columns=ALIASES)
    df.columns = [c.lower() if re.match(r"^[A-Z]{3}\d{4}$", c) else c for c in df.columns]
    stats["colunas_finais"] = len(df.columns)
    stats["tratado_acima_100"] = int(df["flag_trat_acima_100"].sum())
    return df, {**lab_i, **lab_t}, {**uni_i, **uni_t}, stats


# ---------------------------------------------------------------- dicionário
DERIVED = {
    "cod_ibge": ("Código IBGE do município (7 dígitos)", "string", "chave primária"),
    "macrorregiao": ("Macrorregião do município", "string", "Norte, Nordeste, Centro-Oeste, Sudeste, Sul"),
    "municipio": ("Nome do município", "string", "texto"),
    "uf": ("Unidade da Federação", "string", "sigla de 2 letras"),
    "capital": ("Município é capital de UF", "bool", "True/False"),
    "rm_ride": ("Região Metropolitana ou RIDE do município", "string", "nome ou 'Fora de RM/RIDE'"),
    "natureza_juridica": ("Natureza jurídica do(s) prestador(es) (CAD0002)", "string", "'A | B' quando há vários prestadores"),
    "abrangencia": ("Abrangência do prestador (CAD0003)", "string", "Local, Regional ou Múltipla"),
    "prestador": ("Nome do prestador (CAD0005)", "string", "texto"),
    "sigla_prestador": ("Sigla do prestador (CAD0006)", "string", "texto"),
    "tem_dado_esgoto": ("Município possui dados de esgoto na base de indicadores do SINISA 2024", "bool", "derivada; False = município listado na base técnica sem informação do prestador"),
    "multiplos_prestadores": ("Município com mais de um prestador (valor de CAD0002 contém '|')", "bool", "derivada"),
    "natureza_grupo": ("Natureza jurídica agrupada em 5 classes", "string", "derivada"),
    "pop_atendida_rede": ("População atendida com rede coletora = pop_urb_atendida_rede + pop_rur_atendida_rede (convenção do SINISA); vazio se não há dado", "float64", "habitantes; derivada"),
    "pop_sem_rede": ("População sem rede coletora = pop_total − pop_atendida_rede (mínimo 0)", "float64", "habitantes; derivada"),
    "cobertura_efetiva_trat": ("Estimativa da % da população com esgoto coletado e tratado = atend_rede_pop_total × min(trat_sobre_coletado, 100) / 100", "float64", "percentual; derivada (aproximação)"),
    "flag_trat_acima_100": ("trat_sobre_coletado acima de 100% (ex.: esgoto importado/exportado)", "bool", "derivada"),
    "faixa_pop": ("Faixa de população residente", "category", "até 20 mil; 20–100 mil; 100–500 mil; acima de 500 mil"),
    "meta90_coleta": ("Atendimento com rede ≥ 90% (referência da Lei 14.026/2020)", "boolean", "derivada; vazio se indicador não calculado"),
    "meta90_efetiva": ("cobertura_efetiva_trat ≥ 90%", "boolean", "derivada; vazio se não calculável"),
}


def write_dictionary(df: pd.DataFrame, labels: dict, units: dict, notes: pd.DataFrame) -> None:
    code_of = {v: k for k, v in ALIASES.items()}
    nmap = {r["codigo"]: r for _, r in notes.iterrows()}
    rows = ["# Dicionário de dados — SINISA Esgoto 2024 (base municipal)", "",
            "Arquivo: `data/processed/municipios_esgoto_2024.parquet` (e `.csv.gz`). "
            "1 linha = 1 município da base técnica (3.903 linhas; 2.749 com dados de esgoto, ver `tem_dado_esgoto`). Gerado automaticamente por `src/etl.py`.", "",
            "Valores originais `Não calculado (...)` viram vazios (NaN); os motivos estão em `data/processed/etl_log.json`.", "",
            "| Variável | Significado | Tipo | Unidade / formato | Origem |", "| --- | --- | --- | --- | --- |"]
    for col in df.columns:
        code = code_of.get(col, col.upper() if re.match(r"^[a-z]{3}\d{4}$", col) else None)
        if col in DERIVED:
            m, t, u = DERIVED[col]; src = "derivada" if "derivada" in u else "SINISA (cadastro)"
        elif code in nmap:
            n = nmap[code]; m, u = n["descricao"], n["unidade"]; src = f"Indicador {code}: {n['formula']}"
            t = str(df[col].dtype)
        else:
            m, u, t = labels.get(code, col), units.get(code, ""), str(df[col].dtype)
            src = f"Gestão técnica {code}" if code else "SINISA"
        u = "" if u in ("nan", "None") else u
        rows.append(f"| `{col}` | {m} | {t} | {u} | {src.replace('|', '/')} |")
    rows += ["", "Fonte: Ministério das Cidades / SINISA, módulo Esgotamento Sanitário, ano de referência 2024 "
             "(publicação 18/12/2025). Licença do texto e dos dados derivados: CC-BY 4.0."]
    (ROOT / "data" / "data_dictionary.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def read_notes() -> pd.DataFrame:
    n = pd.read_excel(F_IND, sheet_name=1, header=None, dtype=object)
    i = n.index[n[0].astype(str).str.strip() == "CÓDIGO DO INDICADOR"][0]
    n = n.iloc[i + 1:, :4].dropna(subset=[0])
    n.columns = ["codigo", "descricao", "formula", "unidade"]
    return n.apply(lambda s: s.astype(str).str.replace(r"\s+", " ", regex=True).str.strip())


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    OUT.mkdir(parents=True, exist_ok=True)
    df, labels, units, stats = build()
    (OUT / "etl_log.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    df.to_parquet(OUT / "municipios_esgoto_2024.parquet", index=False)
    df.to_csv(OUT / "municipios_esgoto_2024.csv.gz", index=False, compression="gzip")
    write_dictionary(df, labels, units, read_notes())
    log.info("%d municípios x %d colunas gravados em %s", len(df), df.shape[1], OUT)


if __name__ == "__main__":
    main()
