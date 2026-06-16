#!/bin/bash
set -e

cd /app

echo "[entrypoint] Iniciando HTTP server na porta 80..."
python -m http.server 80 --bind 0.0.0.0 &

echo "[entrypoint] Configurando cron jobs..."
{
  echo "${CRON_RUN_ALL:-0 10,13,16,19,22 * * 1-5} cd /app && python run_all.py >> /var/log/cron.log 2>&1"
} > /etc/cron.d/pulseflat-cron \
  && chmod 0644 /etc/cron.d/pulseflat-cron \
  && crontab /etc/cron.d/pulseflat-cron

echo "[entrypoint] Iniciando cron daemon..."
cron

echo "[entrypoint] Executando coleta inicial..."
python run_all.py >> /var/log/cron.log 2>&1 || echo "[entrypoint] Coleta inicial concluída (com avisos)"

echo "[entrypoint] Container pronto. Schedule: ${CRON_RUN_ALL:-0 10,13,16,19,22 * * 1-5} UTC"
echo "---"

touch /var/log/cron.log
tail -f /var/log/cron.log
