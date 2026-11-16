"""Testes de sanidade do pipeline (rodam sobre os .xlsx brutos em data/raw)."""
import pytest

from src import etl


@pytest.fixture(scope="module")
def dados():
    df, _, _, stats = etl.build()
    return df, stats


def test_universo_e_chave(dados):
    df, stats = dados
    assert len(df) == 3903 and df["cod_ibge"].is_unique
    assert df["cod_ibge"].str.len().eq(7).all()
    assert int(df["tem_dado_esgoto"].sum()) == 2749
    assert stats["divergencia_natureza_entre_bases"] == 0


def test_percentuais_de_atendimento_validos(dados):
    df, _ = dados
    for c in ("atend_rede_pop_total", "atend_rede_pop_urbana", "atend_rede_pop_rural"):
        assert df[c].dropna().between(0, 100).all()


def test_reproduz_indicador_oficial_do_brasil(dados):
    df, _ = dados
    cobertura = df["pop_atendida_rede"].fillna(0).sum() / df["pop_total"].sum() * 100
    assert cobertura == pytest.approx(62.3, abs=0.05)  # IES0001 Brasil (base UF/MR/BR)


def test_nao_calculado_virou_nan(dados):
    df, _ = dados
    assert str(df["atend_rede_pop_total"].dtype) == "float64"
    assert df["atend_rede_pop_total"].isna().sum() >= 21
