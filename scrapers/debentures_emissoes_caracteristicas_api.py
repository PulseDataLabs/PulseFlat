"""
scrapers/debentures_emissoes_caracteristicas_api.py
--------------------------------------------------
Coleta oficial de características, emissões e parâmetros de debêntures
via API oficial ANBIMA Developers (ANBIMA Data - Pacote Debêntures+).

Projetado como processo independente e moderno para substituição futura
do scraper legado `debentures_emissoes_caracteristicas` (SND Web).

Contém:
- VNA oficial apurado pela ANBIMA
- PU Par e % do PU Par
- Duration (prazo médio em dias úteis)
- Z-Spread (spread de crédito sobre curva de juros soberana)
- Referência NTN-B e spread incentivado
- Enquadramento na Lei 12.431 (Debênture Incentivada)
- Expressão da taxa contratual (percentual_taxa) e indexador (grupo)
- Taxas indicativas e limites estatísticos
- Código internacional ISIN
"""

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import agora_brt, get_logger
from utils.parsers import _CAL, hash_row

log = get_logger("debentures_emissoes_caracteristicas_api")


class DebenturesEmissoesCaracteristicasApiScraper(BaseAnbimaDataScraper):
    # Identificador único (gera data/debentures_emissoes_caracteristicas_api.csv)
    name = "debentures_emissoes_caracteristicas_api"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = False
    compress = False

    # Chave primária do cadastro
    chaves_dedup = ["codigo_ativo"]

    # Catálogo de Metadados PulseFlat
    title = "Debêntures — Emissões e Características (API ANBIMA)"
    description = (
        "Cadastro e características oficiais de debêntures capturados via API oficial "
        "ANBIMA Data (Debêntures+), incluindo VNA (Valor Nominal Atualizado), PU Par, "
        "Duration, Z-Spread, enquadramento na Lei 12.431 (debênture incentivada), NTN-B de "
        "referência, taxas indicativas e parâmetros contratuais."
    )
    icon = "🏛️"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = [
        "debentures",
        "emissoes",
        "caracteristicas",
        "vna",
        "duration",
        "z_spread",
        "lei_12431",
        "anbima",
        "api",
    ]
    source = "ANBIMA Data (developers.anbima.com.br)"

    def _obter_data_referencia(self) -> date:
        """Determina a data de referência: self.target_date se informada, ou último dia útil."""
        if self.target_date:
            return self.target_date
        return _CAL.offset(date.today(), -1)

    def _obter_isin_map(self, data_str: str) -> dict[str, str]:
        """Busca mapeamento ticker -> ISIN no REUNE da data com fallback nos datasets locais."""
        isin_map = {}
        # 1. Fallback primário nos datasets PulseFlat consolidados
        root_data = Path(__file__).resolve().parents[1] / "data"
        for ref_file in [
            root_data / "debentures_mercado_secundario_precos_negociacao_api.csv.gz",
            root_data / "anbima_debentures.csv",
        ]:
            if ref_file.exists():
                try:
                    df_ref = pd.read_csv(ref_file, usecols=["codigo_ativo", "isin"], dtype=str)
                    df_ref = df_ref[
                        df_ref["isin"].notna() & (df_ref["isin"] != "")
                    ].drop_duplicates(subset=["codigo_ativo"])
                    for _, r in df_ref.iterrows():
                        isin_map.setdefault(r["codigo_ativo"], r["isin"])
                except Exception:
                    pass

        # 2. Enriquecimento complementar via REUNE do dia
        try:
            res = self.client.get(
                "/feed/precos-indices/v1/reune/negociacoes",
                params={"data": data_str, "page": 0, "size": 1000},
            )
            items = (
                res.get("content", [])
                if isinstance(res, dict)
                else (res if isinstance(res, list) else [])
            )
            for item in items:
                ticker = item.get("codigo_ativo")
                isin = item.get("isin")
                if ticker and isin:
                    isin_map[ticker] = isin
        except Exception as e:
            self.logger.warning(f"Não foi possível consultar REUNE para ISINs: {e}")

        return isin_map

    def fetch(self) -> pd.DataFrame:
        """
        Executa a captura da API de Debêntures+ da ANBIMA e estrutura as características
        oficiais de cada ativo monitorado.
        """
        if not self.check_credentials():
            self.logger.warning("Credenciais da ANBIMA não configuradas. Encerrando.")
            return pd.DataFrame()

        data_ref = self._obter_data_referencia()
        data_str = data_ref.strftime("%Y-%m-%d")
        self.logger.info(f"Iniciando coleta de características de debêntures para: {data_str}")

        # 1. Consulta o endpoint Debêntures+ (alta granularidade)
        try:
            dados = self.client.get(
                "/feed/precos-indices/v1/debentures-mais/mercado-secundario",
                params={"data": data_str},
            )
        except Exception as e:
            self.logger.warning(f"Falha ao consultar Debêntures+, tentando fallback padrão: {e}")
            try:
                dados = self.client.get(
                    "/feed/precos-indices/v1/debentures/mercado-secundario",
                    params={"data": data_str},
                )
            except Exception as e2:
                self.logger.error(f"Falha em ambos endpoints da ANBIMA: {e2}")
                return pd.DataFrame()

        if isinstance(dados, dict):
            dados = dados.get("content", [])
        if not isinstance(dados, list):
            dados = []

        self.logger.info(f"Retornados {len(dados)} papéis da API ANBIMA.")
        if not dados:
            return pd.DataFrame()

        # 2. Busca ISINs auxiliares
        isin_map = self._obter_isin_map(data_str)
        data_captura_padrao, _ = agora_brt()

        # 3. Formatação e normalização
        registros = []
        for item in dados:
            ticker = item.get("codigo_ativo")
            if not ticker:
                continue

            isin = isin_map.get(ticker, "")

            def clean_str(val):
                if val is None:
                    return ""
                s = str(val).strip()
                return "" if s in ("-", "--", "nan", "None") else s

            def clean_num(val, dec=6):
                if val is None:
                    return ""
                try:
                    f = float(val)
                    return f"{f:.{dec}f}".rstrip("0").rstrip(".")
                except (ValueError, TypeError):
                    return clean_str(val)

            rec = {
                "data_captura": data_captura_padrao,
                "data_referencia": data_str,
                "codigo_ativo": ticker,
                "emissor": clean_str(item.get("emissor")),
                "isin": isin,
                "grupo": clean_str(item.get("grupo")),
                "percentual_taxa": clean_str(item.get("percentual_taxa")),
                "data_vencimento": clean_str(item.get("data_vencimento")),
                "vna": clean_num(item.get("vna"), dec=6),
                "pu_par": clean_num(item.get("pu_par"), dec=6),
                "pu_indicativo": clean_num(item.get("pu"), dec=6),
                "percent_pu_par": clean_num(item.get("percent_pu_par"), dec=4),
                "duration": clean_num(item.get("duration"), dec=2),
                "z_spread": clean_num(item.get("z_spread"), dec=4),
                "spread_incentivado_sem_gross_up": clean_num(
                    item.get("spread_incentivado_sem_gross_up"), dec=4
                ),
                "referencia_ntnb": clean_str(item.get("referencia_ntnb")),
                "lei_12431": clean_str(item.get("lei_12431")),
                "taxa_indicativa": clean_num(item.get("taxa_indicativa"), dec=4),
                "taxa_compra": clean_num(item.get("taxa_compra"), dec=4),
                "taxa_venda": clean_num(item.get("taxa_venda"), dec=4),
                "desvio_padrao": clean_num(item.get("desvio_padrao"), dec=4),
                "val_min_intervalo": clean_num(item.get("val_min_intervalo"), dec=4),
                "val_max_intervalo": clean_num(item.get("val_max_intervalo"), dec=4),
                "percent_reune": clean_str(item.get("percent_reune")),
            }
            registros.append(rec)

        df = pd.DataFrame(registros)
        if not df.empty:
            df.sort_values(by=["codigo_ativo"], inplace=True)
            df.reset_index(drop=True, inplace=True)

            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]
            self.logger.info(
                f"Consolidação concluída: {len(df)} debêntures estruturadas com sucesso."
            )

        return df


def main():
    DebenturesEmissoesCaracteristicasApiScraper().run()


if __name__ == "__main__":
    main()
