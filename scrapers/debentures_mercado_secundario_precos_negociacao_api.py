"""
scrapers/debentures_mercado_secundario_precos_negociacao_api.py
--------------------------------------------------------------
Coleta oficial do mercado secundário de debêntures e negociações (REUNE)
via APIs do portal ANBIMA Developers (ANBIMA Data).

Projetado para rodar em paralelo ao scraper legado
`debentures_mercado_secundario_precos_negociacao` (SND Web Scraping),
com compatibilidade de esquema para substituição futura.

Padronizado para regras de liquidez média:
- Retorna o universo completo de debêntures monitoradas pela ANBIMA no dia.
- Ativos com negócios: preços unitários realizados, quantidade e negócios.
- Ativos sem negócios: quantidade=0, negócios=0, volume=0.0 e preços vazios.
"""

import sys
import time
from datetime import date
from pathlib import Path
from collections import defaultdict
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scrapers.utils.anbima_data_base import BaseAnbimaDataScraper
from utils.base import get_logger, limpar
from utils.parsers import _CAL, hash_row

log = get_logger("debentures_mercado_secundario_precos_negociacao_api")


class DebenturesMercadoSecundarioPrecosNegociacaoApiScraper(BaseAnbimaDataScraper):
    # Identificador único (gera data/debentures_mercado_secundario_precos_negociacao_api.csv.gz)
    name = "debentures_mercado_secundario_precos_negociacao_api"
    group = "anbima"
    enabled = True
    phase = 1
    accumulate = True
    compress = True

    # Chaves de deduplicação diária
    chaves_dedup = ["data_referencia", "codigo_ativo"]

    # Catálogo de Metadados PulseFlat
    title = "Debêntures — Mercado Secundário e Preços de Negociação (API ANBIMA)"
    description = (
        "Histórico e boletim diário de negociações no mercado secundário de debêntures capturados "
        "via APIs oficiais da ANBIMA e REUNE, contendo preços realizados (mínimo, médio ponderado, "
        "máximo), quantidade negociada, número de negócios, volume financeiro e parâmetros oficiais "
        "da ANBIMA. Padronizado com zeros para cálculo exato de liquidez média."
    )
    icon = "🏛️"
    icon_class = "icon-anbima"
    badge = "ANBIMA API"
    badge_class = "badge-dynamic"
    tags = ["debentures", "mercado_secundario", "precos", "negociacao", "anbima", "reune", "api"]
    source = "ANBIMA Data (developers.anbima.com.br)"

    def _obter_data_referencia(self) -> date:
        """Determina a data de referência: self.target_date se informada, ou último dia útil."""
        if self.target_date:
            return self.target_date
        return _CAL.offset(date.today(), -1)

    def _obter_operacoes_reune(self, data_str: str) -> dict[str, dict[str, Any]]:
        """
        Consulta todas as páginas de negociações do REUNE na data e agrega por ativo.
        """
        reune_agregado: dict[str, dict[str, Any]] = defaultdict(lambda: {
            "quantidade_negocios": 0,
            "quantidade_titulos": 0.0,
            "volume_total_rs": 0.0,
            "precos": [],
            "isin": None,
        })

        page = 0
        total_debs_ops = 0
        self.logger.info(f"Consultando negociações REUNE para {data_str}...")

        while True:
            try:
                raw_body = self.client.get(
                    "/feed/precos-indices/v1/reune/negociacoes",
                    params={"data": data_str, "page": page, "size": 1000},
                )
            except Exception as e:
                self.logger.warning(f"Erro ao consultar página {page} do REUNE: {e}")
                break

            if isinstance(raw_body, dict):
                items = raw_body.get("content", [])
                total_pages = raw_body.get("total_pages", page + 1)
            elif isinstance(raw_body, list):
                items = raw_body
                total_pages = 1
            else:
                break

            if not items:
                break

            for op in items:
                tipo = op.get("tipo_ativo")
                if tipo and tipo not in ("DEB", "Debênture", "Debêntures"):
                    continue
                ticker = op.get("codigo_ativo")
                if not ticker:
                    continue

                try:
                    qtd = float(op.get("qtd_negociada") or 0.0)
                    vol = float(op.get("vl_volume_negociado") or 0.0)
                    pu = float(op.get("vl_pu_negociado") or 0.0)
                except (ValueError, TypeError):
                    continue

                reune_agregado[ticker]["quantidade_negocios"] += 1
                reune_agregado[ticker]["quantidade_titulos"] += qtd
                reune_agregado[ticker]["volume_total_rs"] += vol
                if op.get("isin") and not reune_agregado[ticker]["isin"]:
                    reune_agregado[ticker]["isin"] = op.get("isin")
                if pu > 0:
                    reune_agregado[ticker]["precos"].append(pu)
                total_debs_ops += 1

            page += 1
            if page >= total_pages:
                break

        self.logger.info(
            f"REUNE: {total_debs_ops} operações de debêntures agregadas em {len(reune_agregado)} ativos."
        )
        return reune_agregado

    def fetch(self) -> pd.DataFrame:
        """
        Executa a captura da API de Mercado Secundário da ANBIMA e do REUNE,
        consolidando no padrão do PulseFlat compatível com o SND.
        """
        if not self.check_credentials():
            self.logger.warning("Credenciais da ANBIMA não configuradas. Encerrando.")
            return pd.DataFrame()

        data_ref = self._obter_data_referencia()
        data_str = data_ref.strftime("%Y-%m-%d")
        self.logger.info(f"Iniciando coleta para a data de referência: {data_str}")

        # 1. Busca Mercado Secundário da ANBIMA (Preços e Taxas Oficiais)
        try:
            dados_precos = self.client.get(
                "/feed/precos-indices/v1/debentures/mercado-secundario",
                params={"data": data_str},
            )
        except Exception as e:
            self.logger.error(f"Falha ao consultar Mercado Secundário da ANBIMA: {e}")
            return pd.DataFrame()

        if isinstance(dados_precos, dict):
            dados_precos = dados_precos.get("content", [])
        if not isinstance(dados_precos, list):
            dados_precos = []

        self.logger.info(f"Mercado Secundário ANBIMA: {len(dados_precos)} debêntures monitoradas.")

        # 2. Busca negociações consolidadas do REUNE
        reune_indexado = self._obter_operacoes_reune(data_str)

        # 3. Consolidação registro a registro
        precos_indexados = {
            item.get("codigo_ativo"): item for item in dados_precos if item.get("codigo_ativo")
        }
        todos_ativos = sorted(set(precos_indexados.keys()) | set(reune_indexado.keys()))

        registros = []
        for ticker in todos_ativos:
            item = precos_indexados.get(ticker, {})
            reune_info = reune_indexado.get(ticker, {})
            precos_reune = reune_info.get("precos", [])

            qtd_negocios = reune_info.get("quantidade_negocios", 0)
            qtd_titulos = reune_info.get("quantidade_titulos", 0.0)
            vol_total = reune_info.get("volume_total_rs", 0.0)
            pu_indicativo = item.get("pu")

            # Formatação de preços: se houve negócios calcula as métricas;
            # se não houve negócios, mantém vazio ("") para cálculos de liquidez
            if precos_reune:
                p_min = min(precos_reune)
                p_max = max(precos_reune)
                p_med = (vol_total / qtd_titulos) if qtd_titulos > 0 else (sum(precos_reune) / len(precos_reune))
                pu_min_str = f"{p_min:.6f}".rstrip("0").rstrip(".")
                pu_med_str = f"{p_med:.6f}".rstrip("0").rstrip(".")
                pu_max_str = f"{p_max:.6f}".rstrip("0").rstrip(".")
                qtd_str = str(int(qtd_titulos)) if qtd_titulos.is_integer() else f"{qtd_titulos:.2f}"
                neg_str = str(qtd_negocios)
            else:
                pu_min_str = ""
                pu_med_str = ""
                pu_max_str = ""
                qtd_str = "0"
                neg_str = "0"

            perc_pu_curva = item.get("percent_pu_par")
            perc_pu_str = str(perc_pu_curva).replace(",", ".") if perc_pu_curva is not None else ""

            registro = {
                "data_referencia": data_str,
                "emissor": item.get("emissor", ""),
                "codigo_ativo": ticker,
                "isin": reune_info.get("isin") or "",
                "quantidade": qtd_str,
                "numero_de_negocios": neg_str,
                "pu_minimo": pu_min_str,
                "pu_medio": pu_med_str,
                "pu_maximo": pu_max_str,
                "pu_da_curva": perc_pu_str,
                # Atributos adicionais da API para enriquecimento
                "pu_indicativo": str(pu_indicativo) if pu_indicativo is not None else "",
                "taxa_indicativa": str(item.get("taxa_indicativa", "") or ""),
                "taxa_compra": str(item.get("taxa_compra", "") or ""),
                "taxa_venda": str(item.get("taxa_venda", "") or ""),
                "percentual_taxa": str(item.get("percentual_taxa", "") or ""),
                "volume_total_rs": f"{vol_total:.2f}" if vol_total > 0 else "0.00",
                "percent_reune": str(item.get("percent_reune", "") or ""),
                "data_vencimento": str(item.get("data_vencimento", "") or ""),
            }
            registros.append(registro)

        df = pd.DataFrame(registros)
        if not df.empty:
            # Calcula registro_hash padrão PulseFlat para auditoria e integridade
            records_dict = df.to_dict(orient="records")
            df["registro_hash"] = [
                hash_row({k: v for k, v in r.items() if k not in ("data_captura", "registro_hash")})
                for r in records_dict
            ]
            self.logger.info(
                f"Consolidação concluída: {len(df)} debêntures no total (com negócios e zeradas)."
            )

        return df


def main():
    DebenturesMercadoSecundarioPrecosNegociacaoApiScraper().run()


if __name__ == "__main__":
    main()
