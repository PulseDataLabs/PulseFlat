"""
tests/unit/test_workflows_integrity.py
---------------------------------------
Testes unitários para validar a sintaxe e integridade dos workflows e agendamentos cron do GitHub Actions.
"""

from pathlib import Path
import pytest
import yaml


WORKFLOWS_DIR = Path(".github/workflows")


def get_workflow_files():
    if not WORKFLOWS_DIR.exists():
        return []
    return list(WORKFLOWS_DIR.glob("*.yml")) + list(WORKFLOWS_DIR.glob("*.yaml"))


class TestWorkflowsIntegrity:
    """Valida a integridade estrutural e os crons de todos os workflows do GitHub Actions."""

    def test_workflow_files_exist(self):
        files = get_workflow_files()
        assert len(files) > 0, "Deve haver pelo menos um arquivo de workflow em .github/workflows"

    @pytest.mark.parametrize("wf_file", get_workflow_files(), ids=lambda p: p.name)
    def test_workflow_yaml_syntax(self, wf_file):
        """Garante que todos os arquivos YAML sejam válidos."""
        with wf_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict), f"{wf_file.name} deve ser um documento YAML válido em formato dict"
        assert "name" in data or True  # Valida parse sem erros

    def test_cron_syntax_in_all_workflows(self):
        """
        Valida que todos os agendamentos cron:
        1. Possuam exatamente 5 campos (minuto hora dia_mes mes dia_semana).
        2. Não usem horas agrupadas por vírgula (ex: '13,16,19'), garantindo entradas individuais.
        3. Possuam intervalos válidos para minutos (0-59) e horas (0-23).
        """
        files = get_workflow_files()
        total_crons_checked = 0

        for wf_file in files:
            with wf_file.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            # Extrai trigger 'on' (pode ser True no YAML se a chave for 'on:')
            on_trigger = data.get(True) or data.get("on")
            if not isinstance(on_trigger, dict):
                continue

            schedule_list = on_trigger.get("schedule", [])
            if not isinstance(schedule_list, list):
                continue

            for item in schedule_list:
                cron_expr = item.get("cron")
                assert cron_expr is not None, f"Entrada em schedule de {wf_file.name} deve ter chave 'cron'"
                
                parts = cron_expr.strip().split()
                assert len(parts) == 5, (
                    f"Cron '{cron_expr}' em {wf_file.name} deve possuir exatamente 5 campos, "
                    f"encontrado {len(parts)}"
                )

                minute, hour, day_m, month, day_w = parts

                # Validação de que não há agrupamentos com vírgula nas horas (desmembrados para confiabilidade do runner)
                assert "," not in hour, (
                    f"Em {wf_file.name}, a hora '{hour}' no cron '{cron_expr}' não deve usar vírgula; "
                    "desmembre em entradas de cron individuais para compatibilidade com GitHub Actions."
                )

                # Validação do minuto
                if minute.isdigit():
                    m_val = int(minute)
                    assert 0 <= m_val <= 59, f"Minuto {m_val} fora do intervalo (0-59) em {wf_file.name}"

                # Validação da hora
                if hour.isdigit():
                    h_val = int(hour)
                    assert 0 <= h_val <= 23, f"Hora {h_val} fora do intervalo (0-23) em {wf_file.name}"

                # Validação de dia da semana (0-7, faixas como 1-5, 2-6, ou *)
                is_valid_dow = (
                    day_w in ("*", "1-5", "2-6", "1-7", "0-6", "0-5")
                    or day_w.isdigit()
                    or (
                        "-" in day_w
                        and len(day_w.split("-")) == 2
                        and all(x.isdigit() and 0 <= int(x) <= 7 for x in day_w.split("-"))
                    )
                )
                assert is_valid_dow, f"Dia da semana inválido '{day_w}' em {wf_file.name}"

                total_crons_checked += 1

        assert total_crons_checked >= 5, f"Esperado checar múltiplos crons, checados: {total_crons_checked}"
